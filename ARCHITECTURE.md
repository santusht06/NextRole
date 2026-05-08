# Architecture & Design Documentation

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Frontend Layer                              │
│  React + Vite + TailwindCSS + TypeScript (Port 5173 / 80)          │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Pages: Home, Explore, Search, Detail, Saved               │   │
│  │ Components: Cards, Filters, Pagination, Headers           │   │
│  │ State: Zustand (opportunities, UI, saved)                 │   │
│  │ Data Fetching: TanStack Query with Axios                  │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                 ↓ HTTP/REST
┌─────────────────────────────────────────────────────────────────────┐
│                         API Layer                                   │
│  FastAPI + uvicorn (Port 8000)                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ API Routes:                                                │   │
│  │  - /api/opportunities/* → Opportunity endpoints           │   │
│  │  - /api/search/* → Search (keyword/semantic/AI)           │   │
│  │  - /api/saved/* → Bookmark management                     │   │
│  │  - /health → Health checks                               │   │
│  └─────────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Services:                                                  │   │
│  │  - AIExtractionService → OpenAI API calls                 │   │
│  │  - EmbeddingService → Vector generation                  │   │
│  │  - OpportunityService → Business logic                   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Background Jobs (APScheduler):                             │   │
│  │  - Expire opportunities (6h)                              │   │
│  │  - Verify links (12h)                                     │   │
│  │  - Scrape new data (24h)                                  │   │
│  │  - Deduplicate (48h)                                      │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                 ↓ SQL
┌─────────────────────────────────────────────────────────────────────┐
│                     Data Access Layer                               │
│  SQLAlchemy ORM with connection pooling                             │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Database Models:                                           │   │
│  │  - Opportunity (with vector_id reference)                 │   │
│  │  - User (with OAuth support)                              │   │
│  │  - SavedOpportunity (user bookmarks)                      │   │
│  │  - Embedding (pgvector 1536-D)                            │   │
│  │  - ScrapeLog (ingestion tracking)                         │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                 ↓
┌─────────────────────────────────────────────────────────────────────┐
│                       Database Layer                                │
│  PostgreSQL 15+ with pgvector extension                             │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ 5 tables, B-tree + vector indexes                          │  │
│  │ Connection pool: 10 min / 20 max overflow                  │  │
│  │ Automatic backups & Point-in-time recovery                │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagrams

### 1. Opportunity Ingestion Pipeline

```
External Sources (Devfolio, HackerEarth, MLH, Unstop)
    ↓
Scrapers (BeautifulSoup + Requests)
    ↓
Raw HTML/JSON Data
    ↓
AIExtractionService (OpenAI API)
    ↓
Structured JSON
    ├→ Title, Company, Type, Deadline, etc.
    ├→ Eligibility & Skills (arrays)
    └→ AI-generated summary
    ↓
OpportunityService.create_opportunity()
    ├→ Save to opportunities table
    ├→ Generate embedding
    └→ Store vector in embeddings table
    ↓
Database
    ├→ opportunities table
    ├→ embeddings table (pgvector)
    └→ scrape_logs (success/failure tracking)
```

### 2. Search & Retrieval Flow

```
User Query: "React internships in India"
    ↓
Frontend: useSemanticSearch() hook
    ↓
API: GET /api/search/semantic?q=query
    ↓
EmbeddingService.generate_query_embedding()
    ↓
OpenAI embedding API → 1536-D vector
    ↓
PostgreSQL pgvector similarity search
    ├→ WHERE status = 'active'
    ├→ ORDER BY embedding <-> query_vector LIMIT 20
    └→ Also apply metadata filters
    ↓
AIExtractionService.rerank_opportunities() [optional]
    ├→ Send results to OpenAI for relevance ranking
    └→ Return reranked list
    ↓
Response to frontend
    ↓
Frontend renders OpportunityCard components
```

### 3. Background Job Flow

```
Every 6 hours:
  OpportunityService.expire_old_opportunities()
  ├→ Find opportunities where deadline < now()
  ├→ Set status = 'expired'
  └→ Update database

Every 12 hours:
  OpportunityService.verify_apply_links()
  ├→ HTTP HEAD request to apply_link
  ├→ If 200-399 → OK
  ├→ If 400+ → Mark expired
  └→ Update last_verified_at

Every 24 hours:
  run_all_scrapers()
  ├→ DevfolioScraper.scrape()
  ├→ HackerEarthScraper.scrape()
  ├→ UnstopScraper.scrape()
  └→ MLHScraper.scrape()
  ├→ Run through AI extraction
  ├→ Insert/update in database
  └→ Log success/failure

Every 48 hours:
  OpportunityService.deduplicate_opportunities()
  ├→ Find duplicates (same title + company)
  ├→ Keep newest, delete older
  └→ Clean up embeddings if orphaned
```

---

## API Routing Structure

```
/api
├── /opportunities
│   ├── GET / → List with pagination & filters
│   ├── GET /trending → Get trending opportunities
│   ├── GET /{id} → Get single opportunity
│   └── GET /type/{type} → Filter by type
├── /search
│   ├── GET / → Keyword search (full-text)
│   ├── GET /semantic → Semantic search (embeddings)
│   └── GET /ai-recommendations → AI-reranked results
├── /saved
│   ├── GET / → User's saved opportunities
│   ├── POST /{id} → Save opportunity
│   ├── DELETE /{id} → Remove saved
│   └── GET /check/{id} → Is saved?
└── /health
    └── GET / → Health check
```

---

## Database Schema Details

### Opportunities Table

```sql
CREATE TABLE opportunities (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,          -- "React Developer Internship"
    company VARCHAR(255) NOT NULL,        -- "Tech Corp"
    description TEXT NOT NULL,            -- Full description
    opportunity_type VARCHAR(100),        -- internship | hackathon | ...
    deadline TIMESTAMP,                   -- When to apply by
    location VARCHAR(255),                -- City/Country
    is_remote BOOLEAN,                    -- Remote option?
    eligibility JSONB,                    -- ["2nd year+", "DSA knowledge"]
    skills_required JSONB,                -- ["React", "JavaScript", "CSS"]
    summary TEXT,                         -- AI-generated 2-3 sentence summary
    apply_link VARCHAR(500),              -- Where to apply
    source_url VARCHAR(500),              -- Original listing URL
    source_platform VARCHAR(100),         -- devfolio | hackerearth | ...
    status VARCHAR(50),                   -- active | expired | archived
    is_verified BOOLEAN,                  -- Link verified?
    created_at TIMESTAMP,                 -- When added to platform
    updated_at TIMESTAMP,                 -- Last update
    last_verified_at TIMESTAMP,           -- Last link check
    raw_data JSONB,                       -- Original scraped data
    embedding_id INTEGER,                 -- Reference to embeddings table
    relevance_score FLOAT                 -- For ranking/filtering
);
```

### Embeddings Table (pgvector)

```sql
CREATE TABLE embeddings (
    id SERIAL PRIMARY KEY,
    entity_type VARCHAR(50),              -- opportunity | user_query
    entity_id INTEGER,                    -- Which opportunity/query
    text VARCHAR(2000),                   -- Text that was embedded
    embedding vector(1536),               -- The actual vector (pgvector)
    created_at TIMESTAMP,                 -- When generated
    metadata JSONB                        -- Extra info (model version, etc.)
);
```

### Users Table

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE,            -- User email
    username VARCHAR(255) UNIQUE,         -- Unique username
    hashed_password VARCHAR(255),         -- For email/password auth
    full_name VARCHAR(255),               -- Display name
    college VARCHAR(255),                 -- Which college?
    batch_year INTEGER,                   -- 2024 | 2025 | 2026
    is_verified_student BOOLEAN,          -- Email verified?
    is_admin BOOLEAN,                     -- Admin powers?
    google_id VARCHAR(255),               -- For Google OAuth
    oauth_provider VARCHAR(50),           -- Which OAuth provider?
    created_at TIMESTAMP,                 -- Account creation
    last_login_at TIMESTAMP               -- Last activity
);
```

### Saved Opportunities Table

```sql
CREATE TABLE saved_opportunities (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,             -- Which user?
    opportunity_id INTEGER NOT NULL,      -- Which opportunity?
    saved_at TIMESTAMP,                   -- When saved?
    UNIQUE (user_id, opportunity_id)      -- One save per user-opp pair
);
```

### Scrape Logs Table

```sql
CREATE TABLE scrape_logs (
    id SERIAL PRIMARY KEY,
    source VARCHAR(100),                  -- devfolio | hackerearth | ...
    status VARCHAR(50),                   -- success | failed | partial
    opportunities_found INTEGER,          -- How many found?
    opportunities_added INTEGER,          -- How many new?
    opportunities_updated INTEGER,        -- How many updated?
    error_message TEXT,                   -- If failed, why?
    started_at TIMESTAMP,                 -- When scrape started
    completed_at TIMESTAMP,               -- When scrape finished
    created_at TIMESTAMP                  -- Log creation time
);
```

---

## Indexing Strategy

```sql
-- Single column indexes for filtering
CREATE INDEX idx_opportunity_status ON opportunities(status);
CREATE INDEX idx_opportunity_type ON opportunities(opportunity_type);
CREATE INDEX idx_deadline ON opportunities(deadline);
CREATE INDEX idx_is_remote ON opportunities(is_remote);

-- Composite indexes for common queries
CREATE INDEX idx_type_status ON opportunities(opportunity_type, status);
CREATE INDEX idx_deadline_status ON opportunities(deadline, status);

-- For sorting
CREATE INDEX idx_created_at ON opportunities(created_at DESC);

-- Foreign key indexes
CREATE INDEX idx_saved_user ON saved_opportunities(user_id);
CREATE INDEX idx_saved_opp ON saved_opportunities(opportunity_id);
CREATE INDEX idx_emb_entity ON embeddings(entity_type, entity_id);

-- Vector similarity (pgvector specific)
-- Automatically created for column type vector(1536)
```

---

## AI/ML Integration Points

### 1. OpenAI API Calls

**Text Extraction & Classification:**
- Model: `gpt-3.5-turbo`
- Tokens: ~300-500 per extraction
- Cost: ~$0.001 per opportunity
- Cached for: Immediate use

**Use Cases:**
- Extract structure from raw opportunity text
- Classify opportunity type
- Generate summaries
- Rerank search results

### 2. Embeddings Generation

**Model:** `text-embedding-3-small`
- Dimension: 1536
- Cost: $0.02 per 1M tokens (~50k opportunities)
- Speed: ~100ms per embedding

**Storage:** pgvector in PostgreSQL
- Index type: IVFFlat or HNSW
- Similarity metric: Cosine distance
- Query time: <100ms for 10k vectors

### 3. Semantic Search Process

```python
# Input: User query string
query = "React internships in India"

# Step 1: Generate embedding
query_embedding = EmbeddingService.generate_query_embedding(query)
# Returns: 1536-D vector

# Step 2: PostgreSQL similarity search
results = db.query(Opportunity).join(
    Embedding,
    Opportunity.embedding_id == Embedding.id
).order_by(
    Embedding.embedding.cosine_distance(query_embedding)
).limit(20).all()

# Step 3: Optional AI reranking
final_results = AIExtractionService.rerank_opportunities(
    query, 
    results, 
    top_k=5
)

# Output: Ranked list of opportunities
```

---

## Security Architecture

```
Frontend                          Backend
─────────────────────────────────────────────
User Input                        Input Validation
    ↓                                 ↓
Sanitize                         SQLAlchemy ORM
    ↓                            (SQL Injection Prevention)
HTTPS Only                            ↓
    ↓                            Parameterized Queries
JWT Token                             ↓
    ↓                            CORS Restrictions
API Request                           ↓
    ↓                            Rate Limiting Ready
                                      ↓
                                Environment Variables
                                (No secrets in code)
                                      ↓
                                Database
                                (Prepared Statements)
```

---

## Performance Optimization Techniques

### Frontend
- Code splitting by route
- Lazy loading of images
- Query caching (5 min stale time)
- Pagination (12-20 items per page)
- Skeleton loaders for perceived performance
- CSS purging (TailwindCSS only includes used classes)

### Backend
- Connection pooling (10 min/20 max)
- Database indexes on commonly filtered columns
- Pagination to reduce memory
- Caching headers in responses
- GZIP compression
- Async/await for I/O operations

### Database
- B-tree indexes on filtered columns
- Vector indexes on embeddings
- Query optimization
- Vacuum & analyze regularly
- Connection pooling in SQLAlchemy

---

## Deployment Architecture

```
┌─────────────────────────────────────────┐
│  User Browser / Mobile App              │
└─────────────────────────────────────────┘
                    ↓ HTTPS
┌─────────────────────────────────────────┐
│  CDN / Static Assets                    │
│  (CloudFront / Cloudflare)              │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  Load Balancer                          │
│  (ALB / Nginx)                          │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  Frontend Containers                    │
│  (React + Nginx) × N replicas           │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  API Load Balancer                      │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  Backend Containers                     │
│  (FastAPI) × N replicas                 │
│  + Background Job Worker × M replicas   │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  PostgreSQL Primary                     │
│  + Read Replicas × K                    │
│  + Automated Backups                    │
└─────────────────────────────────────────┘
```

---

## Monitoring & Observability

**Logs:** 
- Application logs → ELK/CloudWatch
- Database queries → slow_log
- Requests → Access logs

**Metrics:**
- API response time
- Database query time
- Scraper success rate
- Search latency
- Uptime percentage

**Alerts:**
- API error rate > 5%
- Database connection pool exhaustion
- Scraper failures
- Disk usage > 80%

---

## Technology Decisions & Rationale

| Component | Choice | Why |
|-----------|--------|-----|
| Frontend Framework | React | Ecosystem, learning curve, community |
| Build Tool | Vite | Fast refresh, optimal bundle size |
| Styling | TailwindCSS | Utility-first, minimal CSS |
| State Mgmt | Zustand | Lightweight, simple API |
| Data Fetching | TanStack Query | Caching, sync, background sync |
| Backend | FastAPI | Fast, automatic docs, modern Python |
| Database | PostgreSQL | Reliable, ACID, pgvector support |
| Vector DB | pgvector | Integrated, no separate service |
| Background Jobs | APScheduler | Simple, in-process for MVP |
| Containers | Docker | Portability, consistency |
| Orchestration | Docker Compose | Simple for MVP, upgradeable to K8s |

---

## Scalability Path

**MVP (Current):**
- Single server deployment
- PostgreSQL with local backups
- In-process background jobs

**Phase 2 (10k+ users):**
- Docker Swarm / Kubernetes
- Redis for caching
- Separate job worker containers
- Database read replicas
- CDN for static assets

**Phase 3 (100k+ users):**
- Horizontal scaling of API servers
- Dedicated database cluster
- Message queue (Redis/RabbitMQ)
- Microservices separation
- Advanced caching strategy
