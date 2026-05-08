from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
from app.core.database import SessionLocal
from app.services.opportunity import OpportunityService
from app.scraping.scrapers import run_all_scrapers
import logging

logger = logging.getLogger(__name__)

class BackgroundJobs:
    """Manages background job scheduling"""
    
    scheduler = None
    
    @staticmethod
    def init_scheduler():
        """Initialize and start the scheduler"""
        BackgroundJobs.scheduler = BackgroundScheduler()
        
        # Expire old opportunities every 6 hours
        BackgroundJobs.scheduler.add_job(
            BackgroundJobs.expire_opportunities_job,
            IntervalTrigger(hours=6),
            id="expire_opportunities",
            name="Expire old opportunities",
            replace_existing=True
        )
        
        # Verify apply links every 12 hours
        BackgroundJobs.scheduler.add_job(
            BackgroundJobs.verify_links_job,
            IntervalTrigger(hours=12),
            id="verify_links",
            name="Verify apply links",
            replace_existing=True
        )
        
        # Run scrapers every 24 hours
        BackgroundJobs.scheduler.add_job(
            BackgroundJobs.scrape_opportunities_job,
            IntervalTrigger(hours=24),
            id="scrape_opportunities",
            name="Scrape new opportunities",
            replace_existing=True
        )
        
        # Deduplicate opportunities every 48 hours
        BackgroundJobs.scheduler.add_job(
            BackgroundJobs.deduplicate_job,
            IntervalTrigger(hours=48),
            id="deduplicate",
            name="Deduplicate opportunities",
            replace_existing=True
        )
        
        BackgroundJobs.scheduler.start()
        logger.info("Background scheduler started")
    
    @staticmethod
    def stop_scheduler():
        """Stop the scheduler"""
        if BackgroundJobs.scheduler:
            BackgroundJobs.scheduler.shutdown()
            logger.info("Background scheduler stopped")
    
    @staticmethod
    def expire_opportunities_job():
        """Background job to expire old opportunities"""
        db = SessionLocal()
        try:
            expired_count = OpportunityService.expire_old_opportunities(db)
            logger.info(f"Expired {expired_count} opportunities")
        except Exception as e:
            logger.error(f"Error expiring opportunities: {str(e)}")
        finally:
            db.close()
    
    @staticmethod
    def verify_links_job():
        """Background job to verify apply links"""
        db = SessionLocal()
        try:
            results = OpportunityService.verify_apply_links(db, batch_size=20)
            logger.info(f"Link verification results: {results}")
        except Exception as e:
            logger.error(f"Error verifying links: {str(e)}")
        finally:
            db.close()
    
    @staticmethod
    def scrape_opportunities_job():
        """Background job to scrape new opportunities"""
        db = SessionLocal()
        try:
            results = run_all_scrapers(db)
            logger.info(f"Scraping results: {results}")
        except Exception as e:
            logger.error(f"Error scraping opportunities: {str(e)}")
        finally:
            db.close()
    
    @staticmethod
    def deduplicate_job():
        """Background job to remove duplicate opportunities"""
        db = SessionLocal()
        try:
            removed_count = OpportunityService.deduplicate_opportunities(db)
            logger.info(f"Removed {removed_count} duplicate opportunities")
        except Exception as e:
            logger.error(f"Error deduplicating: {str(e)}")
        finally:
            db.close()
