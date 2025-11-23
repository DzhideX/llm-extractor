from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.params import Query, Path
from sqlalchemy.orm import Session
from typing import List
from dotenv import load_dotenv
import tempfile
import os

from . import models, schemas
from .database import Base, engine, get_db
from .utils.llm import extract_with_llm
from .utils.pdf import extract_pdf_text
from .utils.general import parse_date


load_dotenv()

app = FastAPI(title="LLM Extraction API")

Base.metadata.create_all(bind=engine)

@app.post("/api/extract", response_model=schemas.ExtractionResponse)
async def extract_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload and extract document structure using AI.
    
    Args:
        file: PDF file to extract
        db: Database session
        
    Raises:
        HTTPException: 400 if file is not a PDF
        HTTPException: 500 if PDF parsing fails
        HTTPException: 500 if LLM extraction fails
        
    Returns:
        ExtractionResponse: Document with extracted metadata and clauses
    """

    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type. Only PDF files are accepted. Received: {file.filename}"
        )

    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_file_path = tmp_file.name
    
    try:
        try:
            pdf_data = extract_pdf_text(tmp_file_path)
        except Exception:
            raise HTTPException(
                status_code=500, 
                detail="Unable to parse PDF. File may be corrupted or password-protected."
            )

        try:
            llm_result = extract_with_llm(
                pdf_text=pdf_data['full_text'],
            )
        except Exception:
            raise HTTPException(
                status_code=500, 
                detail="Failed to extract document. Please try again or contact support if the issue persists."
            )

        db_document = models.Document(
            title=llm_result['document']['title'],
            document_type=llm_result['document']['document_type'],
            effective_date=parse_date(llm_result['document']['effective_date']),
            file_name=pdf_data['metadata'].get('title') or file.filename
        )
        db.add(db_document)
        db.flush()

        for clause_data in llm_result['clauses']:
            db_clause = models.Clause(
                document_id=db_document.id,
                clause_number=clause_data['clause_number'],
                heading=clause_data['heading'],
                clause_type=clause_data['clause_type'],
                start_page=clause_data['start_page'],
                end_page=clause_data['end_page']
            )
            db.add(db_clause)

        db.commit()
        db.refresh(db_document)
        return db_document
    
    finally:
        os.unlink(tmp_file_path)

@app.get("/api/extractions/{document_id}", response_model=schemas.ExtractionResponse)
def get_extraction(
    document_id: int = Path(..., ge=1, description="Document ID"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific extraction by document ID.
    
    Args:
        document_id: ID of the document to retrieve (must be >= 1)
        db: Database session
        
    Raises:
        HTTPException: 404 if document not found
        
    Returns:
        ExtractionResponse: Document with all its clauses
    """
    document = db.query(models.Document).filter(
        models.Document.id == document_id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=404, 
            detail=f"Document with ID {document_id} not found. Use GET /api/extractions to see available documents."
        )
    
    return document


@app.get("/api/extractions", response_model=List[schemas.ExtractionResponse])
def list_extractions(
    offset: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Max records to return"),
    db: Session = Depends(get_db)
):
    """
    List all document extractions with pagination.
    
    Args:
        offset: Number of records to skip (default: 0)
        limit: Maximum records to return (default: 100, max: 1000)
        db: Database session
        
    Returns:
        List[ExtractionResponse]: List of documents with their clauses
    """
    documents = db.query(models.Document).offset(offset).limit(limit).all()
    return documents