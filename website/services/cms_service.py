"""CMS service for managing editable content."""
from typing import Optional, Dict, List
from sqlalchemy.orm import Session
from app.models.cms import CMSSetting
from app.schemas.cms import CMSSettingCreate, CMSSettingUpdate


class CMSService:
    """Service for managing CMS settings."""

    DEFAULT_SETTINGS = {
        # Contact info
        "business_phone": {"value": "0141 266 0600", "group": "contact", "description": "Main business phone number"},
        "business_email": {"value": "post@glasgowroofmasters.co.uk", "group": "contact", "description": "Business email address"},
        "business_address": {"value": "236 Sauchiehall St, Glasgow G2 3HQ", "group": "contact", "description": "Business address"},
        "business_hours": {"value": "Monday–Saturday 9am–6pm, closed Sunday", "group": "contact", "description": "Opening hours"},

        # Social links
        "social_facebook": {"value": "https://facebook.com/glasgowroofmasters", "group": "social", "description": "Facebook page URL"},
        "social_instagram": {"value": "https://instagram.com/glasgowroofmasters", "group": "social", "description": "Instagram profile URL"},
        "social_linkedin": {"value": "https://linkedin.com/company/glasgowroofmasters", "group": "social", "description": "LinkedIn company URL"},
        "social_x": {"value": "https://x.com/glasgowroofmasters", "group": "social", "description": "X (Twitter) profile URL"},
        "social_pinterest": {"value": "https://pinterest.com/glasgowroofmasters", "group": "social", "description": "Pinterest profile URL"},
        "social_youtube": {"value": "https://youtube.com/@glasgowroofmasters", "group": "social", "description": "YouTube channel URL"},

        # SEO
        "meta_title_home": {"value": "Glasgow Roofmasters | Roofing Services Glasgow | Free Inspection", "group": "seo", "description": "Homepage meta title"},
        "meta_desc_home": {"value": "Professional roofing services in Glasgow. New roofs, restoration, repairs, emergency repairs & leadwork. Free inspection, pay on completion. 5-year warranty.", "group": "seo", "description": "Homepage meta description"},
        "meta_title_about": {"value": "About Us | Glasgow Roofmasters | Glasgow Roofing Specialists", "group": "seo", "description": "About page meta title"},
        "meta_desc_about": {"value": "Learn about Glasgow Roofmasters, Glasgow's trusted roofing company. Serving Glasgow and surrounding areas with quality roofing services.", "group": "seo", "description": "About page meta description"},
        "meta_title_services": {"value": "Our Services | Glasgow Roofmasters | New Roofs, Repairs & Leadwork", "group": "seo", "description": "Services page meta title"},
        "meta_desc_services": {"value": "Full range of roofing services in Glasgow: new roof installation, restoration, repairs, emergency repairs and leadwork. Free inspection available.", "group": "seo", "description": "Services page meta description"},
        "meta_title_pricing": {"value": "Pricing | Glasgow Roofmasters | Competitive Roofing Quotes", "group": "seo", "description": "Pricing page meta title"},
        "meta_desc_pricing": {"value": "Transparent pricing for roofing services in Glasgow. Request a free, no-obligation inspection and quote for your roofing project.", "group": "seo", "description": "Pricing page meta description"},
        "meta_title_areas": {"value": "Service Areas | Glasgow Roofmasters | Glasgow & Surrounding Areas", "group": "seo", "description": "Service areas page meta title"},
        "meta_desc_areas": {"value": "Glasgow Roofmasters serves Glasgow city and surrounding areas including West End, Partick, Shawlands, East Kilbride, Paisley and more.", "group": "seo", "description": "Service areas page meta description"},
        "meta_title_gallery": {"value": "Gallery | Glasgow Roofmasters | Roofing Project Photos", "group": "seo", "description": "Gallery page meta title"},
        "meta_desc_gallery": {"value": "View our roofing project gallery. New roofs, restorations, repairs and leadwork projects across Glasgow and surrounding areas.", "group": "seo", "description": "Gallery page meta description"},
        "meta_title_faq": {"value": "FAQ | Glasgow Roofmasters | Roofing Questions Answered", "group": "seo", "description": "FAQ page meta title"},
        "meta_desc_faq": {"value": "Frequently asked questions about roofing services in Glasgow. Free inspection, warranties, materials and more.", "group": "seo", "description": "FAQ page meta description"},
        "meta_title_contact": {"value": "Contact | Glasgow Roofmasters | Free Roof Inspection", "group": "seo", "description": "Contact page meta title"},
        "meta_desc_contact": {"value": "Contact Glasgow Roofmasters for a free roof inspection. Call 0141 266 0600 or fill in our online form. Serving Glasgow and surrounding areas.", "group": "seo", "description": "Contact page meta description"},

        # Google Maps
        "google_maps_embed": {"value": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d143447.8317175707!2d-4.372539903125!3d55.86098249999999!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x4888152c3c7c8b0f%3A0x4c8f0c4c4c4c4c4c!2s236%20Sauchiehall%20St%2C%20Glasgow%20G2%203HQ!5e0!3m2!1sen!2suk!4v1700000000000!5m2!1sen!2suk", "group": "contact", "description": "Google Maps embed URL"},
    }

    @staticmethod
    def initialize_defaults(db: Session) -> None:
        """Initialize default CMS settings if they don't exist."""
        for key, data in CMSService.DEFAULT_SETTINGS.items():
            existing = db.query(CMSSetting).filter(CMSSetting.key == key).first()
            if not existing:
                setting = CMSSetting(
                    key=key,
                    value=data["value"],
                    description=data.get("description"),
                    group=data.get("group", "general")
                )
                db.add(setting)
        db.commit()

    @staticmethod
    def get_setting(db: Session, key: str) -> Optional[str]:
        """Get a single setting value by key."""
        setting = db.query(CMSSetting).filter(CMSSetting.key == key).first()
        return setting.value if setting else None

    @staticmethod
    def get_settings_by_group(db: Session, group: str) -> Dict[str, str]:
        """Get all settings in a group as a dictionary."""
        settings = db.query(CMSSetting).filter(CMSSetting.group == group).all()
        return {s.key: s.value for s in settings}

    @staticmethod
    def get_all_settings(db: Session) -> Dict[str, Dict[str, str]]:
        """Get all settings organized by group."""
        settings = db.query(CMSSetting).all()
        result = {}
        for s in settings:
            if s.group not in result:
                result[s.group] = {}
            result[s.group][s.key] = s.value
        return result

    @staticmethod
    def update_setting(db: Session, key: str, value: str) -> Optional[CMSSetting]:
        """Update a setting value."""
        setting = db.query(CMSSetting).filter(CMSSetting.key == key).first()
        if setting:
            setting.value = value
            db.commit()
            db.refresh(setting)
        return setting
