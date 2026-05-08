from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.opportunity import OpportunityService
from app.services.ai_extraction import AIExtractionService
from typing import Optional

router = APIRouter(prefix="/api/search", tags=["search"])


@router.get("/")
async def search_opportunities(
    q: str = Query(..., min_length=2, max_length=500),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    opportunity_type: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Keyword search for opportunities"""

    opportunities, total = OpportunityService.search_opportunities(
        db, query=q, opportunity_type=opportunity_type, skip=skip, limit=limit
    )

    return {
        "query": q,
        "data": [opp.to_dict() for opp in opportunities],
        "pagination": {"skip": skip, "limit": limit, "total": total},
    }


@router.get("/semantic")
async def semantic_search(
    q: str = Query(..., min_length=2, max_length=500),
    limit: int = Query(20, ge=1, le=100),
    opportunity_type: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Semantic search using AI embeddings
    Finds opportunities similar in meaning, not just keywords
    """

    opportunities = OpportunityService.semantic_search(
        db, query=q, opportunity_type=opportunity_type, limit=limit
    )

    return {
        "query": q,
        "search_type": "semantic",
        "data": [opp.to_dict() for opp in opportunities],
        "count": len(opportunities),
    }


@router.get("/ai-recommendations")
async def get_ai_recommendations(
    query: str = Query(..., min_length=2, max_length=500),
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
):
    """
    Get AI-reranked recommendations based on query
    Uses semantic search + AI reranking for best results
    """

    # First do semantic search to get candidates
    opportunities = OpportunityService.semantic_search(
        db,
        query=query,
        limit=limit * 2,  # Get more candidates for reranking
    )

    # Convert to format for reranking
    opp_data = [
        {
            "id": opp.id,
            "title": opp.title,
            "summary": opp.summary or opp.description[:100],
        }
        for opp in opportunities
    ]

    # Use AI to rerank
    reranked = AIExtractionService.rerank_opportunities(query, opp_data, top_k=limit)

    # Get full opportunity data for reranked results
    reranked_ids = [opp["id"] for opp in reranked]
    result_opportunities = (
        db.query(Opportunity).filter(Opportunity.id.in_(reranked_ids)).all()
    )

    # Sort by reranked order
    result_dict = {opp.id: opp for opp in result_opportunities}
    sorted_opportunities = [result_dict[id] for id in reranked_ids if id in result_dict]

    return {
        "query": query,
        "search_type": "ai-recommendations",
        "data": [opp.to_dict() for opp in sorted_opportunities],
        "reasoning": "Results ranked by AI for relevance to your query",
    }
