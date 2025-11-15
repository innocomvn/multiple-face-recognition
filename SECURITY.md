# 🔒 Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability, please email **security@example.com** instead of using the issue tracker.

We take security seriously and will respond within 48 hours.

---

## Security Best Practices

### 1. Authentication & Authorization ✅

**Default Credentials** (⚠️ CHANGE IMMEDIATELY):
```
Username: admin
Password: admin123
```

**Action Required:**
```bash
# Login and change admin password
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Then update password in database
```

**JWT Configuration:**
```python
# In auth.py - Change in production!
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or secrets.token_hex(32)
```

### 2. Secret Key Management 🔑

**Generate Strong Secret Key:**
```bash
python -c 'import secrets; print(secrets.token_hex(32))'
```

**Set in Environment:**
```bash
export SECRET_KEY=<your-generated-key>
```

**Never commit secrets:**
- ✅ Use `.env` files (already in `.gitignore`)
- ✅ Use environment variables
- ❌ Never hardcode secrets
- ❌ Never commit `.env` to git

### 3. Input Validation 🛡️

**File Upload Security:**
```python
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
```

**SQL Injection Prevention:**
- ✅ Using parameterized queries (we do this)
- ❌ Never concatenate SQL strings

```python
# ✅ SAFE
cursor.execute("SELECT * FROM Users WHERE username=?", (username,))

# ❌ UNSAFE
cursor.execute(f"SELECT * FROM Users WHERE username='{username}'")
```

### 4. HTTPS/SSL 🔐

**Production Requirements:**
- ✅ Use HTTPS only
- ✅ Redirect HTTP to HTTPS
- ✅ Use strong TLS version (1.2+)
- ✅ Set secure cookie flags

**Nginx Configuration:**
```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

### 5. CORS Configuration 🌐

**Current (Development):**
```python
CORS(app)  # Allows all origins
```

**Production (Recommended):**
```python
CORS(app, origins=[
    "https://yourdomain.com",
    "https://www.yourdomain.com"
])
```

### 6. Rate Limiting ⏱️

**Prevent brute force attacks:**
```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/auth/login')
@limiter.limit("5 per minute")
def login():
    # Login logic
```

### 7. Password Security 🔒

**Requirements:**
- ✅ Minimum 8 characters
- ✅ Hashed with SHA-256 (upgrade to bcrypt recommended)
- ✅ Never log passwords
- ✅ No password in URLs

**Upgrade to bcrypt:**
```python
from werkzeug.security import generate_password_hash, check_password_hash

# Hash
password_hash = generate_password_hash(password, method='pbkdf2:sha256')

# Verify
check_password_hash(password_hash, password)
```

### 8. Database Security 💾

**SQLite (Current):**
- ✅ File permissions (600)
- ✅ Regular backups
- ⚠️ Not ideal for production

**PostgreSQL (Recommended for Production):**
```bash
# Install
pip install psycopg2-binary

# Connection
DATABASE_URL=postgresql://user:password@localhost/frams
```

### 9. File System Security 📁

**Directory Permissions:**
```bash
chmod 700 logs/
chmod 700 backups/
chmod 755 "Training images/"
chmod 755 "Customer images/"
```

**Secure Uploads:**
```python
import os
from werkzeug.utils import secure_filename

filename = secure_filename(file.filename)
file.save(os.path.join(UPLOAD_FOLDER, filename))
```

### 10. Logging Security 📝

**Don't log sensitive data:**
```python
# ❌ BAD
app.logger.info(f"User {username} logged in with password {password}")

# ✅ GOOD
app.logger.info(f"User {username} logged in successfully")
```

**Secure log files:**
```bash
chmod 600 logs/*.log
```

---

## Security Checklist

### Pre-Production

- [ ] Change all default passwords
- [ ] Set strong SECRET_KEY
- [ ] Configure HTTPS/SSL
- [ ] Set up firewall rules
- [ ] Enable rate limiting
- [ ] Review CORS settings
- [ ] Scan for vulnerabilities
- [ ] Update all dependencies
- [ ] Remove debug mode
- [ ] Secure file permissions

### Deployment

- [ ] Use environment variables
- [ ] Enable security headers
- [ ] Set up monitoring
- [ ] Configure backup encryption
- [ ] Test authentication flows
- [ ] Review error messages (no info leakage)
- [ ] Disable directory listing
- [ ] Set session timeout

### Post-Deployment

- [ ] Monitor logs for suspicious activity
- [ ] Regular security audits
- [ ] Keep dependencies updated
- [ ] Regular backups
- [ ] Incident response plan

---

## OWASP Top 10 Mitigation

### 1. Injection
- ✅ Parameterized queries
- ✅ Input validation
- ✅ Escape user input

### 2. Broken Authentication
- ✅ JWT tokens
- ✅ Password hashing
- ✅ Session management

### 3. Sensitive Data Exposure
- ✅ HTTPS only
- ✅ Encrypted backups
- ✅ No secrets in code

### 4. XML External Entities (XXE)
- ✅ N/A (not using XML)

### 5. Broken Access Control
- ✅ Role-based access
- ✅ Authentication required
- ✅ Authorization checks

### 6. Security Misconfiguration
- ✅ Secure defaults
- ✅ Remove unnecessary features
- ✅ Up-to-date software

### 7. Cross-Site Scripting (XSS)
- ✅ Input sanitization
- ✅ Output encoding
- ✅ Content Security Policy

### 8. Insecure Deserialization
- ✅ Validate serialized objects
- ✅ Use safe formats (JSON)

### 9. Using Components with Known Vulnerabilities
- ✅ Regular updates
- ✅ Dependency scanning

### 10. Insufficient Logging & Monitoring
- ✅ Comprehensive logging
- ✅ Monitor access patterns
- ✅ Alert on suspicious activity

---

## Security Tools

### Vulnerability Scanning
```bash
# Install
pip install bandit safety

# Scan code
bandit -r . -ll

# Check dependencies
safety check
```

### Dependency Updates
```bash
# Check outdated
pip list --outdated

# Update
pip install --upgrade <package>
```

### SSL Testing
```bash
# Test SSL configuration
ssllabs.com/ssltest/
```

---

## Incident Response

### If Compromised:

1. **Immediate Actions:**
   - Take affected systems offline
   - Change all passwords and keys
   - Revoke compromised tokens
   - Block suspicious IPs

2. **Investigation:**
   - Review logs
   - Identify entry point
   - Assess damage
   - Document findings

3. **Recovery:**
   - Patch vulnerabilities
   - Restore from clean backup
   - Re-deploy securely
   - Monitor closely

4. **Post-Incident:**
   - Update security policies
   - Improve monitoring
   - Train team
   - Document lessons learned

---

## Security Updates

Stay informed:
- Follow security advisories
- Subscribe to CVE alerts
- Monitor dependency vulnerabilities
- Regular security audits

---

## Contact

**Security Team:** security@example.com
**Response Time:** Within 48 hours
**PGP Key:** [Public key URL]

---

## Supported Versions

| Version | Supported |
|---------|-----------|
| 2.0.x   | ✅        |
| 1.0.x   | ❌        |

---

**Last Updated:** 2025-01-15
**Next Review:** 2025-04-15
