import json
from openai import OpenAI
from app.core.config import settings
from typing import Optional, Dict, Any

client = OpenAI(api_key=settings.OPENAI_API_KEY)


class AIExtractionService:
    """Service for extracting structured data from opportunity descriptions using OpenAI"""

    @staticmethod
    def extract_opportunity_info(
        title: str, description: str, raw_html: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Extract structured information from opportunity using AI
        Returns JSON with: type, deadline, location, eligibility, skills, summary
        """

        content = f"""
Extract structured information from this opportunity:

Title: {title}
Description: {description}

Please extract and return a JSON object with:
- type: (internship/hackathon/contest/graduate_program/hiring_challenge)
- deadline: (YYYY-MM-DD format or null if not found)
- location: (city/country or null)
- is_remote: (true/false)
- eligibility: (list of eligibility criteria as strings)
- skills_required: (list of skills as strings)
- summary: (2-3 sentence summary)

Return ONLY valid JSON, no markdown formatting.
"""

        try:
            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert recruiter analyzing opportunity listings. Extract key information and return valid JSON only.",
                    },
                    {"role": "user", "content": content},
                ],
                temperature=0.3,
                max_tokens=500,
            )

            result_text = response.choices[0].message.content.strip()

            # Try to parse JSON
            extracted = json.loads(result_text)
            return extracted
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return {
                "type": "internship",
                "deadline": None,
                "location": None,
                "is_remote": False,
                "eligibility": [],
                "skills_required": [],
                "summary": description[:200],
            }
        except Exception as e:
            print(f"Error during AI extraction: {str(e)}")
            return {
                "type": "internship",
                "deadline": None,
                "location": None,
                "is_remote": False,
                "eligibility": [],
                "skills_required": [],
                "summary": description[:200],
            }

    @staticmethod
    def classify_opportunity_type(title: str, description: str) -> str:
        """Classify opportunity type using AI"""

        content = f"""
Classify this opportunity into one category:
Title: {title}
Description: {description[:500]}

Categories:
- internship
- hackathon
- coding_contest
- graduate_program
- hiring_challenge

Return only the category name.
"""

        try:
            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a recruiter. Classify the opportunity type. Reply with only the category name.",
                    },
                    {"role": "user", "content": content},
                ],
                temperature=0.2,
                max_tokens=50,
            )

            category = response.choices[0].message.content.strip().lower()
            valid_categories = [
                "internship",
                "hackathon",
                "coding_contest",
                "graduate_program",
                "hiring_challenge",
            ]
            return category if category in valid_categories else "internship"
        except Exception as e:
            print(f"Error during classification: {str(e)}")
            return "internship"

    @staticmethod
    def generate_semantic_summary(
        title: str, description: str, extracted_info: Dict[str, Any]
    ) -> str:
        """Generate a semantic summary for better searching"""

        content = f"""
Create a brief, searchable summary (50-100 words) of this opportunity:
Title: {title}
Type: {extracted_info.get("type", "opportunity")}
Skills: {", ".join(extracted_info.get("skills_required", []))}
Description: {description[:300]}

Make it clear and concise for students searching.
"""

        try:
            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[{"role": "user", "content": content}],
                temperature=0.4,
                max_tokens=150,
            )

            return response.choices[0].message.content.strip()
        except Exception:
            return f"{title} - {description[:100]}"

    @staticmethod
    def rerank_opportunities(query: str, opportunities: list, top_k: int = 5) -> list:
        """
        Rerank opportunities based on query relevance using AI
        opportunities: list of dicts with 'id', 'title', 'summary'
        """

        if not opportunities:
            return []

        opportunities_text = "\n".join(
            [
                f"{i + 1}. {opp['title']} - {opp['summary'][:100]}"
                for i, opp in enumerate(opportunities[:10])
            ]
        )

        content = f"""
User is searching for: "{query}"

Here are opportunities:
{opportunities_text}

Rank these by relevance to the user's search query. Return ONLY the numbers in order (1-indexed), comma-separated.
For example: 3,1,5,2
"""

        try:
            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a recruiter. Rank opportunities by relevance. Return only numbers.",
                    },
                    {"role": "user", "content": content},
                ],
                temperature=0.1,
                max_tokens=100,
            )

            ranking_str = response.choices[0].message.content.strip()
            ranks = [
                int(x.strip()) - 1
                for x in ranking_str.split(",")
                if x.strip().isdigit()
            ]

            reranked = [opportunities[i] for i in ranks if i < len(opportunities)]
            return reranked[:top_k]
        except Exception:
            return opportunities[:top_k]
