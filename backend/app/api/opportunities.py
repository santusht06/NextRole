from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.opportunity import Opportunity
from app.services.opportunity import OpportunityService
from typing import Optional, List

router = APIRouter(prefix="/api/opportunities", tags=["opportunities"])


class OpportunityResponse:
    pass


@router.get("/")
async def list_opportunities(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    opportunity_type: Optional[str] = None,
    location: Optional[str] = None,
    is_remote: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    """List all active opportunities with pagination and filters"""

    opportunities, total = OpportunityService.search_opportunities(
        db,
        opportunity_type=opportunity_type,
        location=location,
        is_remote=is_remote,
        skip=skip,
        limit=limit,
    )

    return {
        "data": [opp.to_dict() for opp in opportunities],
        "pagination": {"skip": skip, "limit": limit, "total": total},
    }


@router.get("/trending")
async def get_trending(
    days: int = Query(7, ge=1, le=30),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """Get trending opportunities"""

    opportunities = OpportunityService.get_trending_opportunities(
        db, days=days, limit=limit
    )

    return {"data": [opp.to_dict() for opp in opportunities]}


@router.get("/{opportunity_id}")
async def get_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    """Get a specific opportunity"""

    opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()

    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    return opportunity.to_dict()


@router.get("/type/{opportunity_type}")
async def get_by_type(
    opportunity_type: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Get opportunities by type"""

    opportunities, total = OpportunityService.search_opportunities(
        db, opportunity_type=opportunity_type, skip=skip, limit=limit
    )

    return {
        "data": [opp.to_dict() for opp in opportunities],
        "pagination": {"skip": skip, "limit": limit, "total": total},
    }
