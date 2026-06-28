from abc import ABC, abstractmethod
from typing import List, Dict

# ------------------------------------------------------------------------
# PORTS (Interfaces)
# These define what an AI provider should do, but not HOW it does it.
# ------------------------------------------------------------------------

class LLMProvider(ABC):
    """
    Interface for a Large Language Model provider (e.g. Gemini, OpenAI, Claude).
    """
    
    @abstractmethod
    def generate_response(self, system_instruction: str, messages: List[Dict[str, str]]) -> str:
        """
        Generate a text response based on conversation history.
        
        Args:
            system_instruction (str): The initial prompt instructing the AI how to behave.
            messages (List[Dict]): A list of message dictionaries e.g. [{"sender": "user", "text": "hello"}]
        
        Returns:
            str: The AI's response text.
        """
        pass


class EmbeddingProvider(ABC):
    """
    Interface for a text embedding provider.
    """
    
    @abstractmethod
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Convert a list of strings into a list of vector embeddings.
        """
        pass


class VectorStoreProvider(ABC):
    """
    Interface for a Vector Database (e.g. Qdrant, Pinecone).
    """
    
    @abstractmethod
    def upsert_chunks(self, document_id: int, title: str, original_filename: str, all_chunks: List[tuple[str, int]], embeddings: List[List[float]]) -> None:
        """
        Save text chunks and their embeddings into the database.
        
        Args:
            all_chunks: List of tuples containing (chunk_text, page_number)
            embeddings: List of vectors corresponding to each chunk
        """
        pass

    @abstractmethod
    def search_similar(self, query_vector: List[float], top_k: int = 3) -> List[Dict]:
        """
        Search for the closest text chunks to the provided query vector.
        
        Returns:
            List of dictionaries containing document_id, text, score, etc.
        """
        pass
