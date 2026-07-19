"""Database models."""
from app.core.database import Base
from app.models.inquiry import Inquiry
from app.models.gallery import GalleryImage
from app.models.cms import CMSSetting

__all__ = ["Base", "Inquiry", "GalleryImage", "CMSSetting"]
