import pytest
from app import app

# Fixture to create a test client
@pytest.fixture(scope='session')
def client():
    # Set Flask to testing mode
    app.config['TESTING'] = True
    return app.test_client()

# Test the main page
def test_index_page_loads(client):
    """Test that the main page loads and contains the expected text."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Expense Tracker' in response.data

# Test adding a new expense
def test_add_expense_redirects_successfully(client):
    """Test that a POST to '/add' redirects to the index page."""
    response = client.post('/add', data={
        'date': '2025-08-13',
        'description': 'Groceries',
        'amount': '50.50'
    })
    
    # Assert that the request redirects successfully (status code 302 for redirect)
    assert response.status_code == 302
    assert response.location == '/'

# Test deleting an expense
def test_delete_expense_redirects_successfully(client):
    """Test that a GET to '/delete/<id>' redirects to the index page."""
    response = client.get('/delete/1')
    
    # Assert that the request redirects successfully
    assert response.status_code == 302
    assert response.location == '/'

# Test editing an expense
def test_edit_expense_redirects_successfully(client):
    """Test that a POST to '/edit/<id>' redirects to the index page."""
    response = client.post('/edit/1', data={
        'date': '2025-08-14',
        'description': 'Updated Description',
        'amount': '30.00'
    })
    
    # Assert that the request redirects successfully
    assert response.status_code == 302
    assert response.location == '/'
