# Setup & Deployment Guide

## Table of Contents

1. [Development Setup](#development-setup)
2. [Docker Deployment](#docker-deployment)
3. [Production Deployment](#production-deployment)
4. [Troubleshooting](#troubleshooting)

---

## Development Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ (with pgvector extension)
- OpenAI API Key

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment file
cp .env.example .env
# Edit .env and add your OpenAI API key and database URL
```

### Database Setup

```bash
# Create PostgreSQL database
createdb student_opportunities

# Install pgvector extension
psql student_opportunities -c "CREATE EXTENSION IF NOT EXISTS vector"

# Create tables
psql student_opportunities < ../database/init.sql

# Seed with sample data (optional)
python ../scripts/seed_db.py
```

### Run Backend

```bash
# From backend directory with venv activated
uvicorn app.main:app --reload --port 8000

# API will be available at http://localhost:8000
# API documentation at http://localhost:8000/docs
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file (optional, uses defaults)
cp .env.example .env

# Start development server
npm run dev

# Frontend will be available at http://localhost:5173
```

### Accessing the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **Database**: localhost:5432

---

## Docker Deployment

### Quick Start with Docker Compose

```bash
# Navigate to project root
cd AI-POWDERED-STUDENT-PLATFORM

# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor

# Start all services
docker-compose -f docker/docker-compose.yml up -d

# Check status
docker-compose -f docker/docker-compose.yml ps

# View logs
docker-compose -f docker/docker-compose.yml logs -f
```

### Seed Database in Docker

```bash
# Seed with sample data
docker-compose -f docker/docker-compose.yml exec backend python scripts/seed_db.py

# Or directly execute
docker exec student-opp-api python scripts/seed_db.py
```

### Access Services

- **Frontend**: http://localhost (served via Nginx)
- **Backend API**: http://localhost/api
- **API Docs**: http://localhost/api/docs
- **Database**: localhost:5432

### Docker Compose Services

| Service | Port | Purpose |
|---------|------|---------|
| postgres | 5432 | PostgreSQL database |
| backend | 8000 | FastAPI application |
| frontend | 80 | React + Nginx |

### Docker Compose Commands

```bash
# Start services
docker-compose -f docker/docker-compose.yml up -d

# Stop services
docker-compose -f docker/docker-compose.yml down

# View logs
docker-compose -f docker/docker-compose.yml logs -f [service-name]

# Rebuild images
docker-compose -f docker/docker-compose.yml build --no-cache

# Execute command in container
docker-compose -f docker/docker-compose.yml exec backend bash
```

---

## Production Deployment

### Pre-Production Checklist

- [ ] OpenAI API key configured
- [ ] Database credentials set securely
- [ ] SECRET_KEY set to random value (min 32 chars)
- [ ] ENVIRONMENT set to "production"
- [ ] DEBUG set to "false"
- [ ] CORS origins configured correctly
- [ ] Database backups configured
- [ ] SSL certificates ready
- [ ] Domain name configured

### Environment Configuration

Create `.env` file with production values:

```bash
# Database
DATABASE_URL=postgresql://prod_user:strong_password@prod-db.example.com:5432/student_opportunities

# OpenAI
OPENAI_API_KEY=sk-...your-key-here...

# Security
SECRET_KEY=your-very-long-random-secret-key-at-least-32-characters
ENVIRONMENT=production
DEBUG=false

# CORS
ALLOWED_ORIGINS=["https://yourdomain.com"]
```

### Deployment Options

#### Option 1: Docker on VPS (Recommended for MVP)

```bash
# 1. SSH into VPS
ssh user@your-vps.com

# 2. Clone repository
git clone https://github.com/yourusername/AI-POWDERED-STUDENT-PLATFORM.git
cd AI-POWDERED-STUDENT-PLATFORM

# 3. Setup environment
cp .env.example .env
# Edit .env with production values
nano .env

# 4. Start services
docker-compose -f docker/docker-compose.yml up -d

# 5. Setup automatic backups and monitoring
# (Add your backup strategy here)
```

#### Option 2: Railway.app

```bash
# 1. Create Railway project
# 2. Connect GitHub repository
# 3. Add services:
#    - PostgreSQL
#    - Backend (Python)
#    - Frontend (Node)
# 4. Configure environment variables
# 5. Deploy automatically on push
```

#### Option 3: Render

```bash
# Backend
# - Deploy from GitHub
# - Build command: pip install -r requirements.txt
# - Start command: uvicorn app.main:app --host 0.0.0.0 --port 8000
# - Add PostgreSQL service
# - Set environment variables

# Frontend
# - Deploy from GitHub
# - Build command: npm install && npm run build
# - Publish directory: dist
```

#### Option 4: AWS ECS + RDS

```bash
# 1. Create RDS PostgreSQL instance
# 2. Build Docker images
docker build -t backend:latest -f docker/Dockerfile.backend .
docker build -t frontend:latest -f docker/Dockerfile.frontend .

# 3. Push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account.dkr.ecr.us-east-1.amazonaws.com
docker tag backend:latest your-account.dkr.ecr.us-east-1.amazonaws.com/backend:latest
docker push your-account.dkr.ecr.us-east-1.amazonaws.com/backend:latest

# 4. Create ECS cluster and services
# 5. Configure load balancing with ALB
# 6. Setup CloudFront CDN
```

### Setting Up SSL with Let's Encrypt (Docker)

```bash
# Update docker-compose.yml to include Certbot
# Or use Traefik for automatic SSL

# Manual setup:
docker run --rm -it -v /etc/letsencrypt:/etc/letsencrypt -v /var/www/certbot:/var/www/certbot certbot/certbot certonly --webroot -w /var/www/certbot -d yourdomain.com
```

### Database Backups

```bash
# Daily backup script
#!/bin/bash
BACKUP_DIR="/backups/postgres"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
docker exec student-opp-db pg_dump -U user student_opportunities > "$BACKUP_DIR/backup_$TIMESTAMP.sql"

# Add to crontab
0 2 * * * /path/to/backup-script.sh
```

### Monitoring & Logging

```bash
# Application logs
docker-compose -f docker/docker-compose.yml logs -f backend

# Structured logging setup (optional)
# Use ELK stack or similar for production monitoring
```

---

## Troubleshooting

### Common Issues

#### 1. Database Connection Error

```
Error: could not connect to server: Connection refused
```

**Solution:**
```bash
# Check if PostgreSQL is running
docker-compose -f docker/docker-compose.yml ps

# Restart database
docker-compose -f docker/docker-compose.yml restart postgres

# Check logs
docker-compose -f docker/docker-compose.yml logs postgres
```

#### 2. OpenAI API Key Invalid

```
Error: Invalid API key provided
```

**Solution:**
```bash
# Verify API key in .env
cat .env | grep OPENAI_API_KEY

# Check key format starts with sk-
# Regenerate key from https://platform.openai.com/api-keys
```

#### 3. Port Already in Use

```
Error: Address already in use
```

**Solution:**
```bash
# Change ports in docker-compose.yml or kill existing process
# Find process using port 5173
lsof -i :5173
# Kill process
kill -9 <PID>

# Or change port in vite.config.ts
```

#### 4. Node Modules Issues

```
npm ERR! peer dep missing
```

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

#### 5. TypeScript Errors

```
Type errors in frontend
```

**Solution:**
```bash
cd frontend
npm run type-check
# Fix any errors shown
# Rebuild with npm run build
```

#### 6. Database Migration Issues

```
Error: relation "opportunities" does not exist
```

**Solution:**
```bash
# Recreate database
docker-compose -f docker/docker-compose.yml exec postgres psql -U user -c "DROP DATABASE student_opportunities;"
docker-compose -f docker/docker-compose.yml exec postgres psql -U user -c "CREATE DATABASE student_opportunities;"
docker-compose -f docker/docker-compose.yml exec postgres psql -U user -d student_opportunities < database/init.sql
```

### Performance Troubleshooting

#### Slow API Response

```bash
# Check if indexing is applied
docker-compose -f docker/docker-compose.yml exec backend python -c "
from app.core.database import SessionLocal
from app.models.opportunity import Opportunity
db = SessionLocal()
print(db.query(Opportunity).count())
"

# Check API logs for slow queries
docker-compose -f docker/docker-compose.yml logs backend | grep "Query took"
```

#### High Memory Usage

```bash
# Check memory limits
docker stats

# Adjust in docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 1G
        reservations:
          memory: 512M
```

### Verification Steps

After deployment, verify everything works:

```bash
# 1. Check API health
curl http://localhost:8000/health

# 2. Check if frontend loads
curl http://localhost:80

# 3. List opportunities
curl http://localhost:8000/api/opportunities/

# 4. Test semantic search
curl "http://localhost:8000/api/search/semantic?q=react+internships"

# 5. Check database connection
docker-compose -f docker/docker-compose.yml exec postgres psql -U user -d student_opportunities -c "SELECT COUNT(*) FROM opportunities;"
```

---

## Maintenance

### Regular Maintenance Tasks

```bash
# Weekly: Check logs for errors
docker-compose -f docker/docker-compose.yml logs --since 7d | grep ERROR

# Monthly: Update dependencies
cd backend && pip list --outdated
cd ../frontend && npm outdated

# Quarterly: Full backup
docker-compose -f docker/docker-compose.yml exec postgres pg_dump -U user student_opportunities | gzip > full_backup.sql.gz
```

### Scaling Considerations

For 10k+ users:
- Implement caching layer (Redis)
- Add database read replicas
- Implement API rate limiting
- Setup CDN for static assets
- Use load balancing for backend instances

---

## Support & Resources

- **API Docs**: http://localhost:8000/docs (Swagger)
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **React Docs**: https://react.dev/
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **pgvector Docs**: https://github.com/pgvector/pgvector
- **Docker Docs**: https://docs.docker.com/
