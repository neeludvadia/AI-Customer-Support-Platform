from modules.ai.ports import LLMProvider, EmbeddingProvider, VectorStoreProvider
from modules.ai.adapters.gemini_adapter import GeminiLLMAdapter, GeminiEmbeddingAdapter
from modules.ai.adapters.qdrant_adapter import QdrantVectorStoreAdapter

# ------------------------------------------------------------------------
# DEPENDENCY INJECTION (Factories)
# These functions return the concrete implementations. 
# FastAPI's Depends() will use these to inject the dependencies.
# If you want to switch to OpenAI, just change what these functions return!
# ------------------------------------------------------------------------

def get_llm_provider() -> LLMProvider:
    return GeminiLLMAdapter()

def get_embedding_provider() -> EmbeddingProvider:
    return GeminiEmbeddingAdapter()

def get_vector_store_provider() -> VectorStoreProvider:
    return QdrantVectorStoreAdapter()
