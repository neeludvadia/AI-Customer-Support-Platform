import os
import uuid

from pypdf import PdfReader
from sqlalchemy.orm import Session

from config.settings import settings
from modules.knowledge_base.models import Document
from modules.knowledge_base.repository import DocumentRepository


class KnowledgeBaseService:
    def __init__(self, db: Session):
        self.repo = DocumentRepository(db)

    def upload_pdf(self, filename: str, file_bytes: bytes, uploaded_by: int) -> Document:
        """Save the PDF locally and trigger text extraction."""
        # Ensure uploads directory exists
        uploads_path = os.path.abspath(settings.UPLOADS_DIR)
        os.makedirs(uploads_path, exist_ok=True)

        # Save file with a unique name to avoid collisions
        unique_name = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(uploads_path, unique_name)

        with open(file_path, "wb") as f:
            f.write(file_bytes)

        # Persist record
        title = os.path.splitext(filename)[0]
        doc = self.repo.create(
            title=title,
            original_filename=filename,
            file_path=file_path,
            uploaded_by=uploaded_by,
        )

        # Extract text immediately (can be moved to a background task later)
        self._extract_and_save(doc.id, file_path, original_filename=filename)
        return self.repo.get_by_id(doc.id)

    def _extract_and_save(self, doc_id: int, file_path: str, original_filename: str) -> None:
        """Extract text from PDF per page and update the document record."""
        try:
            reader = PdfReader(file_path)

            # Build per-page list for Qdrant (1-indexed pages)
            pages = []
            all_text_parts = []
            for page_num, page in enumerate(reader.pages, start=1):
                page_text = page.extract_text() or ""
                all_text_parts.append(page_text)
                if page_text.strip():
                    pages.append({"text": page_text, "page_number": page_num})

            extracted = "\n".join(all_text_parts).strip()
            self.repo.update_extracted_text(doc_id, extracted, status="processed")

            # Index to Qdrant vector database with page-level granularity
            if pages:
                try:
                    from modules.knowledge_base.vector_store import VectorStoreHelper
                    vector_store = VectorStoreHelper()
                    doc = self.repo.get_by_id(doc_id)
                    title = doc.title if doc else f"Doc {doc_id}"
                    vector_store.index_document(
                        doc_id=doc_id,
                        title=title,
                        original_filename=original_filename,
                        pages=pages,
                    )
                except Exception as ve:
                    print(f"Error indexing document {doc_id} to vector store: {ve}")
        except Exception:
            self.repo.update_extracted_text(doc_id, "", status="failed")

    def get_document(self, doc_id: int) -> Document | None:
        return self.repo.get_by_id(doc_id)

    def list_documents(self) -> list[Document]:
        return self.repo.get_all()
