from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from database.database import get_db
from modules.auth.dependencies import get_current_user
from modules.auth.models import User
from modules.knowledge_base.dto import DocumentResponse, DocumentUploadResponse
from modules.knowledge_base.service import KnowledgeBaseService
from modules.ai.ports import EmbeddingProvider, VectorStoreProvider
from modules.ai.dependencies import get_embedding_provider, get_vector_store_provider

router = APIRouter(prefix="/knowledge-base", tags=["Knowledge Base"])


@router.post("/upload", response_model=DocumentUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    embedding_provider: EmbeddingProvider = Depends(get_embedding_provider),
    vector_store: VectorStoreProvider = Depends(get_vector_store_provider),
):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are accepted",
        )

    file_bytes = await file.read()
    service = KnowledgeBaseService(db, embedding_provider=embedding_provider, vector_store=vector_store)
    doc = service.upload_pdf(
        filename=file.filename,
        file_bytes=file_bytes,
        uploaded_by=current_user.id,
    )
    return DocumentUploadResponse(
        id=doc.id,
        title=doc.title,
        original_filename=doc.original_filename,
        status=doc.status,
        message="PDF uploaded and text extracted successfully" if doc.status == "processed" else "PDF uploaded but text extraction failed",
    )


@router.get("/{doc_id}", response_model=DocumentResponse)
def get_document(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    doc = KnowledgeBaseService(db).get_document(doc_id)
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    return doc


@router.get("/", response_model=list[DocumentResponse])
def list_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return KnowledgeBaseService(db).list_documents()
