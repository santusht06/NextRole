from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.saved_opportunity import SavedOpportunity
from app.models.opportunity import Opportunity
from typing import Optional

router = APIRouter(prefix="/api/saved", tags=["saved"])

# For MVP, we'll use a simple in-memory store for current user
# In production, implement proper authentication
CURRENT_USER_ID = 1  # Mock user ID


@router.get("/")
async def get_saved_opportunities(
    skip: int = 0, limit: int = 20, db: Session = Depends(get_db)
):
    """Get user's saved opportunities"""

    saved = (
        db.query(SavedOpportunity)
        .filter(SavedOpportunity.user_id == CURRENT_USER_ID)
        .offset(skip)
        .limit(limit)
        .all()
    )

    opportunity_ids = [s.opportunity_id for s in saved]
    opportunities = (
        db.query(Opportunity).filter(Opportunity.id.in_(opportunity_ids)).all()
    )

    return {"data": [opp.to_dict() for opp in opportunities], "total": len(saved)}


@router.post("/{opportunity_id}")
async def save_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    """Save an opportunity"""

    # Check if opportunity exists
    opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()

    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    # Check if already saved
    existing = (
        db.query(SavedOpportunity)
        .filter(
            SavedOpportunity.user_id == CURRENT_USER_ID,
            SavedOpportunity.opportunity_id == opportunity_id,
        )
        .first()
    )

    if existing:
        raise HTTPException(status_code=400, detail="Already saved")

    saved = SavedOpportunity(user_id=CURRENT_USER_ID, opportunity_id=opportunity_id)
    db.add(saved)
    db.commit()

    return {"message": "Opportunity saved"}


@router.delete("/{opportunity_id}")
async def unsave_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    """Remove saved opportunity"""

    saved = (
        db.query(SavedOpportunity)
        .filter(
            SavedOpportunity.user_id == CURRENT_USER_ID,
            SavedOpportunity.opportunity_id == opportunity_id,
        )
        .first()
    )

    if not saved:
        raise HTTPException(status_code=404, detail="Saved opportunity not found")

    db.delete(saved)
    db.commit()

    return {"message": "Opportunity removed from saved"}


@router.get("/check/{opportunity_id}")
async def check_saved(opportunity_id: int, db: Session = Depends(get_db)):
    """Check if opportunity is saved"""

    saved = (
        db.query(SavedOpportunity)
        .filter(
            SavedOpportunity.user_id == CURRENT_USER_ID,
            SavedOpportunity.opportunity_id == opportunity_id,
        )
        .first()
    )

    return {"is_saved": saved is not None}
