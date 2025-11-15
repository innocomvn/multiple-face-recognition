# 🚀 FRAMS Deployment Guide

Complete guide for deploying FRAMS to various platforms.

---

## Table of Contents
- [Heroku](#heroku)
- [AWS EC2](#aws-ec2)
- [Google Cloud](#google-cloud)
- [DigitalOcean](#digitalocean)
- [Docker](#docker)
- [Production Checklist](#production-checklist)

---

## Heroku

### Prerequisites
- Heroku CLI installed
- Heroku account

### Steps

1. **Login to Heroku**
```bash
heroku login
```

2. **Create Heroku App**
```bash
heroku create frams-app
```

3. **Add Buildpacks**
```bash
heroku buildpacks:add --index 1 https://github.com/heroku/heroku-buildpack-apt
heroku buildpacks:add --index 2 heroku/python
```

4. **Configure Environment**
```bash
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
```

5. **Deploy**
```bash
git push heroku main
```

6. **Scale**
```bash
heroku ps:scale web=1
```

7. **Open App**
```bash
heroku open
```

### Heroku-Specific Files

**Procfile** (already exists):
```
web: gunicorn app_improved:app
```

**Aptfile** (for system dependencies):
```
libsm6
libxext6
libxrender-dev
libgomp1
libglib2.0-0
```

---

## AWS EC2

### Prerequisites
- AWS Account
- EC2 key pair created

### Steps

1. **Launch EC2 Instance**
- AMI: Ubuntu Server 20.04 LTS
- Instance Type: t2.medium (minimum)
- Security Group: Open ports 22, 80, 443, 5000

2. **Connect to Instance**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

3. **Install Dependencies**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3.8 python3-pip python3-venv -y

# Install system dependencies
sudo apt install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev
```

4. **Clone Repository**
```bash
git clone <your-repo-url>
cd multiple-face-recognition
```

5. **Setup Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

6. **Configure Environment**
```bash
cp .env.example .env
nano .env  # Edit configuration
```

7. **Run with Gunicorn**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app_improved:app
```

8. **Setup Nginx (Optional)**
```bash
sudo apt install nginx -y

# Create Nginx config
sudo nano /etc/nginx/sites-available/frams
```

**Nginx Config:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/frams /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

9. **Setup Systemd Service**
```bash
sudo nano /etc/systemd/system/frams.service
```

```ini
[Unit]
Description=FRAMS Gunicorn Application
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/multiple-face-recognition
Environment="PATH=/home/ubuntu/multiple-face-recognition/venv/bin"
ExecStart=/home/ubuntu/multiple-face-recognition/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app_improved:app

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable frams
sudo systemctl start frams
sudo systemctl status frams
```

---

## Google Cloud Platform

### Prerequisites
- GCP Account
- gcloud CLI installed

### Steps

1. **Initialize gcloud**
```bash
gcloud init
```

2. **Create app.yaml**
```yaml
runtime: python38
entrypoint: gunicorn -b :$PORT app_improved:app

instance_class: F2

automatic_scaling:
  min_instances: 1
  max_instances: 10

env_variables:
  FLASK_ENV: "production"
```

3. **Deploy**
```bash
gcloud app deploy
```

4. **View App**
```bash
gcloud app browse
```

---

## DigitalOcean

### Using App Platform

1. **Connect GitHub Repository**
- Go to DigitalOcean Dashboard
- Create > Apps > GitHub

2. **Configure Build**
- Build Command: `pip install -r requirements.txt`
- Run Command: `gunicorn -w 4 -b 0.0.0.0:8080 app_improved:app`

3. **Environment Variables**
```
FLASK_ENV=production
SECRET_KEY=<generate-random-key>
```

4. **Deploy**
- Click "Create Resources"
- Wait for deployment

### Using Droplet

Similar to AWS EC2 steps above.

---

## Docker

### Local Build & Run

```bash
# Build
docker build -t frams:latest .

# Run
docker run -p 5000:5000 \
  -v $(pwd)/Training\ images:/app/Training\ images \
  -v $(pwd)/Customer\ images:/app/Customer\ images \
  frams:latest
```

### Docker Compose

```bash
docker-compose up -d
docker-compose logs -f
```

### Push to Registry

```bash
# Docker Hub
docker tag frams:latest your-username/frams:latest
docker push your-username/frams:latest

# AWS ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

docker tag frams:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/frams:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/frams:latest
```

---

## Production Checklist

### Security
- [ ] Change default admin password
- [ ] Set strong SECRET_KEY
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Enable rate limiting
- [ ] Set up authentication
- [ ] Review .gitignore
- [ ] Scan for vulnerabilities

### Performance
- [ ] Use production-grade server (Gunicorn)
- [ ] Enable caching
- [ ] Optimize database queries
- [ ] Set up CDN for static files
- [ ] Configure auto-scaling

### Monitoring
- [ ] Set up logging
- [ ] Configure error tracking (Sentry)
- [ ] Set up health checks
- [ ] Monitor resource usage
- [ ] Set up alerts

### Backup
- [ ] Automate database backups
- [ ] Store backups off-site
- [ ] Test restore process
- [ ] Backup training/customer images

### Configuration
```bash
# Generate secure secret key
python -c 'import secrets; print(secrets.token_hex(32))'

# Set environment variables
export FLASK_ENV=production
export FLASK_DEBUG=False
export SECRET_KEY=<your-secret-key>
export DATABASE_URL=<your-database-url>
```

### Database Migration
```bash
# Backup current database
python backup_database.py --compress

# Migrate to PostgreSQL (recommended for production)
pip install psycopg2-binary
# Update DATABASE_URL in .env
```

---

## Environment Variables

Create `.env` file:

```bash
# Flask
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here

# Server
HOST=0.0.0.0
PORT=5000

# Database
DATABASE_PATH=information.db

# Face Recognition
FACE_MATCH_THRESHOLD=0.50

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# CORS
CORS_ORIGINS=https://yourdomain.com

# Email (optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

---

## SSL/HTTPS Setup

### Using Certbot (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo certbot renew --dry-run
```

---

## Troubleshooting

### Port Already in Use
```bash
# Find process
lsof -i :5000

# Kill process
kill -9 <PID>
```

### Memory Issues
```bash
# Check memory
free -h

# Increase swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Logs
```bash
# Application logs
tail -f logs/app.log

# System logs
sudo journalctl -u frams -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log
```

---

## Support

For deployment issues:
- Check logs first
- Review [SECURITY.md](SECURITY.md)
- Create GitHub issue
- Email support@example.com

---

**Good luck with your deployment! 🚀**
