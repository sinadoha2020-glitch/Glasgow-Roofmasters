"""Gallery image model."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Integer as SAInt
from app.core.database import Base


class GalleryImage(Base):
    """Store gallery images with metadata."""

    __tablename__ = "gallery_images"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    service_category = Column(String(100), nullable=True)  # e.g., "new-roof", "restoration"
    image_path = Column(String(500), nullable=False)  # relative path
    thumbnail_path = Column(String(500), nullable=True)
    alt_text = Column(String(300), nullable=False)

    # Display order and visibility
    display_order = Column(SAInt, default=0)
    is_active = Column(Boolean, default=True)
    is_placeholder = Column(Boolean, default=True)

    # Location info for SEO
    location = Column(String(100), nullable=True)  # e.g., "Glasgow West End"

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<GalleryImage(id={self.id}, title={self.title})>"
