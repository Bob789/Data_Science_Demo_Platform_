# Deployment Guide

Instructions for deploying the ML Model Training Platform to production environments.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Configuration](#environment-configuration)
3. [Development Setup](#development-setup)
4. [Production Deployment](#production-deployment)
5. [Docker Deployment](#docker-deployment)
6. [Monitoring](#monitoring)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements
- Python 3.9 or higher
- PostgreSQL 12 or higher
- 2GB RAM minimum (4GB recommended)
- 10GB disk space for models and logs

### Required Software
- pip or conda for Python packages
- PostgreSQL client (psql)
- Git for version control

---

## Environment Configuration

Create a `.env` file in the project root with the following variables:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ml_platform
DB_USER=postgres
DB_PASSWORD=your_secure_password

# JWT Configuration
JWT_SECRET_KEY=your-very-long-and-secure-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60

# Server Configuration (optional)
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
STREAMLIT_PORT=8501
```

### Security Recommendations

**JWT Secret Key:**
- Use at least 32 characters
- Generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- Never commit to version control

**Database Password:**
- Use strong passwords (16+ characters)
- Store in secure secrets manager for production

---

## Development Setup

### 1. Clone Repository
```bash
git clone https://github.com/Bob789/Final_Project_v003.git
cd Final_Project_v003
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup PostgreSQL Database
```bash
# Create database
createdb ml_platform

# Or via psql
psql -U postgres -c "CREATE DATABASE ml_platform;"
```

### 5. Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
```

### 6. Initialize Admin User
```bash
python scripts/setup_admin.py
```

### 7. Start Development Servers

**Terminal 1 - FastAPI:**
```bash
cd app_fastapi
uvicorn app_fastapi:app --reload --port 8000
```

**Terminal 2 - Streamlit:**
```bash
cd app_streamlit
streamlit run app_streamlit.py --server.port 8501
```

---

## Production Deployment

### System Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and PostgreSQL
sudo apt install python3.9 python3.9-venv python3-pip postgresql postgresql-contrib -y

# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Application Setup

```bash
# Clone repository
git clone https://github.com/Bob789/Final_Project_v003.git
cd Final_Project_v003

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install production dependencies
pip install -r requirements.txt
pip install gunicorn
```

### Database Setup

```bash
# Create production database user
sudo -u postgres psql -c "CREATE USER mlplatform WITH PASSWORD 'secure_password';"
sudo -u postgres psql -c "CREATE DATABASE ml_platform_prod OWNER mlplatform;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ml_platform_prod TO mlplatform;"
```

### Running with Gunicorn

**FastAPI with Gunicorn + Uvicorn Workers:**
```bash
cd app_fastapi
gunicorn app_fastapi:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --access-logfile /var/log/ml_platform/access.log \
    --error-logfile /var/log/ml_platform/error.log
```

### Systemd Service Files

**FastAPI Service (`/etc/systemd/system/ml-fastapi.service`):**
```ini
[Unit]
Description=ML Platform FastAPI Backend
After=network.target postgresql.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/ml_platform/app_fastapi
Environment="PATH=/opt/ml_platform/venv/bin"
EnvironmentFile=/opt/ml_platform/.env
ExecStart=/opt/ml_platform/venv/bin/gunicorn app_fastapi:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

**Streamlit Service (`/etc/systemd/system/ml-streamlit.service`):**
```ini
[Unit]
Description=ML Platform Streamlit Frontend
After=network.target ml-fastapi.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/ml_platform/app_streamlit
Environment="PATH=/opt/ml_platform/venv/bin"
EnvironmentFile=/opt/ml_platform/.env
ExecStart=/opt/ml_platform/venv/bin/streamlit run app_streamlit.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless true
Restart=always

[Install]
WantedBy=multi-user.target
```

**Enable and Start Services:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable ml-fastapi ml-streamlit
sudo systemctl start ml-fastapi ml-streamlit
```

### Nginx Reverse Proxy

**Configuration (`/etc/nginx/sites-available/ml_platform`):**
```nginx
upstream fastapi {
    server 127.0.0.1:8000;
}

upstream streamlit {
    server 127.0.0.1:8501;
}

server {
    listen 80;
    server_name your-domain.com;

    # FastAPI Backend
    location /api/ {
        proxy_pass http://fastapi/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_cache_bypass $http_upgrade;
    }

    # Streamlit Frontend
    location / {
        proxy_pass http://streamlit;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_cache_bypass $http_upgrade;
    }

    # Streamlit WebSocket
    location /_stcore/stream {
        proxy_pass http://streamlit/_stcore/stream;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
    }
}
```

**Enable Site:**
```bash
sudo ln -s /etc/nginx/sites-available/ml_platform /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

---

## Docker Deployment

### Dockerfile

**`Dockerfile.fastapi`:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app_fastapi/ ./app_fastapi/
COPY scripts/ ./scripts/

EXPOSE 8000

CMD ["uvicorn", "app_fastapi.app_fastapi:app", "--host", "0.0.0.0", "--port", "8000"]
```

**`Dockerfile.streamlit`:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app_streamlit/ ./app_streamlit/
COPY app_fastapi/ ./app_fastapi/

EXPOSE 8501

CMD ["streamlit", "run", "app_streamlit/app_streamlit.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
```

### Docker Compose

**`docker-compose.yml`:**
```yaml
version: '3.8'

services:
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: ml_platform
      POSTGRES_USER: mlplatform
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U mlplatform -d ml_platform"]
      interval: 10s
      timeout: 5s
      retries: 5

  fastapi:
    build:
      context: .
      dockerfile: Dockerfile.fastapi
    environment:
      - DB_HOST=db
      - DB_PORT=5432
      - DB_NAME=ml_platform
      - DB_USER=mlplatform
      - DB_PASSWORD=${DB_PASSWORD}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
    depends_on:
      db:
        condition: service_healthy
    ports:
      - "8000:8000"
    volumes:
      - model_data:/app/app_fastapi/models

  streamlit:
    build:
      context: .
      dockerfile: Dockerfile.streamlit
    environment:
      - API_URL=http://fastapi:8000
    depends_on:
      - fastapi
    ports:
      - "8501:8501"

volumes:
  postgres_data:
  model_data:
```

**Run with Docker Compose:**
```bash
docker-compose up -d
```

---

## Monitoring

### Log Locations
- FastAPI logs: `app_fastapi/logs/app.log`
- Gunicorn access: `/var/log/ml_platform/access.log`
- Gunicorn errors: `/var/log/ml_platform/error.log`
- Nginx logs: `/var/log/nginx/`

### Health Checks

**FastAPI Health:**
```bash
curl http://localhost:8000/health
# Expected: {"status": "ok"}
```

**Database Connection:**
```bash
psql -U mlplatform -h localhost -d ml_platform -c "SELECT 1;"
```

### Recommended Monitoring Tools
- **Prometheus + Grafana**: Metrics collection and visualization
- **Sentry**: Error tracking and alerting
- **ELK Stack**: Centralized logging

---

## Troubleshooting

### Common Issues

#### Database Connection Failed
```
Error: could not connect to server: Connection refused
```
**Solution:**
- Verify PostgreSQL is running: `sudo systemctl status postgresql`
- Check connection parameters in `.env`
- Verify firewall allows PostgreSQL port

#### JWT Token Invalid
```
Error: Invalid or expired token
```
**Solution:**
- Check `JWT_SECRET_KEY` matches between restarts
- Verify token hasn't expired
- Re-authenticate to get new token

#### Model Training Fails
```
Error: Training failed: insufficient memory
```
**Solution:**
- Reduce dataset size
- Add swap space
- Use smaller model or fewer cross-validation folds

#### Streamlit Can't Connect to FastAPI
```
Error: Connection refused
```
**Solution:**
- Verify FastAPI is running on correct port
- Check CORS settings if different domains
- Verify network connectivity between containers (Docker)

### Performance Tuning

**Gunicorn Workers:**
```
workers = (2 * CPU_cores) + 1
```

**PostgreSQL:**
```sql
-- Increase shared buffers
ALTER SYSTEM SET shared_buffers = '256MB';
-- Increase work memory
ALTER SYSTEM SET work_mem = '16MB';
```

**Streamlit:**
```bash
# Increase file upload limit
streamlit run app_streamlit.py --server.maxUploadSize 200
```

---

## Backup Procedures

### Database Backup
```bash
# Daily backup script
pg_dump -U mlplatform -h localhost ml_platform | gzip > backup_$(date +%Y%m%d).sql.gz
```

### Model Files Backup
```bash
# Backup trained models
tar -czf models_backup_$(date +%Y%m%d).tar.gz app_fastapi/models/
```

### Restore Procedures
```bash
# Restore database
gunzip -c backup_20251127.sql.gz | psql -U mlplatform -d ml_platform

# Restore models
tar -xzf models_backup_20251127.tar.gz
```

---

*Last Updated: 2025-11-27*
