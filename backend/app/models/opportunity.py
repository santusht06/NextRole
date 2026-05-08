from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, Index, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from app.core.database import Base

class Opportunity(Base):
    __tablename__ = "opportunities"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic info
    title = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    
    # Structured data (AI-extracted)
    opportunity_type = Column(String(100), nullable=False, index=True)  # internship, hackathon, etc.
    deadline = Column(DateTime, nullable=True, index=True)
    location = Column(String(255), nullable=True)
    is_remote = Column(Boolean, default=False, index=True)
    
    # Extracted information (from AI)
    eligibility = Column(JSON, default=[])  # List of eligibility criteria
    skills_required = Column(JSON, default=[])  # List of required skills
    summary = Column(Text, nullable=True)
    
    # Links and status
    apply_link = Column(String(500), nullable=False)
    source_url = Column(String(500), nullable=True)
    source_platform = Column(String(100), nullable=True, index=True)  # devfolio, hackerearth, etc.
    
    # Status tracking
    status = Column(String(50), default="active", index=True)  # active, expired, archived
    is_verified = Column(Boolean, default=False)
    
    # Freshness tracking
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_verified_at = Column(DateTime, nullable=True)
    
    # Raw data (for debugging/reference)
    raw_data = Column(JSON, nullable=True)
    
    # Embeddings reference
    embedding_id = Column(Integer, nullable=True, index=True)
    
    # Ranking/relevance
    relevance_score = Column(Float, default=0.0)
    
    __table_args__ = (
        Index("idx_opportunity_type_status", "opportunity_type", "status"),
        Index("idx_deadline_status", "deadline", "status"),
        Index("idx_created_at", "created_at"),
    )
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "description": self.description,
            "type": self.opportunity_type,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "location": self.location,
            "is_remote": self.is_remote,
            "eligibility": self.eligibility,
            "skills": self.skills_required,
            "summary": self.summary,
            "apply_link": self.apply_link,
            "source_url": self.source_url,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
