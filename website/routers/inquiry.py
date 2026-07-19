"""Inquiry API routes."""
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.inquiry import Inquiry
from app.schemas.inquiry import InquiryCreate, InquiryResponse
from app.services.email_service import EmailService

router = APIRouter(prefix="/api/inquiries", tags=["inquiries"])


@router.post("/", response_model=InquiryResponse, status_code=status.HTTP_201_CREATED)
async def create_inquiry(
    inquiry: InquiryCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """Submit a new free inspection request."""
    db_inquiry = Inquiry(
        name=inquiry.name,
        email=inquiry.email,
        phone=inquiry.phone,
        service_type=inquiry.service_type,
        message=inquiry.message,
        postcode=inquiry.postcode,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent")
    )
    db.add(db_inquiry)
    db.commit()
    db.refresh(db_inquiry)

    # Send notification emails (non-blocking, fire-and-forget)
    inquiry_dict = {
        "name": inquiry.name,
        "email": inquiry.email,
        "phone": inquiry.phone,
        "service_type": inquiry.service_type,
        "message": inquiry.message,
        "postcode": inquiry.postcode,
        "created_at": str(db_inquiry.created_at)
    }

    # Try to send emails but don't fail the request if email fails
    try:
        EmailService.send_inquiry_notification(inquiry_dict)
        EmailService.send_confirmation_email(inquiry.email, inquiry.name)
    except Exception:
        pass  # Logged in service

    return db_inquiry


@router.get("/", response_model=List[InquiryResponse])
async def list_inquiries(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all inquiries (admin endpoint - would need auth in production)."""
    inquiries = db.query(Inquiry).order_by(Inquiry.created_at.desc()).offset(skip).limit(limit).all()
    return inquiries


@router.get("/{inquiry_id}", response_model=InquiryResponse)
async def get_inquiry(inquiry_id: int, db: Session = Depends(get_db)):
    """Get a specific inquiry by ID."""
    inquiry = db.query(Inquiry).filter(Inquiry.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    return inquiry
