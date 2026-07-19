"""CMS API routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict
from app.core.database import get_db
from app.services.cms_service import CMSService

router = APIRouter(prefix="/api/cms", tags=["cms"])


@router.get("/settings")
async def get_all_settings(db: Session = Depends(get_db)):
    """Get all CMS settings organized by group."""
    return CMSService.get_all_settings(db)


@router.get("/settings/{group}")
async def get_settings_by_group(group: str, db: Session = Depends(get_db)):
    """Get settings for a specific group."""
    return CMSService.get_settings_by_group(db, group)


@router.get("/setting/{key}")
async def get_setting(key: str, db: Session = Depends(get_db)):
    """Get a single setting value."""
    value = CMSService.get_setting(db, key)
    if value is None:
        raise HTTPException(status_code=404, detail="Setting not found")
    return {"key": key, "value": value}


@router.put("/setting/{key}")
async def update_setting(key: str, value: str, db: Session = Depends(get_db)):
    """Update a setting value."""
    setting = CMSService.update_setting(db, key, value)
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    return {"key": key, "value": setting.value, "updated": True}
