"""API routers."""
from app.routers.inquiry import router as inquiry_router
from app.routers.gallery import router as gallery_router
from app.routers.cms import router as cms_router
from app.routers.pages import router as pages_router

__all__ = ["inquiry_router", "gallery_router", "cms_router", "pages_router"]
