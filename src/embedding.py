from typing import List, Optional
from fastembed import TextEmbedding

def get_embedding_function(model_path: Optional[str] = None):
    class EmbeddingWrapper:
        def __init__(self):
            if model_path:
                self.model = TextEmbedding(model_name_or_path=model_path)
            else:
                self.model = TextEmbedding()
        def embed_documents(self, texts: List[str]) -> List[List[float]]:
            return list(self.model.embed(texts))
        def embed_query(self, text: str) -> List[float]:
            return list(self.model.embed([text]))[0]
    return EmbeddingWrapper()