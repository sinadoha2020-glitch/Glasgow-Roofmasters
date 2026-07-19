from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime
import os
import re

app = Flask(__name__, 
                template_folder='website/templates',
                static_folder='website/static')

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:////tmp/roofmasters.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Mail config (configure with real credentials in production)
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', '')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'post@glasgowroofmasters.co.uk')

# Business Config (easily editable CMS-style fields)
BUSINESS_CONFIG = {
    'name': 'Glasgow Roofmasters',
    'address': '236 Sauchiehall St, Glasgow G2 3HQ',
    'phone': '0141 266 0600',
    'email': 'post@glasgowroofmasters.co.uk',
    'hours': {
        'monday': '9am – 6pm',
        'tuesday': '9am – 6pm',
        'wednesday': '9am – 6pm',
        'thursday': '9am – 6pm',
        'friday': '9am – 6pm',
        'saturday': '9am – 6pm',
        'sunday': 'Closed'
    },
    'social': {
        'facebook': 'https://facebook.com/glasgowroofmasters',
        'instagram': 'https://instagram.com/glasgowroofmasters',
        'linkedin': 'https://linkedin.com/company/glasgowroofmasters',
        'x': 'https://x.com/glasgowroofmasters',
        'pinterest': 'https://pinterest.com/glasgowroofmasters',
        'youtube': 'https://youtube.com/@glasgowroofmasters'
    },
    'google_maps_embed': 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d143447.8317175707!2d-4.372539903359426!3d55.85553669458642!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x4888469f07dd1d8d%3A0x626f0c950a2c6e2c!2sGlasgow%2C%20UK!5e0!3m2!1sen!2sus!4v1699999999999!5m2!1sen!2sus'
}

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Database Models
class InspectionRequest(db.Model):
    __tablename__ = 'inspection_requests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text)
    service_type = db.Column(db.String(50))
    status = db.Column(db.String(20), default='new')  # new, contacted, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'message': self.message,
            'service_type': self.service_type,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }

class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))

# Context processor for global template variables
@app.context_processor
def inject_business_config():
    return {
        'business': BUSINESS_CONFIG,
        'current_year': datetime.now().year
    }

# Routes
@app.route('/')
def home():
    return render_template('pages/home.html', 
                         title='Glasgow Roofmasters | Roofing Services Glasgow',
                         meta_desc='Professional roofing services in Glasgow. New roofs, repairs, restoration, emergency repairs & leadwork. Free inspection, pay on completion. Call 0141 266 0600.')

@app.route('/about')
def about():
    return render_template('pages/about.html',
                         title='About Us | Glasgow Roofmasters',
                         meta_desc='Learn about Glasgow Roofmasters, your trusted Glasgow roofing specialist. Free inspections, 5-year warranty, fully insured.')

@app.route('/services')
def services():
    return render_template('pages/services.html',
                         title='Our Services | Glasgow Roofmasters',
                         meta_desc='Complete roofing services in Glasgow: new roof installation, restoration, repairs, emergency repairs & leadwork. Free quotes.')

@app.route('/services/<service_slug>')
def service_detail(service_slug):
    services_data = {
        'new-roof': {
            'title': 'New Roof Installation Glasgow',
            'heading': 'New Roof Installation',
            'meta_desc': 'Expert new roof installation in Glasgow. Felt, EPDM rubber, fibreglass, tiles, slate & steel roofing. Free inspection & quote.',
            'materials': ['Felt Roofing', 'EPDM Rubber Roofing', 'Fibreglass Roofing', 'Concrete Tiles', 'Clay Tiles', 'Natural Slate', 'Steel Roofing']
        },
        'restoration': {
            'title': 'Roof Restoration Glasgow',
            'heading': 'Roof Restoration',
            'meta_desc': 'Professional roof restoration services in Glasgow. Extend your roof life by 10-20 years. Cost-effective alternative to replacement.',
            'benefits': ['Extends roof life by 10-20 years', 'More cost-effective than full replacement', 'Improves property value', 'Enhanced weather protection']
        },
        'repairs': {
            'title': 'Roof Repairs Glasgow',
            'heading': 'Roof Repairs',
            'meta_desc': 'Reliable roof repair services across Glasgow. Leaks, damaged tiles, guttering & more. Fast response, quality workmanship.',
            'types': ['Tile & Slate Replacement', 'Leak Detection & Repair', 'Guttering Repairs', 'Flat Roof Repairs', 'Chimney Repairs']
        },
        'emergency-repairs': {
            'title': 'Emergency Roof Repairs Glasgow',
            'heading': 'Emergency Repairs',
            'meta_desc': '24/7 emergency roof repairs in Glasgow. [EDIT: confirm with business] target response time. Storm damage, leaks & urgent issues.',
            'features': ['Rapid response team', 'Temporary weatherproofing', 'Permanent repair solutions', 'Insurance claim assistance']
        },
        'leadwork': {
            'title': 'Leadwork Specialists Glasgow',
            'heading': 'Leadwork',
            'meta_desc': 'Specialist leadwork services in Glasgow. Chimneys, flashing, valleys & custom leadwork by experienced craftsmen.',
            'applications': ['Chimney Flashing', 'Valley Gutters', 'Step Flashing', 'Lead Aprons', 'Custom Leadwork']
        }
    }
    service = services_data.get(service_slug)
    if not service:
        return render_template('pages/404.html'), 404
    return render_template('pages/service-detail.html',
                         title=service['title'],
                         meta_desc=service['meta_desc'],
                         service=service,
                         slug=service_slug)

@app.route('/pricing')
def pricing():
    return render_template('pages/pricing.html',
                         title='Pricing | Glasgow Roofmasters',
                         meta_desc='Transparent roofing pricing in Glasgow. Request a free, no-obligation inspection and quote for your roofing project.')

@app.route('/service-areas')
def service_areas():
    areas = [
        'Merchant City', 'West End', 'Partick', 'Dennistoun', 'Shawlands',
        'Castlemilk', 'Giffnock', 'Bishopbriggs', 'Cambuslang', 'Clydebank',
        'Cumbernauld', 'East Kilbride', 'Newton Mearns', 'Paisley'
    ]
    return render_template('pages/service-areas.html',
                         title='Service Areas | Glasgow Roofmasters',
                         meta_desc='Glasgow Roofmasters serves Glasgow city and surrounding areas including West End, East Kilbride, Paisley & more.',
                         areas=areas)

@app.route('/gallery')
def gallery():
    return render_template('pages/gallery.html',
                         title='Project Gallery | Glasgow Roofmasters',
                         meta_desc='View our roofing project gallery. [Placeholder images - real project photos pending]. Glasgow roofing specialists.')

@app.route('/faq')
def faq():
    return render_template('pages/faq.html',
                         title='FAQ | Glasgow Roofmasters',
                         meta_desc='Frequently asked questions about Glasgow Roofmasters roofing services, warranties, pricing & more.')

@app.route('/contact')
def contact():
    return render_template('pages/contact.html',
                         title='Contact Us | Glasgow Roofmasters',
                         meta_desc='Contact Glasgow Roofmasters for a free inspection. 236 Sauchiehall St, Glasgow. Call 0141 266 0600 or email us.')

# API Endpoints
@app.route('/api/inspection-request', methods=['POST'])
@limiter.limit("5 per minute")
def api_inspection_request():
    data = request.get_json()

    # Validation
    required = ['name', 'email', 'phone']
    for field in required:
        if not data.get(field):
            return jsonify({'success': False, 'error': f'{field.capitalize()} is required'}), 400

    # Email validation
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    if not email_pattern.match(data['email']):
        return jsonify({'success': False, 'error': 'Please enter a valid email address'}), 400

    # Phone validation (UK format)
    phone = re.sub(r'[\s\-\(\)]', '', data['phone'])
    if not re.match(r'^(\+44|0)[0-9]{9,10}$', phone):
        return jsonify({'success': False, 'error': 'Please enter a valid UK phone number'}), 400

    # Save to database
    request_obj = InspectionRequest(
        name=data['name'].strip(),
        email=data['email'].strip().lower(),
        phone=phone,
        message=data.get('message', '').strip(),
        service_type=data.get('service_type', ''),
        ip_address=request.remote_addr
    )
    db.session.add(request_obj)
    db.session.commit()

    # Send notification email (if configured)
    try:
        if app.config['MAIL_USERNAME']:
            msg = Message(
                'New Inspection Request - Glasgow Roofmasters',
                recipients=[BUSINESS_CONFIG['email']],
                body=f"""New inspection request received:

Name: {request_obj.name}
Email: {request_obj.email}
Phone: {request_obj.phone}
Service: {request_obj.service_type or 'Not specified'}
Message: {request_obj.message or 'None'}

View in admin panel."""
            )
            mail.send(msg)
    except Exception as e:
        app.logger.error(f"Failed to send email: {e}")

    return jsonify({
        'success': True,
        'message': 'Thank you! We will contact you within 24 hours to arrange your free inspection.',
        'request_id': request_obj.id
    })

@app.route('/api/contact', methods=['POST'])
@limiter.limit("5 per minute")
def api_contact():
    data = request.get_json()

    required = ['name', 'email', 'message']
    for field in required:
        if not data.get(field):
            return jsonify({'success': False, 'error': f'{field.capitalize()} is required'}), 400

    msg = ContactMessage(
        name=data['name'].strip(),
        email=data['email'].strip().lower(),
        phone=data.get('phone', '').strip(),
        subject=data.get('subject', '').strip(),
        message=data['message'].strip(),
        ip_address=request.remote_addr
    )
    db.session.add(msg)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Thank you for your message. We will respond as soon as possible.'
    })

# Admin routes (basic)
@app.route('/admin/requests')
def admin_requests():
    requests_list = InspectionRequest.query.order_by(InspectionRequest.created_at.desc()).all()
    return render_template('admin/requests.html', requests=requests_list)


@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'service': 'glasgow-roofmasters'}), 200

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return render_template('pages/404.html'), 404

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({'success': False, 'error': 'Rate limit exceeded. Please try again later.'}), 429

# Create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
