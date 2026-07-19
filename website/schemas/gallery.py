"""Gallery schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class GalleryImageBase(BaseModel):
    """Base gallery image schema."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    service_category: Optional[str] = Field(None, max_length=100)
    alt_text: str = Field(..., min_length=5, max_length=300)
    location: Optional[str] = Field(None, max_length=100)
    display_order: int = Field(0, ge=0)
    is_active: bool = True
    is_placeholder: bool = True


class GalleryImageCreate(GalleryImageBase):
    """Schema for creating a gallery image."""
    image_path: str = Field(..., min_length=1, max_length=500)
    thumbnail_path: Optional[str] = Field(None, max_length=500)


class GalleryImageResponse(GalleryImageBase):
    """Schema for gallery image response."""
    id: int
    image_path: str
    thumbnail_path: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
