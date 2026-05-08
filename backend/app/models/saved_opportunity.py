from sqlalchemy import Column, Integer, DateTime, ForeignKey, Index, UniqueConstraint
from datetime import datetime
from app.core.database import Base

class SavedOpportunity(Base):
    __tablename__ = "saved_opportunities"
    
    id = Column(Integer, primary_key=True, index=True)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"), nullable=False, index=True)
    
    saved_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    __table_args__ = (
        UniqueConstraint("user_id", "opportunity_id", name="unique_user_opportunity"),
        Index("idx_user_id", "user_id"),
        Index("idx_opportunity_id", "opportunity_id"),
    )
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "opportunity_id": self.opportunity_id,
            "saved_at": self.saved_at.isoformat(),
        }
