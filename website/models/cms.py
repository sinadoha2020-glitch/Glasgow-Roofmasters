"""CMS settings model for editable business info."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.core.database import Base


class CMSSetting(Base):
    """Key-value store for editable CMS settings."""

    __tablename__ = "cms_settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False, index=True)
    value = Column(Text, nullable=False)
    description = Column(String(500), nullable=True)
    group = Column(String(50), default="general")  # general, contact, social, seo

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<CMSSetting(key={self.key})>"
