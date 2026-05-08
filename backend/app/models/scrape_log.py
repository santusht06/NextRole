from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from datetime import datetime
from app.core.database import Base

class ScrapeLog(Base):
    __tablename__ = "scrape_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Scrape details
    source = Column(String(100), nullable=False)  # 'devfolio', 'hackerearth', etc.
    status = Column(String(50), nullable=False)  # 'success', 'failed', 'partial'
    
    # Counts
    opportunities_found = Column(Integer, default=0)
    opportunities_added = Column(Integer, default=0)
    opportunities_updated = Column(Integer, default=0)
    
    # Error handling
    error_message = Column(Text, nullable=True)
    
    # Timing
    started_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        duration = None
        if self.completed_at:
            duration = (self.completed_at - self.started_at).total_seconds()
        
        return {
            "id": self.id,
            "source": self.source,
            "status": self.status,
            "opportunities_found": self.opportunities_found,
            "opportunities_added": self.opportunities_added,
            "opportunities_updated": self.opportunities_updated,
            "error_message": self.error_message,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_seconds": duration,
        }
