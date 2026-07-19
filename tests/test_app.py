import pytest
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Glasgow Roofmasters' in response.data

def test_about_page(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert b'About' in response.data

def test_services_page(client):
    response = client.get('/services')
    assert response.status_code == 200

def test_contact_page(client):
    response = client.get('/contact')
    assert response.status_code == 200

def test_404_page(client):
    response = client.get('/nonexistent')
    assert response.status_code == 404

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert b'healthy' in response.data

def test_inspection_form_validation(client):
    # Missing required fields
    response = client.post('/api/inspection-request', 
                          json={},
                          content_type='application/json')
    assert response.status_code == 400

    # Invalid email
    response = client.post('/api/inspection-request',
                          json={'name': 'Test', 'email': 'invalid', 'phone': '01412660600'},
                          content_type='application/json')
    assert response.status_code == 400

def test_contact_form(client):
    response = client.post('/api/contact',
                          json={'name': 'Test User', 'email': 'test@example.com', 'message': 'Hello'},
                          content_type='application/json')
    assert response.status_code == 200
    assert b'success' in response.data
