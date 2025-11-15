"""
API Authentication Module for FRAMS

Provides JWT and API Key authentication for securing endpoints.

Usage:
    from auth import require_auth, require_api_key, create_token

    @app.route('/api/protected')
    @require_auth
    def protected_route():
        return jsonify({'message': 'Authenticated!'})
"""

import jwt
import secrets
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
import sqlite3
import hashlib

# Configuration
JWT_SECRET_KEY = secrets.token_hex(32)  # Change in production
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24

# Database
AUTH_DB = 'information.db'


def init_auth_database():
    """Initialize authentication tables"""
    conn = sqlite3.connect(AUTH_DB)

    # Users table
    conn.execute('''CREATE TABLE IF NOT EXISTS Users
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                     Username TEXT UNIQUE NOT NULL,
                     PasswordHash TEXT NOT NULL,
                     Role TEXT DEFAULT 'user',
                     CreatedAt TEXT NOT NULL)''')

    # API Keys table
    conn.execute('''CREATE TABLE IF NOT EXISTS ApiKeys
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                     KeyName TEXT NOT NULL,
                     ApiKey TEXT UNIQUE NOT NULL,
                     UserId INTEGER,
                     Active INTEGER DEFAULT 1,
                     CreatedAt TEXT NOT NULL,
                     FOREIGN KEY (UserId) REFERENCES Users(ID))''')

    # Create default admin user if not exists
    cursor = conn.execute("SELECT COUNT(*) FROM Users WHERE Username='admin'")
    if cursor.fetchone()[0] == 0:
        password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
        conn.execute(
            "INSERT INTO Users (Username, PasswordHash, Role, CreatedAt) VALUES (?, ?, ?, ?)",
            ('admin', password_hash, 'admin', datetime.now().isoformat())
        )

    conn.commit()
    conn.close()


# Initialize on import
init_auth_database()


def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against hash"""
    return hash_password(password) == password_hash


def create_token(username: str, role: str = 'user') -> str:
    """
    Create JWT token

    Args:
        username: Username
        role: User role (admin/user)

    Returns:
        JWT token string
    """
    payload = {
        'username': username,
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }

    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def decode_token(token: str) -> dict:
    """
    Decode and verify JWT token

    Args:
        token: JWT token

    Returns:
        Decoded payload

    Raises:
        jwt.ExpiredSignatureError: Token expired
        jwt.InvalidTokenError: Invalid token
    """
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    return payload


def generate_api_key() -> str:
    """Generate random API key"""
    return 'frams_' + secrets.token_urlsafe(32)


def create_api_key(key_name: str, user_id: int = None) -> str:
    """
    Create new API key

    Args:
        key_name: Name/description for the key
        user_id: User ID (optional)

    Returns:
        API key string
    """
    api_key = generate_api_key()

    conn = sqlite3.connect(AUTH_DB)
    conn.execute(
        "INSERT INTO ApiKeys (KeyName, ApiKey, UserId, CreatedAt) VALUES (?, ?, ?, ?)",
        (key_name, api_key, user_id, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

    return api_key


def verify_api_key(api_key: str) -> bool:
    """
    Verify API key is valid and active

    Args:
        api_key: API key to verify

    Returns:
        True if valid, False otherwise
    """
    conn = sqlite3.connect(AUTH_DB)
    cursor = conn.execute(
        "SELECT Active FROM ApiKeys WHERE ApiKey=?",
        (api_key,)
    )
    row = cursor.fetchone()
    conn.close()

    return row is not None and row[0] == 1


def get_token_from_request():
    """Extract token from request headers"""
    auth_header = request.headers.get('Authorization')

    if auth_header and auth_header.startswith('Bearer '):
        return auth_header.split(' ')[1]

    return None


def get_api_key_from_request():
    """Extract API key from request headers or query params"""
    # Check header
    api_key = request.headers.get('X-API-Key')
    if api_key:
        return api_key

    # Check query parameter
    api_key = request.args.get('api_key')
    if api_key:
        return api_key

    return None


def require_auth(f):
    """
    Decorator to require JWT authentication

    Usage:
        @app.route('/api/protected')
        @require_auth
        def protected():
            return jsonify({'message': 'OK'})
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = get_token_from_request()

        if not token:
            return jsonify({'error': 'Missing authentication token'}), 401

        try:
            payload = decode_token(token)
            request.user = payload
            return f(*args, **kwargs)

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401

        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

    return decorated_function


def require_api_key(f):
    """
    Decorator to require API key authentication

    Usage:
        @app.route('/api/data')
        @require_api_key
        def get_data():
            return jsonify({'data': [...]})
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = get_api_key_from_request()

        if not api_key:
            return jsonify({'error': 'Missing API key'}), 401

        if not verify_api_key(api_key):
            return jsonify({'error': 'Invalid API key'}), 401

        return f(*args, **kwargs)

    return decorated_function


def require_role(role: str):
    """
    Decorator to require specific role

    Usage:
        @app.route('/api/admin')
        @require_auth
        @require_role('admin')
        def admin_only():
            return jsonify({'message': 'Admin access'})
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(request, 'user'):
                return jsonify({'error': 'Authentication required'}), 401

            if request.user.get('role') != role:
                return jsonify({'error': 'Insufficient permissions'}), 403

            return f(*args, **kwargs)

        return decorated_function

    return decorator


# Example authentication endpoints
def setup_auth_routes(app):
    """
    Setup authentication routes

    Call this from your main app:
        from auth import setup_auth_routes
        setup_auth_routes(app)
    """

    @app.route('/api/auth/login', methods=['POST'])
    def login():
        """Login endpoint - returns JWT token"""
        data = request.get_json()

        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Missing username or password'}), 400

        username = data['username']
        password = data['password']

        conn = sqlite3.connect(AUTH_DB)
        cursor = conn.execute(
            "SELECT PasswordHash, Role FROM Users WHERE Username=?",
            (username,)
        )
        row = cursor.fetchone()
        conn.close()

        if not row:
            return jsonify({'error': 'Invalid credentials'}), 401

        password_hash, role = row

        if not verify_password(password, password_hash):
            return jsonify({'error': 'Invalid credentials'}), 401

        token = create_token(username, role)

        return jsonify({
            'success': True,
            'token': token,
            'username': username,
            'role': role,
            'expires_in': JWT_EXPIRATION_HOURS * 3600
        })

    @app.route('/api/auth/register', methods=['POST'])
    def register():
        """Register new user"""
        data = request.get_json()

        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Missing username or password'}), 400

        username = data['username']
        password = data['password']
        role = data.get('role', 'user')

        if role not in ['user', 'admin']:
            return jsonify({'error': 'Invalid role'}), 400

        password_hash = hash_password(password)

        try:
            conn = sqlite3.connect(AUTH_DB)
            conn.execute(
                "INSERT INTO Users (Username, PasswordHash, Role, CreatedAt) VALUES (?, ?, ?, ?)",
                (username, password_hash, role, datetime.now().isoformat())
            )
            conn.commit()
            conn.close()

            return jsonify({
                'success': True,
                'message': 'User registered successfully',
                'username': username
            }), 201

        except sqlite3.IntegrityError:
            return jsonify({'error': 'Username already exists'}), 409

    @app.route('/api/auth/api-key', methods=['POST'])
    @require_auth
    def create_new_api_key():
        """Create new API key (requires authentication)"""
        data = request.get_json() or {}
        key_name = data.get('name', 'API Key')

        api_key = create_api_key(key_name)

        return jsonify({
            'success': True,
            'api_key': api_key,
            'message': 'API key created successfully',
            'usage': 'Add header: X-API-Key: {api_key}'
        }), 201

    @app.route('/api/auth/verify', methods=['GET'])
    @require_auth
    def verify_token_endpoint():
        """Verify token is valid"""
        return jsonify({
            'success': True,
            'user': request.user
        })


if __name__ == '__main__':
    # Example usage
    print("🔐 FRAMS Authentication Module")
    print("=" * 60)

    # Create API key
    api_key = create_api_key('Test Key')
    print(f"\n✅ API Key created: {api_key}")

    # Create token
    token = create_token('admin', 'admin')
    print(f"✅ JWT Token created: {token[:50]}...")

    # Verify
    print(f"✅ API Key valid: {verify_api_key(api_key)}")

    payload = decode_token(token)
    print(f"✅ Token decoded: {payload}")

    print("\n" + "=" * 60)
    print("Default credentials:")
    print("  Username: admin")
    print("  Password: admin123")
    print("  (Change in production!)")
