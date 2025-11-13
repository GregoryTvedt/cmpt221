# TODO: add five more unit test cases

def test_home_page(client):
    """Test that home page loads"""
    response = client.get('/')
    assert response.status_code == 200

def test_login_page(client):
    """Test that home page loads"""
    response = client.get('/login')
    assert response.status_code == 200

def test_users_page(client):
    """Test that users page loads"""
    response = client.get('/users')
    assert response.status_code == 200

def test_invalid_first_name(client):
    """Test signup validation for invalid first name"""
    response = client.post('/signup', data={
        'FirstName': '123',  # invalid - contains numbers
        'LastName': 'Doe',
        'Email': 'test@test.com',
        'PhoneNumber': '1234567890',
        'Password': 'password123'
    })
    assert b'First name can only contain letters' in response.data

def test_invalid_phone_number(client):
    """Test signup validation for invalid phone number"""
    response = client.post('/signup', data={
        'FirstName': 'John',
        'LastName': 'Doe',
        'Email': 'test@test.com',
        'PhoneNumber': '123',  # invalid - not 10 digits
        'Password': 'password123'
    })
    assert b'Phone number must be exactly 10 digits' in response.data

def test_invalid_lastname(client):
    """Test signup validation for invalid last name"""
    response = client.post('/signup', data={
        'FirstName': 'John',
        'LastName': '123', # invalid - contains numbers
        'Email': 'test@test.com',
        'PhoneNumber': '1234567890',
        'Password': 'password123'
    })
    assert b'Last name can only contain letters' in response.data

def test_incorrect_password(client):
    """Test wrong password for a given user"""
    response = client.get('/users')

    if b'test2@test2.com' not in response.data:
        client.post('/signup', data={
        'FirstName': 'John',
        'LastName': 'Doe',
        'Email': 'test2@test2.com',
        'PhoneNumber': '1234567890',
        'Password': 'password123'
    })

    response = client.post('/login', data={
        'Email': 'test2@test2.com',
        'Password': 'password124' # invalid - password is not the same as user
    })
    assert b'Failed login attempt' in response.data

def test_nonexistent_email(client):
    """Test login validation for nonexistent email"""
    response = client.post('/login', data={
        'Email': 'test3@test3.com', # invalid - email does not exist in database
        'Password': 'password12'
    })
    assert b'Failed login attempt' in response.data

def test_successful_login(client):
    """Test login validation for a successful user login"""
    response = client.get('/users')

    if b'test4@test4.com' not in response.data:
        client.post('/signup', data={
        'FirstName': 'John',
        'LastName': 'Doe',
        'Email': 'test4@test4.com',
        'PhoneNumber': '1234567890',
        'Password': 'password123'
    })
    
    response = client.post('/login', data={
        'Email': 'test4@test4.com',
        'Password': 'password123'
    })
    assert b'success' in response.data

def test_empty_field(client):
    """Test an empty field for a user login"""
    response = client.post('/signup', data={
        'FirstName': '',
        'LastName': 'Doe',
        'Email':'test5@test5.com',
        'PhoneNumber': '1234567890',
        'Password': 'password123'
    })
    assert b'First name can only contain letters' in response.data