"""RAG (Retrieval Augmented Generation) service for semantic search."""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from pgvector.sqlalchemy import Vector
from datetime import datetime
from typing import List, Tuple, Optional, Dict, Any
import logging

from app.models.opportunity import Opportunity
from app.models.embedding import Embedding
from app.services.embedding import EmbeddingService
from app.services.ai_extraction import AIExtractionService
from app.core.config import settings

logger = logging.getLogger(__name__)


class RAGService:
    """Service for Retrieval Augmented Generation with semantic search."""

    @staticmethod
    def semantic_search(
        db: Session,
        query: str,
        limit: int = 50,
        filters: Optional[Dict[str, Any]] = None,
        threshold: Optional[float] = None,
    ) -> List[Opportunity]:
        """
        Perform semantic search using embeddings.

        Args:
            db: Database session
            query: Search query string
            limit: Maximum results to return
            filters: Optional filters (type, location, is_remote, etc.)
            threshold: Similarity threshold (0-1)

        Returns:
            List of opportunities sorted by relevance
        """
        try:
            # Generate query embedding
            query_embedding = EmbeddingService.generate_query_embedding(query)

            if not query_embedding or all(v == 0 for v in query_embedding):
                logger.warning("Failed to generate query embedding")
                return []

            # Build base query
            query_obj = db.query(
                Opportunity,
                Embedding.embedding.cosine_distance(query_embedding).label(
                    "similarity"
                ),
            ).join(
                Embedding,
                and_(
                    Embedding.entity_type == "opportunity",
                    Embedding.entity_id == Opportunity.id,
                ),
            )

            # Apply filters
            filters = filters or {}
            filters["status"] = "active"  # Always filter for active only

            for key, value in filters.items():
                if hasattr(Opportunity, key):
                    column = getattr(Opportunity, key)
                    if isinstance(value, list):
                        query_obj = query_obj.filter(column.in_(value))
                    else:
                        query_obj = query_obj.filter(column == value)

            # Apply threshold if provided
            if threshold is None:
                threshold = settings.SEMANTIC_SEARCH_THRESHOLD

            # Execute query and get results
            results = query_obj.order_by("similarity").limit(limit * 2).all()

            # Filter by threshold and rerank
            opportunities = []
            for opp, similarity in results:
                # Convert distance to similarity score (cosine distance: 0-2, we want 0-1)
                similarity_score = max(0, 1 - similarity)

                if similarity_score >= threshold:
                    opp.relevance_score = similarity_score
                    opportunities.append(opp)

                if len(opportunities) >= limit:
                    break

            return opportunities

        except Exception as e:
            logger.error(f"Error in semantic search: {str(e)}")
            return []

    @staticmethod
    def hybrid_search(
        db: Session,
        query: str,
        limit: int = 50,
        filters: Optional[Dict[str, Any]] = None,
        semantic_weight: float = 0.7,
        keyword_weight: float = 0.3,
    ) -> List[Opportunity]:
        """
        Perform hybrid search combining semantic and keyword search.

        Args:
            db: Database session
            query: Search query
            limit: Maximum results
            filters: Optional filters
            semantic_weight: Weight for semantic search (0-1)
            keyword_weight: Weight for keyword search (0-1)

        Returns:
            Hybrid search results
        """
        # Get semantic results
        semantic_results = RAGService.semantic_search(
            db, query, limit=limit, filters=filters
        )

        # Get keyword results
        keyword_results = RAGService.keyword_search(
            db, query, limit=limit, filters=filters
        )

        # Merge and score
        results_dict = {}

        for i, opp in enumerate(semantic_results):
            score = (1 - i / len(semantic_results)) * semantic_weight
            if opp.id not in results_dict:
                results_dict[opp.id] = {"opp": opp, "score": 0}
            results_dict[opp.id]["score"] += score

        for i, opp in enumerate(keyword_results):
            score = (1 - i / len(keyword_results)) * keyword_weight
            if opp.id not in results_dict:
                results_dict[opp.id] = {"opp": opp, "score": 0}
            results_dict[opp.id]["score"] += score

        # Sort by combined score
        sorted_results = sorted(
            results_dict.values(), key=lambda x: x["score"], reverse=True
        )

        return [r["opp"] for r in sorted_results[:limit]]

    @staticmethod
    def keyword_search(
        db: Session,
        query: str,
        limit: int = 50,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Opportunity]:
        """
        Perform traditional keyword search.

        Args:
            db: Database session
            query: Search query
            limit: Maximum results
            filters: Optional filters

        Returns:
            Keyword search results
        """
        query_terms = query.lower().split()

        q = db.query(Opportunity)

        # Apply filters
        filters = filters or {}
        filters["status"] = "active"

        for key, value in filters.items():
            if hasattr(Opportunity, key):
                column = getattr(Opportunity, key)
                if isinstance(value, list):
                    q = q.filter(column.in_(value))
                else:
                    q = q.filter(column == value)

        # Search in title, description, company, skills
        conditions = []
        for term in query_terms:
            conditions.append(
                or_(
                    Opportunity.title.ilike(f"%{term}%"),
                    Opportunity.description.ilike(f"%{term}%"),
                    Opportunity.company.ilike(f"%{term}%"),
                    func.cast(Opportunity.skills_required, str).ilike(f"%{term}%"),
                )
            )

        if conditions:
            q = q.filter(or_(*conditions))

        return q.order_by(Opportunity.created_at.desc()).limit(limit).all()

    @staticmethod
    def search_with_reranking(
        db: Session,
        query: str,
        limit: int = 50,
        filters: Optional[Dict[str, Any]] = None,
        use_ai_rerank: bool = True,
    ) -> List[Opportunity]:
        """
        Perform search with optional AI-based reranking.

        Args:
            db: Database session
            query: Search query
            limit: Maximum results
            filters: Optional filters
            use_ai_rerank: Whether to use AI for reranking (more expensive)

        Returns:
            Reranked search results
        """
        # Get initial results
        results = RAGService.hybrid_search(db, query, limit=limit * 2, filters=filters)

        if not use_ai_rerank or not results:
            return results[:limit]

        # AI-based reranking
        try:
            reranked = AIExtractionService.rerank_opportunities(query, results)
            return reranked[:limit]
        except Exception as e:
            logger.error(f"Error in AI reranking: {str(e)}")
            return results[:limit]

    @staticmethod
    def update_embeddings(db: Session, opportunity_id: Optional[int] = None):
        """
        Update embeddings for opportunities.

        Args:
            db: Database session
            opportunity_id: Optional specific opportunity ID to update
        """
        try:
            if opportunity_id:
                opportunities = (
                    db.query(Opportunity).filter(Opportunity.id == opportunity_id).all()
                )
            else:
                # Update embeddings older than 30 days or missing
                opportunities = (
                    db.query(Opportunity).filter(Opportunity.status == "active").all()
                )

            updated_count = 0
            for opp in opportunities:
                try:
                    # Generate new embedding
                    embedding_vector = EmbeddingService.generate_opportunity_embedding(
                        opp.title,
                        opp.description,
                        opp.company,
                        opp.skills_required,
                    )

                    # Delete old embedding if exists
                    if opp.embedding_id:
                        db.query(Embedding).filter(
                            Embedding.id == opp.embedding_id
                        ).delete()

                    # Create new embedding
                    embedding = Embedding(
                        entity_type="opportunity",
                        entity_id=opp.id,
                        text=f"{opp.title} {opp.company} {' '.join(opp.skills_required)}",
                        embedding=embedding_vector,
                    )
                    db.add(embedding)
                    opp.embedding_id = embedding.id
                    updated_count += 1

                except Exception as e:
                    logger.error(
                        f"Error updating embedding for opportunity {opp.id}: {str(e)}"
                    )
                    continue

            db.commit()
            logger.info(f"Updated embeddings for {updated_count} opportunities")
            return updated_count

        except Exception as e:
            logger.error(f"Error in update_embeddings: {str(e)}")
            db.rollback()
            return 0

    @staticmethod
    def get_related_opportunities(
        db: Session, opportunity_id: int, limit: int = 5
    ) -> List[Opportunity]:
        """
        Get opportunities related to a specific opportunity.

        Args:
            db: Database session
            opportunity_id: ID of the opportunity
            limit: Maximum results

        Returns:
            List of related opportunities
        """
        try:
            opportunity = (
                db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
            )

            if not opportunity:
                return []

            # Use skills and type as search basis
            search_query = f"{opportunity.opportunity_type} {' '.join(opportunity.skills_required)}"

            results = RAGService.semantic_search(
                db,
                search_query,
                limit=limit + 1,  # +1 to exclude the original
                filters={"opportunity_type": opportunity.opportunity_type},
            )

            # Remove the original opportunity
            results = [r for r in results if r.id != opportunity_id]

            return results[:limit]

        except Exception as e:
            logger.error(f"Error getting related opportunities: {str(e)}")
            return []
