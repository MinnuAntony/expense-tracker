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
def test_add_expense(client):
    """Test the functionality of adding a new expense."""
    response = client.post('/add', data={
        'date': '2025-08-13',
        'description': 'Groceries',
        'amount': '50.50'
    }, follow_redirects=True)
    
    # Assert that the request redirects successfully and the new item is on the page
    assert response.status_code == 200
    assert b'Groceries' in response.data

# Test deleting an expense
def test_delete_expense(client):
    """Test the functionality of deleting an existing expense."""
    # Note: Since we are not testing the database, this test can't verify deletion.
    # It only checks for a successful redirect to the main page.
    # We will simulate a delete request for a hypothetical item with id 1.
    response = client.get('/delete/1', follow_redirects=True)
    
    # Assert that the request redirects successfully
    assert response.status_code == 200
    assert b'Expense Tracker' in response.data

# Test editing an expense
def test_edit_expense(client):
    """Test the functionality of editing an existing expense."""
    # Note: Since we are not testing the database, this test can't verify the update.
    # It only checks for a successful redirect to the main page.
    # We will simulate a POST request for a hypothetical item with id 1.
    response = client.post('/edit/1', data={
        'date': '2025-08-14',
        'description': 'Updated Description',
        'amount': '30.00'
    }, follow_redirects=True)
    
    # Assert that the request redirects successfully
    assert response.status_code == 200
    assert b'Updated Description' in response.data
