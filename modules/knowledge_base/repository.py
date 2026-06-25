from sqlalchemy.orm import Session
from modules.knowledge_base.models import Document


class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, title: str, original_filename: str, file_path: str, uploaded_by: int) -> Document:
        doc = Document(
            title=title,
            original_filename=original_filename,
            file_path=file_path,
            uploaded_by=uploaded_by,
        )
        self.db.add(doc)
        self.db.commit()
        self.db.refresh(doc)
        return doc

    def update_extracted_text(self, doc_id: int, text: str, status: str) -> Document | None:
        doc = self.db.query(Document).filter(Document.id == doc_id).first()
        if doc:
            doc.extracted_text = text
            doc.status = status
            self.db.commit()
            self.db.refresh(doc)
        return doc

    def get_by_id(self, doc_id: int) -> Document | None:
        return self.db.query(Document).filter(Document.id == doc_id).first()

    def get_all(self) -> list[Document]:
        return self.db.query(Document).order_by(Document.created_at.desc()).all()
