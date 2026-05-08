from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Index
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Auth
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=True)  # Can be null for OAuth users
    
    # Profile
    full_name = Column(String(255), nullable=True)
    profile_picture_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    
    # Student info
    college = Column(String(255), nullable=True)
    batch_year = Column(Integer, nullable=True)
    is_verified_student = Column(Boolean, default=False)
    
    # Account status
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    
    # OAuth
    google_id = Column(String(255), unique=True, nullable=True)
    oauth_provider = Column(String(50), nullable=True)  # 'google', etc.
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime, nullable=True)
    
    __table_args__ = (
        Index("idx_email", "email"),
        Index("idx_username", "username"),
    )
    
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "full_name": self.full_name,
            "profile_picture_url": self.profile_picture_url,
            "college": self.college,
            "batch_year": self.batch_year,
            "is_verified_student": self.is_verified_student,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat(),
        }
