from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List

class ClauseBase(BaseModel):
    clause_number: Optional[str] = None
    heading: Optional[str] = None
    clause_type: Optional[str] = None
    start_page: Optional[int] = None
    end_page: Optional[int] = None

class Clause(ClauseBase):
    id: int
    document_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class DocumentBase(BaseModel):
    title: Optional[str] = None
    document_type: Optional[str] = None
    effective_date: Optional[date] = None
    file_name: Optional[str] = None

class Document(DocumentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class DocumentWithClauses(Document):
    clauses: List[Clause] = []

    class Config:
        from_attributes = True


class ExtractionResponse(DocumentWithClauses):
    """Response for extraction endpoints"""
    pass