"""Page rendering routes with Jinja2 templates."""
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.cms_service import CMSService
from app.models.gallery import GalleryImage

router = APIRouter()

# Common context builder
def get_base_context(request: Request, db: Session):
    """Build base template context with CMS settings."""
    contact = CMSService.get_settings_by_group(db, "contact")
    social = CMSService.get_settings_by_group(db, "social")
    seo = CMSService.get_settings_by_group(db, "seo")

    return {
        "request": request,
        "business_phone": contact.get("business_phone", "0141 266 0600"),
        "business_email": contact.get("business_email", "post@glasgowroofmasters.co.uk"),
        "business_address": contact.get("business_address", "236 Sauchiehall St, Glasgow G2 3HQ"),
        "business_hours": contact.get("business_hours", "Monday–Saturday 9am–6pm, closed Sunday"),
        "social": social,
        "seo": seo,
        "google_maps_embed": contact.get("google_maps_embed", ""),
    }


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    """Render homepage."""
    context = get_base_context(request, db)
    context["page_title"] = seo.get("meta_title_home", "Glasgow Roofmasters | Roofing Services Glasgow")
    context["meta_description"] = seo.get("meta_desc_home", "")
    context["canonical_url"] = str(request.url)

    # Get gallery preview images
    gallery_images = db.query(GalleryImage).filter(
        GalleryImage.is_active == True
    ).order_by(GalleryImage.display_order).limit(6).all()
    context["gallery_preview"] = gallery_images

    return request.app.state.templates.TemplateResponse("pages/home.html", context)


@router.get("/about", response_class=HTMLResponse)
async def about(request: Request, db: Session = Depends(get_db)):
    """Render about page."""
    context = get_base_context(request, db)
    context["page_title"] = seo.get("meta_title_about", "About Us | Glasgow Roofmasters")
    context["meta_description"] = seo.get("meta_desc_about", "")
    context["canonical_url"] = str(request.url).replace("/about", "/about")
    return request.app.state.templates.TemplateResponse("pages/about.html", context)


@router.get("/services", response_class=HTMLResponse)
async def services(request: Request, db: Session = Depends(get_db)):
    """Render services page."""
    context = get_base_context(request, db)
    context["page_title"] = seo.get("meta_title_services", "Our Services | Glasgow Roofmasters")
    context["meta_description"] = seo.get("meta_desc_services", "")
    context["canonical_url"] = str(request.url).replace("/services", "/services")
    return request.app.state.templates.TemplateResponse("pages/services.html", context)


@router.get("/pricing", response_class=HTMLResponse)
async def pricing(request: Request, db: Session = Depends(get_db)):
    """Render pricing page."""
    context = get_base_context(request, db)
    context["page_title"] = seo.get("meta_title_pricing", "Pricing | Glasgow Roofmasters")
    context["meta_description"] = seo.get("meta_desc_pricing", "")
    context["canonical_url"] = str(request.url).replace("/pricing", "/pricing")
    return request.app.state.templates.TemplateResponse("pages/pricing.html", context)


@router.get("/service-areas", response_class=HTMLResponse)
async def service_areas(request: Request, db: Session = Depends(get_db)):
    """Render service areas page."""
    context = get_base_context(request, db)
    context["page_title"] = seo.get("meta_title_areas", "Service Areas | Glasgow Roofmasters")
    context["meta_description"] = seo.get("meta_desc_areas", "")
    context["canonical_url"] = str(request.url).replace("/service-areas", "/service-areas")
    return request.app.state.templates.TemplateResponse("pages/service-areas.html", context)


@router.get("/gallery", response_class=HTMLResponse)
async def gallery(request: Request, db: Session = Depends(get_db)):
    """Render gallery page."""
    context = get_base_context(request, db)
    context["page_title"] = seo.get("meta_title_gallery", "Gallery | Glasgow Roofmasters")
    context["meta_description"] = seo.get("meta_desc_gallery", "")
    context["canonical_url"] = str(request.url).replace("/gallery", "/gallery")

    # Get all gallery images
    gallery_images = db.query(GalleryImage).filter(
        GalleryImage.is_active == True
    ).order_by(GalleryImage.display_order, GalleryImage.created_at.desc()).all()
    context["gallery_images"] = gallery_images

    return request.app.state.templates.TemplateResponse("pages/gallery.html", context)


@router.get("/faq", response_class=HTMLResponse)
async def faq(request: Request, db: Session = Depends(get_db)):
    """Render FAQ page."""
    context = get_base_context(request, db)
    context["page_title"] = seo.get("meta_title_faq", "FAQ | Glasgow Roofmasters")
    context["meta_description"] = seo.get("meta_desc_faq", "")
    context["canonical_url"] = str(request.url).replace("/faq", "/faq")
    return request.app.state.templates.TemplateResponse("pages/faq.html", context)


@router.get("/contact", response_class=HTMLResponse)
async def contact(request: Request, db: Session = Depends(get_db)):
    """Render contact page."""
    context = get_base_context(request, db)
    context["page_title"] = seo.get("meta_title_contact", "Contact | Glasgow Roofmasters")
    context["meta_description"] = seo.get("meta_desc_contact", "")
    context["canonical_url"] = str(request.url).replace("/contact", "/contact")
    return request.app.state.templates.TemplateResponse("pages/contact.html", context)


# Sitemap
@router.get("/sitemap.xml", response_class=HTMLResponse)
async def sitemap(request: Request):
    """Generate XML sitemap."""
    from datetime import datetime
    base_url = str(request.base_url).rstrip("/")

    pages = [
        {"url": f"{base_url}/", "priority": "1.0", "changefreq": "weekly"},
        {"url": f"{base_url}/about", "priority": "0.8", "changefreq": "monthly"},
        {"url": f"{base_url}/services", "priority": "0.9", "changefreq": "weekly"},
        {"url": f"{base_url}/pricing", "priority": "0.7", "changefreq": "monthly"},
        {"url": f"{base_url}/service-areas", "priority": "0.8", "changefreq": "monthly"},
        {"url": f"{base_url}/gallery", "priority": "0.6", "changefreq": "weekly"},
        {"url": f"{base_url}/faq", "priority": "0.6", "changefreq": "monthly"},
        {"url": f"{base_url}/contact", "priority": "0.9", "changefreq": "weekly"},
    ]

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""
    for page in pages:
        xml += f"""  <url>
    <loc>{page["url"]}</loc>
    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>
    <changefreq>{page["changefreq"]}</changefreq>
    <priority>{page["priority"]}</priority>
  </url>
"""
    xml += "</urlset>"

    return HTMLResponse(content=xml, media_type="application/xml")
