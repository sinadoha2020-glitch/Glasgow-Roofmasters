"""Gallery API routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.gallery import GalleryImage
from app.schemas.gallery import GalleryImageResponse

router = APIRouter(prefix="/api/gallery", tags=["gallery"])


@router.get("/", response_model=List[GalleryImageResponse])
async def list_gallery_images(
    category: str = None,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """List gallery images, optionally filtered by category."""
    query = db.query(GalleryImage)

    if active_only:
        query = query.filter(GalleryImage.is_active == True)
    if category:
        query = query.filter(GalleryImage.service_category == category)

    images = query.order_by(GalleryImage.display_order, GalleryImage.created_at.desc()).all()
    return images


@router.get("/{image_id}", response_model=GalleryImageResponse)
async def get_gallery_image(image_id: int, db: Session = Depends(get_db)):
    """Get a specific gallery image."""
    image = db.query(GalleryImage).filter(GalleryImage.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return image
