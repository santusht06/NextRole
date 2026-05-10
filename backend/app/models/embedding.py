from sqlalchemy import Column, Integer, DateTime, String, JSON, Index
from pgvector.sqlalchemy import Vector
from datetime import datetime
from app.core.database import Base


class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True, index=True)

    # What we're embedding
    entity_type = Column(String(50), nullable=False)  # 'opportunity', 'user_query'
    entity_id = Column(
        Integer, nullable=True, index=True
    )  # Reference to opportunity or user

    # The text that was embedded
    text = Column(String(2000), nullable=False)

    # The embedding vector (1536-dimensional for OpenAI's text-embedding-3-small)
    embedding = Column(Vector(1536), nullable=False)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    metadata = Column(JSON, default={})

    __table_args__ = (Index("idx_entity_type_id", "entity_type", "entity_id"),)

    def to_dict(self):
        return {
            "id": self.id,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "text": self.text,
            "created_at": self.created_at.isoformat(),
        }
