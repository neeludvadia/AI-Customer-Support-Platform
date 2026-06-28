from typing import List, Dict
from google import genai
from google.genai import types

from modules.ai.ports import LLMProvider, EmbeddingProvider
from config.settings import settings

# ------------------------------------------------------------------------
# ADAPTERS (Implementations)
# These files contain the exact code to talk to specific services (Gemini).
# ------------------------------------------------------------------------

class GeminiLLMAdapter(LLMProvider):
    def __init__(self):
        # We grab the API key from settings
        api_key = settings.GEMINI_API_KEY
        if not api_key or api_key == "your_gemini_api_key_here":
            self.client = None
        else:
            self.client = genai.Client(api_key=api_key)

    def generate_response(self, system_instruction: str, messages: List[Dict[str, str]]) -> str:
        if not self.client:
            raise ValueError("Gemini API key is not configured in .env file.")

        # Convert generic message dictionaries into Gemini's expected Content format
        contents = []
        for msg in messages:
            # Our generic format uses "sender": "user" or "assistant"
            # Gemini expects "role": "user" or "model"
            gemini_role = "user" if msg.get("sender") == "user" else "model"
            
            contents.append(
                types.Content(
                    role=gemini_role,
                    parts=[types.Part(text=msg.get("text", ""))]
                )
            )

        # Call the Gemini API
        try:
            config = types.GenerateContentConfig(system_instruction=system_instruction)
            
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents,
                config=config
            )
            return response.text or "I am sorry, I could not generate a response."
            
        except Exception as e:
            return f"Error communicating with AI service: {str(e)}"


class GeminiEmbeddingAdapter(EmbeddingProvider):
    def __init__(self):
        api_key = settings.GEMINI_API_KEY
        if not api_key or api_key == "your_gemini_api_key_here":
            self.client = None
        else:
            self.client = genai.Client(api_key=api_key)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        if not self.client:
            raise ValueError("Gemini API key is not configured in .env file.")
        
        if not texts:
            return []

        try:
            # We use the embedding model specified in config (usually gemini-embedding-001)
            response = self.client.models.embed_content(
                model=settings.EMBEDDING_MODEL,
                contents=texts,
            )
            
            # Extract the actual float values from the response
            if hasattr(response, "embeddings"):
                return [emb.values for emb in response.embeddings]
            elif hasattr(response, "embedding"):
                return [response.embedding.values]
            else:
                raise ValueError("Unexpected response format from Gemini Embeddings API")
                
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            raise e
