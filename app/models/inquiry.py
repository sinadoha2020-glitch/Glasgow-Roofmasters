"""Inquiry/Contact form submission model."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from app.core.database import Base


class Inquiry(Base):
    """Store free inspection requests and contact form submissions."""

    __tablename__ = "inquiries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    service_type = Column(String(100), nullable=True)
    message = Column(Text, nullable=False)
    postcode = Column(String(20), nullable=True)

    # Status tracking
    is_read = Column(Boolean, default=False)
    is_responded = Column(Boolean, default=False)

    # Metadata
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Inquiry(id={self.id}, name={self.name}, email={self.email})>"
