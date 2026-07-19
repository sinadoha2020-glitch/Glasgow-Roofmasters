"""Pydantic schemas for request/response validation."""
from app.schemas.inquiry import InquiryCreate, InquiryResponse, InquiryList
from app.schemas.gallery import GalleryImageCreate, GalleryImageResponse
from app.schemas.cms import CMSSettingCreate, CMSSettingResponse, CMSSettingUpdate

__all__ = [
    "InquiryCreate", "InquiryResponse", "InquiryList",
    "GalleryImageCreate", "GalleryImageResponse",
    "CMSSettingCreate", "CMSSettingResponse", "CMSSettingUpdate",
]
