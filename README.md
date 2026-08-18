# NextRole - AI-Powered Student Opportunity Platform

A modern, production‑ready platform for discovering genuine and active student opportunities including internships, hackathons, coding contests, graduate programs, and hiring challenges.

## 📦 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/NextRole.git
   cd NextRole
   ```

2. **Backend dependencies**

   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Frontend dependencies**

   ```bash
   cd ../frontend
   npm install
   ```

4. **Optional: Docker setup**

   ```bash
   cd ../docker
   docker compose -f docker-compose.yml up -d
   ```

   This builds and starts the backend, frontend, PostgreSQL, and Nginx services.

## 🎯 Key Features

- **AI-Powered Discovery**: Intelligent semantic search using OpenAI embeddings
- **Fresh Opportunities Only**: Only active listings with automatic expiry detection
- **Multiple Aggregation Sources**: Scrapes from Devfolio, HackerEarth, Unstop, MLH, and company career pages
- **Semantic Search**: Find opportunities by meaning, not just keywords
- **Smart Categorization**: AI‑extracted structured data with automatic classification
- **Vector Search**: pgvector‑powered similarity search for better recommendations
- **Trending & Recommendations**: AI‑based opportunity recommendations
- **Bookmark System**: Save opportunities for later
- **Dark Mode**: Modern UI with dark mode support
- **Real-time Updates**: Background jobs for continuous opportunity freshness

## 🏗️ Architecture

### Tech Stack

**Frontend**
- React 18 + Vite
- TypeScript
- TailwindCSS
- Zustand (State Management)
- TanStack Query (Data Fetching)
- Lucide React (Icons)

**Backend**
- FastAPI (Python)
- PostgreSQL + pgvector
- SQLAlchemy ORM
- OpenAI API (GPT‑4 & Embeddings)
- APScheduler (Background Jobs)

**Infrastructure**
- Docker & Docker Compose
- PostgreSQL 15 with pgvector
- Nginx (Reverse Proxy)

## 📋 Project Structure

```
NextRole/
├── frontend/               # React application
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── pages/         # Page components
│   │   ├── hooks/         # Custom React hooks
│   │   ├── services/      # API services
│   │   ├── store/         # Zustand stores
│   │   ├── types/         # TypeScript types
│   │   └── utils/         # Utility functions
│   └── package.json
│
├── backend/               # FastAPI application
│   ├── app/
│   │   ├── api/           # Route handlers
│   │   ├── models/        # SQLAlchemy models
│   │   ├── services/      # Business logic
│   │   ├── scraping/      # Scraper implementations
│   │   ├── workers/       # Background jobs
│   │   └── __init__.py

#### 2. Environment Configuration

Create `.env` file from template:

```bash
cp backend/.env.example backend/.env
```

Update with your configuration:

```makefile
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/student_opportunities

# OpenAI
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4

# Security
SECRET_KEY=your-super-secret-key-change-in-production
DEBUG=True
ENVIRONMENT=development
```

#### 3. Using Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose -f docker/docker-compose.yml up -d

# Create database tables
docker-compose -f docker/docker-compose.yml exec backend python -m app.core.database init_db

# Seed sample data
docker-compose -f docker/docker-compose.yml exec backend python scripts/seed_db.py
```

Access:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database**: localhost:5432

#### 4. Local Development Setup

##### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations (if using Alembic)
alembic upgrade head

# Start server
uvicorn app.main:app --reload --port 8000
```

##### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

### Database Setup

The database schema includes:

- **opportunities**: Main opportunity listings
- **users**: User accounts and profiles
- **saved_opportunities**: Bookmarked opportunities
- **embeddings**: Vector embeddings for semantic search
- **scrape_logs**: Scraping history and logs

pgvector is automatically created and indexes are set up for optimal performance.

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api
```

### Key Endpoints

#### Opportunities
- `GET /opportunities` - List all active opportunities
- `GET /opportunities/{id}` - Get specific opportunity
- `GET /opportunities/trending` - Get trending opportunities
- `GET /opportunities/stats/overview` - Get statistics

#### Search
- `GET /search?q=query` - Keyword search
- `GET /search/semantic?q=query` - Semantic search with embeddings
- `GET /search/ai-recommendations?query=query` - AI-powered recommendations

#### Saved
- `GET /saved` - Get user's saved opportunities
- `POST /saved/{opportunity_id}` - Save opportunity
- `DELETE /saved/{opportunity_id}` - Unsave opportunity
- `GET /saved/check/{opportunity_id}` - Check if saved

#### Health
- `GET /health` - Health check
- `GET /health/db` - Database health check

Full API documentation available at: `http://localhost:8000/docs`

## 🔄 Data Pipeline

### Scraping Pipeline

1. **Source Aggregation**: Scrape opportunities from multiple sources
2. **Deduplication**: Identify and merge duplicate opportunities
3. **AI Extraction**: Extract structured data using GPT-4
4. **Classification**: Automatically classify opportunity type
5. **Embedding Generation**: Create vector embeddings for semantic search
6. **Storage**: Store in PostgreSQL with pgvector

### Background Jobs

Automatic tasks running via APScheduler:

- **Expire Old Opportunities** (Every 6 hours): Mark past deadline opportunities as expired
- **Verify Apply Links** (Every 12 hours): Check link validity
- **Run Scrapers** (Every 24 hours): Fetch new opportunities
- **Deduplicate** (Every 48 hours): Remove duplicate entries
- **Refresh Embeddings** (Daily): Update embeddings for better search

## 🔍 Search Features

### Keyword Search
Traditional full-text search on title, description, company, and skills.

### Semantic Search
AI-powered similarity search using OpenAI embeddings. Find opportunities by meaning:
- "AI internships for freshers"
- "hackathons without DSA"
- "remote web dev opportunities"

### Hybrid Search
Combines keyword and semantic search for optimal results.

### AI Reranking (Optional)
GPT-4 reranks results based on query relevance for better accuracy.

## 🎨 UI Components

### Key Components

- **OpportunityCard**: Display individual opportunities
- **FilterBar**: Advanced filtering options
- **Pagination**: Efficient result navigation
- **LoadingStates**: Skeleton loaders and spinners
- **Header**: Navigation and search
- **MainLayout**: Consistent page layout

## 🔒 Security Features

- JWT-based authentication
- Password hashing with bcrypt
- CORS protection
- Input validation with Pydantic
- SQL injection prevention via SQLAlchemy ORM
- Rate limiting ready (implement as needed)
- Environment variable configuration

## 📊 Performance Optimization

- Vector index optimization with IVFFlat
- Database query optimization with indexes
- Frontend code splitting with Vite
- Efficient pagination
- Caching strategies
- Background job optimization

## 📝 Seed Database

Run sample data:

```bash
python scripts/seed_db.py
```

This creates:
- Sample opportunities from various sources
- Demo user accounts
- Sample embeddings
- Test data for development

## 🐛 Development Tips

### Adding New Opportunity Source

1. Create scraper in `backend/app/scraping/scrapers.py`
2. Extend `BaseScraper` class
3. Implement `scrape()` method
4. Register in `run_all_scrapers()`

### Adding New API Endpoint

1. Create route in `backend/app/api/`
2. Add database queries in services
3. Define Pydantic schemas
4. Test with FastAPI docs at `/docs`

### Customizing Frontend

1. Modify components in `frontend/src/components/`
2. Update stores in `frontend/src/store/`
3. Add pages in `frontend/src/pages/`
4. Customize styling with Tailwind

## 📱 Responsive Design

The platform is fully responsive:
- Mobile-first approach
- Tablet optimization
- Desktop experience
- Dark mode support across all breakpoints

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📦 Deployment

### Production Build

```bash
# Frontend
cd frontend
npm run build
# Outputs to dist/

# Backend
# Ensure all environment variables are set
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Docker Production

```bash
docker-compose -f docker/docker-compose.yml -e ENVIRONMENT=production up -d
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4 and embedding models
- FastAPI for the backend framework
- React team for the frontend library
- pgvector for vector search capabilities
- All contributors and users

## 📧 Support

For support, email support@nextrole.app or open an issue on GitHub.

## 🗺️ Roadmap

- [ ] User authentication with OAuth
- [ ] Email alerts for new opportunities
- [ ] Resume matching and ranking
- [ ] Advanced filtering and saved searches
- [ ] Opportunity recommendations based on user profile
- [ ] Mobile app (React Native)
- [ ] Batch-wise filtering
