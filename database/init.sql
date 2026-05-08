-- Create pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Opportunities table
CREATE TABLE IF NOT EXISTS opportunities (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    opportunity_type VARCHAR(100) NOT NULL,
    deadline TIMESTAMP,
    location VARCHAR(255),
    is_remote BOOLEAN DEFAULT FALSE,
    eligibility JSONB DEFAULT '[]',
    skills_required JSONB DEFAULT '[]',
    summary TEXT,
    apply_link VARCHAR(500) NOT NULL,
    source_url VARCHAR(500),
    source_platform VARCHAR(100),
    status VARCHAR(50) DEFAULT 'active',
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_verified_at TIMESTAMP,
    raw_data JSONB,
    embedding_id INTEGER,
    relevance_score FLOAT DEFAULT 0.0,
    INDEX idx_opportunity_type_status (opportunity_type, status),
    INDEX idx_deadline_status (deadline, status),
    INDEX idx_created_at (created_at)
);

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255),
    full_name VARCHAR(255),
    profile_picture_url VARCHAR(500),
    bio TEXT,
    college VARCHAR(255),
    batch_year INTEGER,
    is_verified_student BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    google_id VARCHAR(255) UNIQUE,
    oauth_provider VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_username (username)
);

-- Saved opportunities table
CREATE TABLE IF NOT EXISTS saved_opportunities (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    opportunity_id INTEGER NOT NULL REFERENCES opportunities(id),
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, opportunity_id),
    INDEX idx_user_id (user_id),
    INDEX idx_opportunity_id (opportunity_id)
);

-- Embeddings table
CREATE TABLE IF NOT EXISTS embeddings (
    id SERIAL PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL,
    entity_id INTEGER,
    text VARCHAR(2000) NOT NULL,
    embedding vector(1536) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'
);

-- Scrape logs table
CREATE TABLE IF NOT EXISTS scrape_logs (
    id SERIAL PRIMARY KEY,
    source VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    opportunities_found INTEGER DEFAULT 0,
    opportunities_added INTEGER DEFAULT 0,
    opportunities_updated INTEGER DEFAULT 0,
    error_message TEXT,
    started_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_opp_status ON opportunities(status);
CREATE INDEX IF NOT EXISTS idx_opp_type ON opportunities(opportunity_type);
CREATE INDEX IF NOT EXISTS idx_opp_deadline ON opportunities(deadline);
CREATE INDEX IF NOT EXISTS idx_opp_remote ON opportunities(is_remote);
CREATE INDEX IF NOT EXISTS idx_emb_entity ON embeddings(entity_type, entity_id);
