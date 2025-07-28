import os
import shutil
from typing import List, Dict, Any, Optional, Union
from langchain.schema.document import Document
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pymupdf

from .text_utils import clean_text

def load_and_split_documents(
    data_path: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 100
) -> List[Document]:
    docs: List[Document] = []
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=['\\. ', '\n\n', '\n', ' ', '']
    )
    for fname in sorted(os.listdir(data_path)):
        if not fname.lower().endswith('.pdf'):
            continue
        full_path = os.path.join(data_path, fname)
        pdf = pymupdf.open(full_path)
        for page_num in range(len(pdf)):
            raw_text = pdf[page_num].get_text("text")
            docs.append(Document(page_content=raw_text, metadata={'source': fname, 'page': page_num + 1}))
        pdf.close()
    chunks = splitter.split_documents(docs)
    for c in chunks:
        content = c.page_content
        last_dot = content.rfind('.')
        if last_dot != -1:
            c.page_content = content[:last_dot+1]
    return chunks

def calculate_chunk_ids(chunks: List[Document]) -> None:
    last: Optional[str] = None
    idx = 0
    for c in chunks:
        key = f"{c.metadata['source']}:{c.metadata['page']}"
        idx = idx + 1 if key == last else 0
        c.metadata['id'] = f"{key}:{idx}"
        last = key

def build_chroma(
    chunks: List[Document],
    persist_directory: str = 'chroma',
    embedding_function=None
) -> Chroma:
    if os.path.exists(persist_directory):
        shutil.rmtree(persist_directory)
    if embedding_function is None:
        from .embedding import get_embedding_function
        embedding_function = get_embedding_function()
    db = Chroma(persist_directory=persist_directory, embedding_function=embedding_function)
    calculate_chunk_ids(chunks)
    db.add_documents(documents=chunks, ids=[c.metadata['id'] for c in chunks])
    return db

def query_and_format(
    db: Chroma,
    input_meta: Dict[str, Any],
    query: str,
    top_k: int = 5
) -> Dict[str, Any]:
    results = db.similarity_search_with_score(query, k=top_k)
    raw_docs = input_meta.get('documents', [])
    docs_list = [os.path.basename(item['filename']) if isinstance(item, dict) else os.path.basename(item) for item in raw_docs]
    out: Dict[str, Any] = {
        'metadata': {
            'input_documents': docs_list,
            'persona': input_meta.get('persona', {}).get('role', ''),
            'job_to_be_done': input_meta.get('job_to_be_done', {}).get('task', '')
        },
        'extracted_sections': [],
        'subsection_analysis': []
    }
    for rank, (doc, _) in enumerate(results, start=1):
        lines = [ln.strip() for ln in doc.page_content.splitlines() if ln.strip()]
        title = lines[0] if lines else ''
        out['extracted_sections'].append({'document': doc.metadata['source'], 'section_title': title, 'rank': rank})
    for doc, _ in results:
        raw_snippet = doc.page_content[:200]
        last_dot = raw_snippet.rfind('.')
        if last_dot != -1:
            raw_snippet = raw_snippet[: last_dot + 1]
        cleaned = clean_text(raw_snippet)
        out['subsection_analysis'].append({'document': doc.metadata['source'], 'text': cleaned})
    return out