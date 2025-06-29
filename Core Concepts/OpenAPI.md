# Python/Swagger Integration with Authentication: A Comprehensive Guide

## Understanding Swagger (OpenAPI) and Python Integration

Swagger (now known as OpenAPI) is a specification for building and documenting RESTful APIs. When integrated with Python, it provides a powerful way to create, document, and consume APIs with clear contracts.

### Key Benefits:
- **API Documentation**: Automatic generation of interactive API documentation
- **Client SDK Generation**: Create client libraries in multiple languages
- **Server Stub Generation**: Generate server boilerplate code
- **Validation**: Ensure API requests/responses conform to the specification

## Authentication Methods in Swagger/OpenAPI

Swagger supports several authentication mechanisms:

1. **API Key Authentication**
   - Passed in headers, query parameters, or cookies
   - Simple but less secure than other methods

2. **OAuth 2.0**
   - Industry-standard protocol for authorization
   - Supports flows like authorization code, implicit, client credentials

3. **Bearer Token (JWT)**
   - Commonly used with token-based authentication
   - Tokens are passed in the Authorization header

4. **Basic Authentication**
   - Username and password passed in the Authorization header
   - Should only be used with HTTPS

## Real-World Example: Python Flask API with Swagger and JWT Authentication

Let's create a complete example with:
1. A Python Flask API with Swagger documentation
2. JWT authentication
3. Protected and unprotected endpoints

### Step 1: Setup Dependencies

```bash
pip install flask flask-restx python-dotenv pyjwt
```

### Step 2: Project Structure

```
my_api/
├── app.py                # Main application
├── auth.py               # Authentication logic
├── requirements.txt      # Dependencies
└── .env                  # Environment variables
```

### Step 3: Implementation

**app.py**

```python
from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
api = Api(app, version='1.0', title='Sample API', description='A sample API with JWT authentication')

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Namespace for our API
ns = api.namespace('api', description='Main API operations')

# Model for user registration/login
user_model = api.model('User', {
    'username': fields.String(required=True, description='The user username'),
    'password': fields.String(required=True, description='The user password')
})

# Model for protected data
data_model = api.model('ProtectedData', {
    'data': fields.String(required=True, description='Some protected data'),
    'user': fields.String(description='Username of the authenticated user')
})

# Mock database
users_db = {
    'admin': {
        'username': 'admin',
        'password': generate_password_hash('admin123'),
        'role': 'admin'
    }
}

# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check if token is in the header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return {'message': 'Token is missing'}, 401
        
        try:
            # Decode the token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = users_db.get(data['username'])
        except:
            return {'message': 'Token is invalid or expired'}, 401
        
        return f(current_user, *args, **kwargs)
    return decorated

@ns.route('/register')
class Register(Resource):
    @api.expect(user_model)
    def post(self):
        """Register a new user"""
        data = api.payload
        username = data['username']
        password = data['password']
        
        if username in users_db:
            return {'message': 'User already exists'}, 400
            
        users_db[username] = {
            'username': username,
            'password': generate_password_hash(password),
            'role': 'user'
        }
        
        return {'message': 'User created successfully'}, 201

@ns.route('/login')
class Login(Resource):
    @api.expect(user_model)
    def post(self):
        """Login and get JWT token"""
        data = api.payload
        username = data['username']
        password = data['password']
        
        user = users_db.get(username)
        
        if not user or not check_password_hash(user['password'], password):
            return {'message': 'Invalid credentials'}, 401
            
        # Create JWT token
        token = jwt.encode({
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, app.config['SECRET_KEY'])
        
        return {'token': token}, 200

@ns.route('/protected')
class Protected(Resource):
    @api.doc(security=['Bearer'])
    @api.marshal_with(data_model)
    @token_required
    def get(self, current_user):
        """Access protected data (requires authentication)"""
        return {
            'data': 'This is protected data',
            'user': current_user['username']
        }, 200

@ns.route('/public')
class Public(Resource):
    def get(self):
        """Access public data (no authentication required)"""
        return {'data': 'This is public data'}, 200

if __name__ == '__main__':
    app.run(debug=True)
```

**auth.py** (Optional - for more complex auth scenarios)

```python
from functools import wraps
from flask import request, jsonify
import jwt
from .app import app

def admin_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user['role'] != 'admin':
            return {'message': 'Admin access required'}, 403
        return f(current_user, *args, **kwargs)
    return decorated
```

### Step 4: Environment Variables (.env)

```
SECRET_KEY=your-very-secret-key-123
```

### Step 5: Running the Application

```bash
python app.py
```

## Testing the API with Swagger UI

1. Access the Swagger UI at `http://localhost:5000`
2. You'll see all endpoints documented with their models and requirements

### Testing Flow:

1. **Register a new user**:
   - POST to `/api/register` with `{"username": "newuser", "password": "password123"}`

2. **Login to get JWT token**:
   - POST to `/api/login` with the same credentials
   - Copy the token from the response

3. **Access protected endpoint**:
   - Click "Authorize" button in Swagger UI
   - Enter "Bearer <your-token>"
   - Now you can access `/api/protected`

4. **Access public endpoint**:
   - `/api/public` is accessible without authentication

## Real-World Enhancements

1. **Database Integration**:
   - Replace the mock database with a real database like PostgreSQL or MongoDB

2. **Token Refresh**:
   - Implement a refresh token mechanism for longer sessions

3. **Rate Limiting**:
   - Add rate limiting to prevent abuse

4. **Input Validation**:
   - Enhance validation beyond what Swagger provides

5. **Logging**:
   - Add comprehensive logging for security and debugging

## Client-Side Usage Example

Here's how you would use this API from a Python client:

```python
import requests

BASE_URL = "http://localhost:5000/api"

# 1. Register (only needed once)
register_data = {"username": "testuser", "password": "testpass"}
response = requests.post(f"{BASE_URL}/register", json=register_data)
print("Register:", response.json())

# 2. Login
login_data = {"username": "testuser", "password": "testpass"}
response = requests.post(f"{BASE_URL}/login", json=login_data)
token = response.json().get('token')
print("Login:", token)

# 3. Access protected endpoint
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(f"{BASE_URL}/protected", headers=headers)
print("Protected:", response.json())

# 4. Access public endpoint
response = requests.get(f"{BASE_URL}/public")
print("Public:", response.json())
```

## Security Best Practices

1. **Always use HTTPS** in production
2. **Set appropriate token expiration times** (shorter is generally better)
3. **Store secrets securely** (environment variables, secret managers)
4. **Implement proper password hashing** (like bcrypt)
5. **Add rate limiting** to prevent brute force attacks
6. **Use secure flags** for cookies if using them
7. **Regularly rotate secrets** and revoke compromised tokens

This example provides a complete, real-world implementation of a Python API with Swagger documentation and JWT authentication that you can extend for your specific needs.