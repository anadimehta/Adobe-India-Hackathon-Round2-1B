import os
import sys
import json
import argparse
from typing import Dict, Any, Optional, Union

from .embedding import get_embedding_function
from .chroma_db import load_and_split_documents, build_chroma, query_and_format

def get_json_result_for_query(
    input_spec: Union[str, Dict[str, Any]],
    output_path: Optional[str] = None,
    model_path: Optional[str] = None
) -> Dict[str, Any]:
    if isinstance(input_spec, str):
        input_spec_path = os.path.abspath(input_spec)
        with open(input_spec_path) as f:
            spec = json.load(f)
        spec_dir = os.path.dirname(input_spec_path)
    else:
        spec = input_spec
        spec_dir = os.getcwd()
    embedding_fn = get_embedding_function(model_path)
    if 'query' in spec:
        query = spec.pop('query')
    else:
        challenge = spec.get('challenge_info', {})
        query = challenge.get('description', '').strip()
        if not query:
            raise ValueError("Specification must include a 'query' field or a 'challenge_info.description'.")
    data_path = spec.get('data_path')
    if not data_path:
        common_dir_names = ['data', 'PDFs', 'pdfs', 'documents', 'docs']
        data_path = next((os.path.join(spec_dir, d) for d in common_dir_names if os.path.exists(os.path.join(spec_dir, d))), None)
        if not data_path:
            data_path = os.path.join(spec_dir, 'data')
    else:
        if not os.path.isabs(data_path):
            data_path = os.path.join(spec_dir, data_path)
    persist_dir = spec.get('persist_dir') or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chroma')
    if not os.path.isabs(persist_dir):
        persist_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), persist_dir)
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data directory not found: {data_path}")
    chunks = load_and_split_documents(data_path)
    db = build_chroma(chunks, persist_directory=persist_dir, embedding_function=embedding_fn)
    result = query_and_format(db, spec, query)
    if output_path:
        if not os.path.isabs(output_path):
            output_path = os.path.abspath(output_path)
        with open(output_path, 'w') as f_out:
            json.dump(result, f_out, indent=2)
    return result

def main():
    parser = argparse.ArgumentParser(
        description='Offline semantic search: specify local embedding model path.'
    )
    parser.add_argument('input', help='Path to input JSON spec')
    parser.add_argument('output', nargs='?', default='outline.json', help='Optional output JSON file')
    parser.add_argument('--model-path', '-m', help='Local path to pretrained embedding model directory')
    args = parser.parse_args()
    model_path = args.model_path or os.getenv('FASTEMBED_EMBEDDING_MODEL')
    global embedded_fn
    embedded_fn = get_embedding_function(model_path)
    try:
        input_path = os.path.abspath(args.input)
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
        output_path = os.path.abspath(args.output) if args.output else None
        res = get_json_result_for_query(input_path, output_path, model_path)
        print(f'Results saved to {output_path}')
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()