from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime, timedelta
from app.models.opportunity import Opportunity
from app.models.embedding import Embedding
from app.services.ai_extraction import AIExtractionService
from app.services.embedding import EmbeddingService
from app.core.config import settings
import requests
from typing import Optional, List, Dict, Any


class OpportunityService:
    """Service for managing opportunities"""

    @staticmethod
    def create_opportunity(db: Session, **kwargs) -> Opportunity:
        """Create a new opportunity"""

        # Generate AI-extracted info if not provided
        if "opportunity_type" not in kwargs:
            title = kwargs.get("title", "")
            description = kwargs.get("description", "")
            extracted = AIExtractionService.extract_opportunity_info(title, description)
            kwargs.update(extracted)

        opportunity = Opportunity(**kwargs)
        db.add(opportunity)
        db.commit()
        db.refresh(opportunity)

        # Generate and store embedding
        embedding_vector = EmbeddingService.generate_opportunity_embedding(
            opportunity.title,
            opportunity.description,
            opportunity.company,
            opportunity.skills_required,
        )

        embedding = Embedding(
            entity_type="opportunity",
            entity_id=opportunity.id,
            text=f"{opportunity.title} {opportunity.company} {' '.join(opportunity.skills_required)}",
            embedding=embedding_vector,
        )
        db.add(embedding)
        opportunity.embedding_id = embedding.id
        db.commit()

        return opportunity

    @staticmethod
    def update_opportunity_status(
        db: Session, opportunity_id: int, status: str
    ) -> Optional[Opportunity]:
        """Update opportunity status"""
        opportunity = (
            db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
        )
        if opportunity:
            opportunity.status = status
            opportunity.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(opportunity)
        return opportunity

    @staticmethod
    def expire_old_opportunities(db: Session) -> int:
        """Mark opportunities as expired if deadline has passed"""
        now = datetime.utcnow()

        expired = (
            db.query(Opportunity)
            .filter(and_(Opportunity.deadline < now, Opportunity.status == "active"))
            .all()
        )

        count = 0
        for opp in expired:
            opp.status = "expired"
            opp.updated_at = now
            count += 1

        db.commit()
        return count

    @staticmethod
    def verify_apply_links(db: Session, batch_size: int = 10) -> Dict[str, int]:
        """Verify that apply links are valid"""

        results = {"verified": 0, "broken": 0, "error": 0}

        # Get opportunities that haven't been verified recently
        cutoff_time = datetime.utcnow() - timedelta(days=3)
        opportunities = (
            db.query(Opportunity)
            .filter(
                or_(
                    Opportunity.last_verified_at == None,
                    Opportunity.last_verified_at < cutoff_time,
                ),
                Opportunity.status == "active",
            )
            .limit(batch_size)
            .all()
        )

        for opp in opportunities:
            try:
                response = requests.head(
                    opp.apply_link, timeout=5, allow_redirects=True
                )
                if 200 <= response.status_code < 400:
                    opp.is_verified = True
                    results["verified"] += 1
                else:
                    opp.status = "expired"
                    results["broken"] += 1
            except Exception as e:
                results["error"] += 1

            opp.last_verified_at = datetime.utcnow()

        db.commit()
        return results

    @staticmethod
    def search_opportunities(
        db: Session,
        query: Optional[str] = None,
        opportunity_type: Optional[str] = None,
        location: Optional[str] = None,
        is_remote: Optional[bool] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[List[Opportunity], int]:
        """
        Search opportunities with keyword and metadata filtering
        """

        filter_conditions = [Opportunity.status == "active"]

        # Add optional filters
        if opportunity_type:
            filter_conditions.append(Opportunity.opportunity_type == opportunity_type)

        if location:
            filter_conditions.append(Opportunity.location.ilike(f"%{location}%"))

        if is_remote is not None:
            filter_conditions.append(Opportunity.is_remote == is_remote)

        # Keyword search
        if query:
            search_term = f"%{query}%"
            filter_conditions.append(
                or_(
                    Opportunity.title.ilike(search_term),
                    Opportunity.description.ilike(search_term),
                    Opportunity.company.ilike(search_term),
                    Opportunity.summary.ilike(search_term),
                )
            )

        # Build and execute query
        query_obj = db.query(Opportunity).filter(and_(*filter_conditions))
        total = query_obj.count()

        opportunities = (
            query_obj.order_by(Opportunity.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        return opportunities, total

    @staticmethod
    def semantic_search(
        db: Session, query: str, opportunity_type: Optional[str] = None, limit: int = 20
    ) -> List[Opportunity]:
        """
        Semantic search using embeddings
        1. Generate query embedding
        2. Find similar opportunities using pgvector similarity
        3. Apply metadata filters
        """

        try:
            # Generate query embedding
            query_embedding = EmbeddingService.generate_query_embedding(query)

            # Use pgvector similarity search
            from sqlalchemy import text

            filter_conditions = [Opportunity.status == "active"]
            if opportunity_type:
                filter_conditions.append(
                    Opportunity.opportunity_type == opportunity_type
                )

            # Build base query with metadata filters
            base_query = db.query(Opportunity).filter(and_(*filter_conditions))

            # Join with embeddings and get similarities
            results = (
                db.query(
                    Opportunity,
                    Embedding.embedding.cosine_distance(query_embedding).label(
                        "similarity"
                    ),
                )
                .join(Embedding, Opportunity.embedding_id == Embedding.id)
                .filter(and_(*filter_conditions))
                .order_by("similarity")
                .limit(limit)
                .all()
            )

            return [opp for opp, _ in results]

        except Exception as e:
            print(f"Semantic search error: {str(e)}")
            # Fallback to keyword search
            opportunities, _ = OpportunityService.search_opportunities(
                db, query=query, opportunity_type=opportunity_type, limit=limit
            )
            return opportunities

    @staticmethod
    def get_trending_opportunities(
        db: Session, days: int = 7, limit: int = 10
    ) -> List[Opportunity]:
        """Get trending opportunities from recent additions"""

        cutoff_date = datetime.utcnow() - timedelta(days=days)

        opportunities = (
            db.query(Opportunity)
            .filter(
                and_(
                    Opportunity.status == "active",
                    Opportunity.created_at >= cutoff_date,
                )
            )
            .order_by(Opportunity.created_at.desc())
            .limit(limit)
            .all()
        )

        return opportunities

    @staticmethod
    def deduplicate_opportunities(db: Session) -> int:
        """
        Remove duplicate opportunities
        Considers same title + company as duplicate
        """

        # Find duplicates
        duplicates = (
            db.query(
                Opportunity.title,
                Opportunity.company,
                func.count(Opportunity.id).label("count"),
            )
            .group_by(Opportunity.title, Opportunity.company)
            .filter(func.count(Opportunity.id) > 1)
            .all()
        )

        removed_count = 0

        for title, company, count in duplicates:
            # Keep the newest, remove older ones
            opportunities = (
                db.query(Opportunity)
                .filter(
                    and_(Opportunity.title == title, Opportunity.company == company)
                )
                .order_by(Opportunity.created_at.desc())
                .all()
            )

            # Remove all but the first (newest)
            for opp in opportunities[1:]:
                db.delete(opp)
                removed_count += 1

        db.commit()
        return removed_count
