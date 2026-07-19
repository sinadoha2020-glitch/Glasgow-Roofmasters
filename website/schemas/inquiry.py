"""Inquiry schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator
import re


class InquiryBase(BaseModel):
    """Base inquiry schema."""
    name: str = Field(..., min_length=2, max_length=150, description="Full name")
    email: EmailStr = Field(..., description="Email address")
    phone: Optional[str] = Field(None, max_length=50, description="Phone number")
    service_type: Optional[str] = Field(None, max_length=100, description="Type of service needed")
    message: str = Field(..., min_length=10, max_length=5000, description="Message details")
    postcode: Optional[str] = Field(None, max_length=20, description="Postcode")

    @validator("phone")
    def validate_phone(cls, v):
        if v and not re.match(r"^[\d\s\+\-\(\)]{7,50}$", v):
            raise ValueError("Invalid phone number format")
        return v

    @validator("postcode")
    def validate_postcode(cls, v):
        if v and not re.match(r"^[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}$", v.upper().replace(" ", "")):
            # Allow any reasonable format for now, just clean it
            pass
        return v.upper().strip() if v else v


class InquiryCreate(InquiryBase):
    """Schema for creating a new inquiry."""
    pass


class InquiryResponse(InquiryBase):
    """Schema for inquiry response."""
    id: int
    is_read: bool
    is_responded: bool
    created_at: datetime

    class Config:
        from_attributes = True


class InquiryList(BaseModel):
    """Schema for paginated inquiry list."""
    items: list[InquiryResponse]
    total: int
    page: int
    per_page: int
