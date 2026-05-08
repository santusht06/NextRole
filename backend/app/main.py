from fastapi import FastAPI, Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZIPMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.database import engine, Base
from app.api import health, opportunities, search, saved
from app.workers.jobs import BackgroundJobs
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle
    Startup: Initialize background jobs
    Shutdown: Stop background jobs
    """
    # Startup
    BackgroundJobs.init_scheduler()
    logger.info("Application startup complete")
    
    yield
    
    # Shutdown
    BackgroundJobs.stop_scheduler()
    logger.info("Application shutdown complete")

# Create FastAPI app
app = FastAPI(
    title="Student Opportunities API",
    description="AI-powered platform for discovering student opportunities",
    version="1.0.0",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(GZIPMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(opportunities.router)
app.include_router(search.router)
app.include_router(saved.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
