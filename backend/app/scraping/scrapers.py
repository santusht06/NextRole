import requests
from bs4 import BeautifulSoup
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.opportunity import Opportunity
from app.models.scrape_log import ScrapeLog
from app.services.opportunity import OpportunityService
from typing import List, Dict, Any
import json

class BaseScraper:
    """Base class for all scrapers"""
    
    def __init__(self):
        self.source = "unknown"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
    
    def log_scrape(self, db: Session, status: str, opportunities: List[Dict], error: str = None):
        """Log scraping attempt"""
        
        log = ScrapeLog(
            source=self.source,
            status=status,
            opportunities_found=len(opportunities),
            opportunities_added=len([o for o in opportunities if o.get("new")]),
            opportunities_updated=len([o for o in opportunities if not o.get("new")]),
            error_message=error,
            started_at=datetime.utcnow(),
            completed_at=datetime.utcnow()
        )
        
        db.add(log)
        db.commit()
        
        return log
    
    def fetch_page(self, url: str) -> str:
        """Fetch page content"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return None

class DevfolioScraper(BaseScraper):
    """Scraper for Devfolio hackathons"""
    
    def __init__(self):
        super().__init__()
        self.source = "devfolio"
        self.base_url = "https://devfolio.co/api/events"
    
    def scrape(self, db: Session) -> List[Opportunity]:
        """
        Scrape Devfolio hackathons
        Note: This is a simplified example. Devfolio may require API authentication.
        """
        
        opportunities = []
        try:
            # In production, use proper API with authentication
            # This is a mock implementation
            response = self.session.get(f"{self.base_url}?limit=50", timeout=10)
            data = response.json()
            
            for event in data.get("events", []):
                # Check if already exists
                existing = db.query(Opportunity).filter(
                    Opportunity.source_url == event.get("url")
                ).first()
                
                opportunity_data = {
                    "title": event.get("name", ""),
                    "company": "Devfolio",
                    "description": event.get("description", ""),
                    "opportunity_type": "hackathon",
                    "deadline": datetime.fromisoformat(event.get("end_date")) if event.get("end_date") else None,
                    "location": event.get("city", ""),
                    "is_remote": event.get("is_remote", False),
                    "apply_link": event.get("url", ""),
                    "source_url": event.get("url", ""),
                    "source_platform": self.source,
                    "status": "active",
                    "raw_data": event,
                    "new": existing is None
                }
                
                if not existing:
                    opp = OpportunityService.create_opportunity(db, **opportunity_data)
                
                opportunities.append(opportunity_data)
        
        except Exception as e:
            print(f"Devfolio scrape error: {str(e)}")
            self.log_scrape(db, "failed", opportunities, str(e))
            return opportunities
        
        self.log_scrape(db, "success", opportunities)
        return opportunities

class HackerEarthScraper(BaseScraper):
    """Scraper for HackerEarth opportunities"""
    
    def __init__(self):
        super().__init__()
        self.source = "hackerearth"
        self.base_url = "https://www.hackerearth.com/api/community/opportunities"
    
    def scrape(self, db: Session) -> List[Opportunity]:
        """Scrape HackerEarth opportunities"""
        
        opportunities = []
        try:
            # Mock API call
            response = self.session.get(self.base_url, timeout=10)
            data = response.json()
            
            for opp in data.get("opportunities", []):
                existing = db.query(Opportunity).filter(
                    Opportunity.source_url == opp.get("url")
                ).first()
                
                opportunity_data = {
                    "title": opp.get("title", ""),
                    "company": opp.get("company", "HackerEarth"),
                    "description": opp.get("description", ""),
                    "opportunity_type": opp.get("type", "coding_contest"),
                    "deadline": datetime.fromisoformat(opp.get("deadline")) if opp.get("deadline") else None,
                    "location": opp.get("location", ""),
                    "is_remote": opp.get("remote", False),
                    "apply_link": opp.get("url", ""),
                    "source_url": opp.get("url", ""),
                    "source_platform": self.source,
                    "status": "active",
                    "raw_data": opp,
                    "new": existing is None
                }
                
                if not existing:
                    opp_obj = OpportunityService.create_opportunity(db, **opportunity_data)
                
                opportunities.append(opportunity_data)
        
        except Exception as e:
            print(f"HackerEarth scrape error: {str(e)}")
            self.log_scrape(db, "failed", opportunities, str(e))
            return opportunities
        
        self.log_scrape(db, "success", opportunities)
        return opportunities

class UnstopScraper(BaseScraper):
    """Scraper for Unstop (formerly HackerEarth Challenges) opportunities"""
    
    def __init__(self):
        super().__init__()
        self.source = "unstop"
        self.base_url = "https://unstop.com/api/opportunities"
    
    def scrape(self, db: Session) -> List[Opportunity]:
        """Scrape Unstop opportunities"""
        
        opportunities = []
        try:
            # Mock API implementation
            filters = {
                "category": ["internship", "hackathon", "hiring_challenge"],
                "status": "active"
            }
            
            response = self.session.get(
                self.base_url,
                params=filters,
                timeout=10
            )
            data = response.json()
            
            for opp in data.get("opportunities", []):
                existing = db.query(Opportunity).filter(
                    Opportunity.source_url == opp.get("url")
                ).first()
                
                opportunity_data = {
                    "title": opp.get("title", ""),
                    "company": opp.get("company_name", ""),
                    "description": opp.get("description", ""),
                    "opportunity_type": opp.get("category", "internship"),
                    "deadline": datetime.fromisoformat(opp.get("deadline")) if opp.get("deadline") else None,
                    "location": opp.get("location", ""),
                    "is_remote": "Remote" in opp.get("location", ""),
                    "apply_link": opp.get("apply_url", ""),
                    "source_url": opp.get("url", ""),
                    "source_platform": self.source,
                    "status": "active",
                    "raw_data": opp,
                    "new": existing is None
                }
                
                if not existing:
                    opp_obj = OpportunityService.create_opportunity(db, **opportunity_data)
                
                opportunities.append(opportunity_data)
        
        except Exception as e:
            print(f"Unstop scrape error: {str(e)}")
            self.log_scrape(db, "failed", opportunities, str(e))
            return opportunities
        
        self.log_scrape(db, "success", opportunities)
        return opportunities

class MLHScraper(BaseScraper):
    """Scraper for MLH (Major League Hacking) hackathons"""
    
    def __init__(self):
        super().__init__()
        self.source = "mlh"
        self.base_url = "https://api.mlh.io/events"
    
    def scrape(self, db: Session) -> List[Opportunity]:
        """Scrape MLH hackathons"""
        
        opportunities = []
        try:
            # MLH API
            response = self.session.get(f"{self.base_url}?status=upcoming", timeout=10)
            data = response.json()
            
            for event in data.get("events", []):
                existing = db.query(Opportunity).filter(
                    Opportunity.source_url == event.get("url")
                ).first()
                
                opportunity_data = {
                    "title": event.get("name", ""),
                    "company": "MLH",
                    "description": event.get("description", ""),
                    "opportunity_type": "hackathon",
                    "deadline": datetime.fromisoformat(event.get("end_date")) if event.get("end_date") else None,
                    "location": f"{event.get('city', '')}, {event.get('country', '')}",
                    "is_remote": event.get("mode", "") == "remote",
                    "apply_link": event.get("url", ""),
                    "source_url": event.get("url", ""),
                    "source_platform": self.source,
                    "status": "active",
                    "raw_data": event,
                    "new": existing is None
                }
                
                if not existing:
                    opp_obj = OpportunityService.create_opportunity(db, **opportunity_data)
                
                opportunities.append(opportunity_data)
        
        except Exception as e:
            print(f"MLH scrape error: {str(e)}")
            self.log_scrape(db, "failed", opportunities, str(e))
            return opportunities
        
        self.log_scrape(db, "success", opportunities)
        return opportunities

def run_all_scrapers(db: Session) -> Dict[str, Any]:
    """Run all scrapers and return results"""
    
    scrapers = [
        DevfolioScraper(),
        HackerEarthScraper(),
        UnstopScraper(),
        MLHScraper()
    ]
    
    results = {
        "total_opportunities": 0,
        "total_added": 0,
        "scrapers": {}
    }
    
    for scraper in scrapers:
        try:
            opportunities = scraper.scrape(db)
            added = len([o for o in opportunities if o.get("new")])
            
            results["scrapers"][scraper.source] = {
                "status": "success",
                "found": len(opportunities),
                "added": added
            }
            results["total_opportunities"] += len(opportunities)
            results["total_added"] += added
        
        except Exception as e:
            results["scrapers"][scraper.source] = {
                "status": "failed",
                "error": str(e)
            }
    
    return results
