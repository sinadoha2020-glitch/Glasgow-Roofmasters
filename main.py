"""Glasgow Roofmasters - Full Stack Web Application.

FastAPI backend with Jinja2 templating, SQLite database, and full CMS functionality.
"""
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware

from app.core.config import get_settings, BASE_DIR
from app.core.database import engine, Base
from app.routers import inquiry_router, gallery_router, cms_router, pages_router
from app.services.cms_service import CMSService

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    Base.metadata.create_all(bind=engine)

    # Initialize CMS defaults
    from app.core.database import SessionLocal
    db = SessionLocal()
    try:
        CMSService.initialize_defaults(db)
    finally:
        db.close()

    yield

    # Shutdown
    pass


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Professional roofing services in Glasgow, Scotland",
    lifespan=lifespan,
)

# Session middleware for flash messages
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    max_age=3600,
)

# Static files
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "app" / "static")), name="static")

# Templates
templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))
app.state.templates = templates

# Custom Jinja2 filters
from markupsafe import Markup


def nl2br(value):
    """Convert newlines to <br> tags."""
    if not value:
        return ""
    return Markup(value.replace("\n", "<br>"))


def phone_link(value):
    """Format phone number as tel: link."""
    if not value:
        return ""
    clean = value.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    return f"tel:{clean}"


templates.env.filters["nl2br"] = nl2br
templates.env.filters["phone_link"] = phone_link

# Include routers
app.include_router(pages_router)
app.include_router(inquiry_router)
app.include_router(gallery_router)
app.include_router(cms_router)


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Custom 404 handler."""
    if request.url.path.startswith("/api/"):
        return JSONResponse(status_code=404, content={"detail": "Not found"})
    return templates.TemplateResponse(
        "pages/404.html",
        {"request": request, "page_title": "Page Not Found | Glasgow Roofmasters"},
        status_code=404
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": settings.APP_VERSION}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
