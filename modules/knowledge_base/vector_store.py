import uuid
from google import genai
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from config.settings import settings


class VectorStoreHelper:
    def __init__(self):
        self.qdrant_client = QdrantClient(
            url=settings.QDRANT_URL
        )
        self.collection_name = settings.QDRANT_COLLECTION
        
        # Initialize Gemini API Client
        api_key = settings.GEMINI_API_KEY
        if api_key and api_key != "your_gemini_api_key_here":
            self.genai_client = genai.Client(api_key=api_key)
        else:
            self.genai_client = None

        self._ensure_collection()

    def _ensure_collection(self):
        # Check if collection exists, if not we create it.
        # Vector size for gemini-embedding-001 is 3072.
        if not self.qdrant_client.collection_exists(self.collection_name):
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=3072,
                    distance=Distance.COSINE
                )
            )

    def chunk_text(self, text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:
        if not text:
            return []
        # Basic character-based overlap chunking
        chunks = []
        start = 0
        text_len = len(text)
        while start < text_len:
            end = start + chunk_size
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            # Advance by chunk_size - chunk_overlap
            start += chunk_size - chunk_overlap
            # If the next start is beyond text length, stop
            if start >= text_len or (chunk_size - chunk_overlap <= 0):
                break
        return chunks

    def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        if not self.genai_client:
            raise ValueError(
                "Gemini API key is not configured. "
                "Please configure GEMINI_API_KEY in your .env file."
            )
        if not texts:
            return []

        # Google GenAI embed_content supports batching or single text
        try:
            response = self.genai_client.models.embed_content(
                model=settings.EMBEDDING_MODEL,
                contents=texts,
            )
            # Response embeddings is a list of embeddings. Each embedding has a field `.values`
            if hasattr(response, "embeddings"):
                return [emb.values for emb in response.embeddings]
            elif hasattr(response, "embedding"):
                # single result
                return [response.embedding.values]
            else:
                raise ValueError("Unexpected response format from Gemini Embeddings API")
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            raise e

    def embed_query(self, text: str) -> list[float]:
        embeddings = self.generate_embeddings([text])
        return embeddings[0] if embeddings else []

    def index_document(self, doc_id: int, title: str, text: str) -> None:
        chunks = self.chunk_text(text)
        if not chunks:
            return
        
        embeddings = self.generate_embeddings(chunks)
        
        points = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            point_id = str(uuid.uuid4())
            points.append(
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "document_id": doc_id,
                        "title": title,
                        "text": chunk,
                        "chunk_index": i
                    }
                )
            )
        
        if points:
            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=points
            )

    def search_similar_chunks(self, query_vector: list[float], top_k: int = 3) -> list[dict]:
        if not query_vector:
            return []
            
        results = self.qdrant_client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=top_k
        )
        
        chunks = []
        if hasattr(results, "points") and results.points:
            for hit in results.points:
                chunks.append({
                    "document_id": hit.payload.get("document_id") if hit.payload else None,
                    "title": hit.payload.get("title") if hit.payload else None,
                    "text": hit.payload.get("text") if hit.payload else None,
                    "score": hit.score
                })
        return chunks
