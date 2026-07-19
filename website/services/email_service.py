"""Email service for sending notifications."""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from app.core.config import get_settings

settings = get_settings()


class EmailService:
    """Handle email sending for inquiries and notifications."""

    @staticmethod
    def send_inquiry_notification(inquiry_data: dict) -> bool:
        """Send email notification when a new inquiry is received."""
        if not settings.SMTP_HOST or not settings.SMTP_USER:
            # Log that email would be sent but SMTP not configured
            print(f"[EMAIL] Would send inquiry notification for: {inquiry_data.get('email')}")
            return False

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"New Inspection Request - {inquiry_data.get('name', 'Unknown')}"
            msg["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
            msg["To"] = settings.SMTP_FROM_EMAIL

            # Plain text version
            text_body = f"""
New Free Inspection Request
===========================

Name: {inquiry_data.get('name')}
Email: {inquiry_data.get('email')}
Phone: {inquiry_data.get('phone', 'Not provided')}
Service: {inquiry_data.get('service_type', 'Not specified')}
Postcode: {inquiry_data.get('postcode', 'Not provided')}

Message:
{inquiry_data.get('message')}

---
Submitted at: {inquiry_data.get('created_at', 'Now')}
            """.strip()

            # HTML version
            html_body = f"""
<!DOCTYPE html>
<html>
<head><style>body{{font-family:Arial,sans-serif;line-height:1.6;color:#333;}}.header{{background:#1B3A57;color:#fff;padding:20px;}}.content{{padding:20px;}}.field{{margin-bottom:15px;}}.label{{font-weight:bold;color:#1B3A57;}}</style></head>
<body>
<div class="header"><h1>New Inspection Request</h1></div>
<div class="content">
<div class="field"><span class="label">Name:</span> {inquiry_data.get('name')}</div>
<div class="field"><span class="label">Email:</span> {inquiry_data.get('email')}</div>
<div class="field"><span class="label">Phone:</span> {inquiry_data.get('phone', 'Not provided')}</div>
<div class="field"><span class="label">Service:</span> {inquiry_data.get('service_type', 'Not specified')}</div>
<div class="field"><span class="label">Postcode:</span> {inquiry_data.get('postcode', 'Not provided')}</div>
<div class="field"><span class="label">Message:</span><br/>{inquiry_data.get('message', '').replace(chr(10), '<br/>')}</div>
</div>
</body>
</html>
            """.strip()

            msg.attach(MIMEText(text_body, "plain"))
            msg.attach(MIMEText(html_body, "html"))

            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)

            return True
        except Exception as e:
            print(f"[EMAIL ERROR] Failed to send email: {e}")
            return False

    @staticmethod
    def send_confirmation_email(to_email: str, name: str) -> bool:
        """Send confirmation email to the customer."""
        if not settings.SMTP_HOST or not settings.SMTP_USER:
            print(f"[EMAIL] Would send confirmation to: {to_email}")
            return False

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = "Your Free Roof Inspection Request - Glasgow Roofmasters"
            msg["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
            msg["To"] = to_email

            html_body = f"""
<!DOCTYPE html>
<html>
<head><style>body{{font-family:Arial,sans-serif;line-height:1.6;color:#333;}}.header{{background:#1B3A57;color:#fff;padding:30px;text-align:center;}}.content{{padding:30px;max-width:600px;margin:0 auto;}}.cta{{background:#E8593A;color:#fff;padding:15px 30px;text-decoration:none;border-radius:4px;display:inline-block;margin:20px 0;}}.footer{{background:#F7F8FA;padding:20px;text-align:center;color:#5C6670;font-size:14px;}}</style></head>
<body>
<div class="header"><h1>Glasgow Roofmasters</h1><p>Your Request Has Been Received</p></div>
<div class="content">
<p>Hi {name},</p>
<p>Thank you for requesting a free, no-obligation roof inspection. We have received your details and will be in touch shortly to arrange a convenient time.</p>
<p><strong>What happens next?</strong></p>
<ul>
<li>We will call you within 24 hours to schedule your inspection</li>
<li>A qualified roofing specialist will visit your property</li>
<li>You will receive a detailed assessment with no obligation</li>
<li>You only pay once work is completed as agreed</li>
</ul>
<p>If you need to speak to us urgently, please call <strong>0141 266 0600</strong>.</p>
</div>
<div class="footer">
<p>Glasgow Roofmasters<br/>236 Sauchiehall St, Glasgow G2 3HQ<br/>0141 266 0600 | post@glasgowroofmasters.co.uk</p>
</div>
</body>
</html>
            """.strip()

            msg.attach(MIMEText(html_body, "html"))

            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)

            return True
        except Exception as e:
            print(f"[EMAIL ERROR] Failed to send confirmation: {e}")
            return False
