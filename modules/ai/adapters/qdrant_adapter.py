import uuid
from typing import List, Dict, Tuple
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from modules.ai.ports import VectorStoreProvider
from config.settings import settings

class QdrantVectorStoreAdapter(VectorStoreProvider):
    def __init__(self):
        self.qdrant_client = QdrantClient(url=settings.QDRANT_URL)
        self.collection_name = settings.QDRANT_COLLECTION
        self._ensure_collection()

    def _ensure_collection(self):
        # We assume vectors from gemini-embedding-001 have a size of 3072.
        # If you swap embedding models in the future, you may need to recreate
        # the collection with the new vector size!
        if not self.qdrant_client.collection_exists(self.collection_name):
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=3072,
                    distance=Distance.COSINE
                )
            )

    def upsert_chunks(
        self, 
        document_id: int, 
        title: str, 
        original_filename: str, 
        all_chunks: List[Tuple[str, int]], 
        embeddings: List[List[float]]
    ) -> None:
        
        points = []
        for i, ((chunk_text, page_number), embedding) in enumerate(zip(all_chunks, embeddings)):
            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload={
                        "document_id": document_id,
                        "title": title,
                        "original_filename": original_filename,
                        "text": chunk_text,
                        "page_number": page_number,
                        "chunk_index": i,
                    },
                )
            )

        if points:
            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=points,
            )

    def search_similar(self, query_vector: List[float], top_k: int = 3) -> List[Dict]:
        if not query_vector:
            return []

        results = self.qdrant_client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=top_k,
        )

        chunks = []
        if hasattr(results, "points") and results.points:
            for hit in results.points:
                p = hit.payload or {}
                chunks.append({
                    "document_id": p.get("document_id"),
                    "title": p.get("title"),
                    "original_filename": p.get("original_filename"),
                    "text": p.get("text"),
                    "page_number": p.get("page_number"),
                    "score": hit.score,
                })
        return chunks
