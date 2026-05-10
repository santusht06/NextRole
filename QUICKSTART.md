# NextRole - Quick Start Guide

## 🚀 30-Minute Quick Start

### Prerequisites
- Docker & Docker Compose installed
- OpenAI API key (get at https://platform.openai.com/api-keys)

### Step 1: Clone & Setup

```bash
# Clone repository
git clone https://github.com/yourusername/NextRole.git
cd NextRole

# Create environment file
cat > backend/.env << EOF
DATABASE_URL=postgresql://user:password@localhost:5432/student_opportunities
OPENAI_API_KEY=your-openai-api-key-here
SECRET_KEY=dev-secret-key-change-in-production
DEBUG=True
ENVIRONMENT=development
EOF
```

### Step 2: Start with Docker

```bash
# Build and start all services
docker-compose -f docker/docker-compose.yml up -d

# Wait for PostgreSQL to be healthy (30 seconds)
sleep 30

# Seed sample data
docker-compose -f docker/docker-compose.yml exec backend python scripts/seed_db.py

# Verify services are running
docker-compose -f docker/docker-compose.yml ps
```

### Step 3: Access the Application

- **Frontend**: http://localhost:3000 (or http://localhost if using nginx)
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (interactive Swagger UI)
- **Database**: localhost:5432 (PostgreSQL)

### Step 4: Test Features

```bash
# Search opportunities
curl "http://localhost:8000/api/opportunities"

# Semantic search
curl "http://localhost:8000/api/search/semantic?q=React%20internships"

# Get trending
curl "http://localhost:8000/api/opportunities/trending"

# Health check
curl "http://localhost:8000/health"
```

---

## 🛠️ Local Development (Without Docker)

### Backend Setup

```bash
cd backend

# Virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Dependencies
pip install -r requirements.txt

# Database (if local PostgreSQL)
createdb student_opportunities
psql student_opportunities < ../database/init.sql

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend

# Dependencies
npm install

# Development server
npm run dev  # Starts at http://localhost:5173
```

---

## 📚 Key Features Demo

### 1. Semantic Search

Try these searches in the UI:
- "AI internships for freshers"
- "hackathons without competitive programming"
- "remote backend opportunities in India"
- "machine learning internships"

### 2. Advanced Filtering

- Filter by opportunity type (internship, hackathon, contest, etc.)
- Filter by location or remote-only
- Sort by recency or deadline

### 3. Bookmarking

- Click bookmark icon to save opportunities
- View saved in /saved page
- Persistent across sessions

### 4. Real-time Updates

Background jobs automatically:
- Expire past-deadline opportunities
- Verify apply links
- Scrape new opportunities
- Remove duplicates

---

## 🔍 API Examples

### List Opportunities

```bash
curl "http://localhost:8000/api/opportunities?page=1&page_size=20"
```

### Semantic Search

```bash
curl "http://localhost:8000/api/search/semantic?q=React&limit=10"
```

### Get Single Opportunity

```bash
curl "http://localhost:8000/api/opportunities/1"
```

### Save Opportunity

```bash
curl -X POST "http://localhost:8000/api/saved/1"
```

### Get Saved Opportunities

```bash
curl "http://localhost:8000/api/saved"
```

---

## 🐛 Troubleshooting

### Docker Issues

```bash
# View logs
docker-compose -f docker/docker-compose.yml logs backend

# Restart services
docker-compose -f docker/docker-compose.yml restart

# Full reset
docker-compose -f docker/docker-compose.yml down -v
docker-compose -f docker/docker-compose.yml up -d
```

### Database Connection Error

```bash
# Check PostgreSQL is running
docker-compose -f docker/docker-compose.yml ps postgres

# Check credentials in .env
grep DATABASE_URL backend/.env

# Manually test connection
psql $DATABASE_URL -c "SELECT 1"
```

### OpenAI API Error

- Verify API key is valid
- Check OpenAI account has credits
- Monitor API usage at https://platform.openai.com/account/usage
- Check error message: `curl http://localhost:8000/health/db`

### Frontend Not Loading

- Clear browser cache: Ctrl+Shift+Delete
- Check frontend service: `docker ps | grep frontend`
- View frontend logs: `docker logs student-opp-web`
- Try hard refresh: Ctrl+F5

---

## 📝 Environment Variables

Key configuration variables in `.env`:

```env
# Database
DATABASE_URL=postgresql://user:pass@host:5432/db_name

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4

# Security
SECRET_KEY=your-secret-key-min-32-chars
DEBUG=False  # Set to False in production

# Scheduling
CHECK_EXPIRED_INTERVAL_HOURS=6
REFRESH_EMBEDDINGS_INTERVAL_HOURS=24
SCRAPER_RUN_INTERVAL_HOURS=12

# Search
SEMANTIC_SEARCH_THRESHOLD=0.6
MAX_SEARCH_RESULTS=50
```

---

## 🎯 Next Steps

1. **Add Real Data**: Implement actual scrapers for production sources
2. **Authentication**: Set up Google OAuth for real users
3. **Advanced Search**: Add AI chat interface for natural language search
4. **Notifications**: Email alerts for saved opportunities
5. **Analytics**: Track user behavior and popular searches
6. **Mobile App**: React Native version
7. **Resume Matching**: Score opportunities based on user profile

---

## 📊 Performance Tips

- Enable browser caching for static assets
- Use semantic search instead of keyword for better results
- Implement pagination limits
- Monitor OpenAI API usage
- Set up CDN for frontend assets
- Use read replicas for database
- Implement Redis caching layer

---

## 🔗 Useful Links

- FastAPI Docs: https://fastapi.tiangolo.com/
- React Docs: https://react.dev
- PostgreSQL pgvector: https://github.com/pgvector/pgvector
- OpenAI API: https://platform.openai.com
- TailwindCSS: https://tailwindcss.com
- Zustand: https://github.com/pmndrs/zustand

---

## 📞 Support

- **Issues**: Open GitHub issues
- **Discussions**: Use GitHub discussions
- **Email**: support@nextrole.app

**Happy coding! 🚀**
