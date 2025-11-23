from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(Text, nullable=True)
    document_type = Column(String(100), nullable=True)
    effective_date = Column(Date, nullable=True)
    file_name = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    clauses = relationship("Clause", back_populates="document", cascade="all, delete-orphan")


class Clause(Base):
    __tablename__ = "clauses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    clause_number = Column(String(50), nullable=True)
    heading = Column(Text, nullable=True)
    clause_type = Column(String(100), nullable=True)
    start_page = Column(Integer, nullable=True)
    end_page = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    document = relationship("Document", back_populates="clauses")