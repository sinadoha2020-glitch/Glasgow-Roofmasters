"""CMS setting schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CMSSettingBase(BaseModel):
    """Base CMS setting schema."""
    key: str = Field(..., min_length=1, max_length=100)
    value: str = Field(..., min_length=0)
    description: Optional[str] = Field(None, max_length=500)
    group: str = Field("general", max_length=50)


class CMSSettingCreate(CMSSettingBase):
    """Schema for creating a CMS setting."""
    pass


class CMSSettingUpdate(BaseModel):
    """Schema for updating a CMS setting."""
    value: str = Field(..., min_length=0)
    description: Optional[str] = Field(None, max_length=500)


class CMSSettingResponse(CMSSettingBase):
    """Schema for CMS setting response."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
