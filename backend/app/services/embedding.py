from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


class EmbeddingService:
    """Service for generating and managing embeddings using OpenAI"""

    EMBEDDING_DIMENSION = 1536  # text-embedding-3-small dimension
    MODEL = "text-embedding-3-small"

    @staticmethod
    def generate_embedding(text: str) -> list:
        """
        Generate embedding for text using OpenAI's text-embedding-3-small
        """
        try:
            # Clean and limit text
            text = text[:8191]  # API limit

            response = client.embeddings.create(
                model=EmbeddingService.MODEL, input=text
            )

            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {str(e)}")
            # Return zero vector as fallback
            return [0.0] * EmbeddingService.EMBEDDING_DIMENSION

    @staticmethod
    def generate_query_embedding(query: str) -> list:
        """Generate embedding for a search query"""
        return EmbeddingService.generate_embedding(query)

    @staticmethod
    def generate_opportunity_embedding(
        title: str, description: str, company: str = "", skills: list = None
    ) -> list:
        """
        Generate combined embedding for opportunity
        Prioritize title and key fields for better search
        """
        skills_text = ", ".join(skills) if skills else ""
        combined_text = f"{title} {company} {skills_text} {description[:500]}"
        return EmbeddingService.generate_embedding(combined_text)

    @staticmethod
    def similarity_search(query_embedding: list, db_embeddings: list) -> list:
        """
        Calculate similarity between query and stored embeddings
        Returns list of (index, similarity_score) tuples
        """
        import math

        def cosine_similarity(vec1, vec2):
            """Calculate cosine similarity between two vectors"""
            if len(vec1) != len(vec2):
                return 0.0

            dot_product = sum(a * b for a, b in zip(vec1, vec2))
            mag1 = math.sqrt(sum(a * a for a in vec1))
            mag2 = math.sqrt(sum(b * b for b in vec2))

            if mag1 == 0 or mag2 == 0:
                return 0.0

            return dot_product / (mag1 * mag2)

        similarities = [
            (i, cosine_similarity(query_embedding, emb))
            for i, emb in enumerate(db_embeddings)
        ]

        return sorted(similarities, key=lambda x: x[1], reverse=True)
