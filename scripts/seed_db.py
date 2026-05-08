#!/usr/bin/env python3
"""
Seed script for populating database with sample opportunities
Run this after creating the database to populate with test data
"""

from datetime import datetime, timedelta
from app.core.database import SessionLocal, engine, Base
from app.models.opportunity import Opportunity
from app.services.opportunity import OpportunityService
import json


def seed_database():
    """Populate database with sample opportunities"""

    # Create tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    sample_opportunities = [
        {
            "title": "Frontend Engineer Internship - React",
            "company": "Tech Startup XYZ",
            "description": "Join our frontend team and build amazing user experiences with React. You'll work on our customer dashboard and collaborate with senior engineers. We're looking for someone passionate about web development.",
            "opportunity_type": "internship",
            "deadline": datetime.utcnow() + timedelta(days=30),
            "location": "San Francisco, CA",
            "is_remote": True,
            "eligibility": [
                "2nd year or above",
                "Basic knowledge of JavaScript",
                "Familiar with React or Vue",
            ],
            "skills_required": ["React", "JavaScript", "CSS", "HTML"],
            "summary": "Build customer dashboards using React. Remote, 30 days deadline.",
            "apply_link": "https://example.com/apply/1",
            "source_url": "https://example.com/job/1",
            "source_platform": "devfolio",
            "status": "active",
            "is_verified": True,
        },
        {
            "title": "Hackathon: AI & Open Data Challenge 2024",
            "company": "Google & World Bank",
            "description": "Build AI solutions using open government data. Win prizes up to $50,000. This hackathon focuses on addressing real-world problems using machine learning and public datasets.",
            "opportunity_type": "hackathon",
            "deadline": datetime.utcnow() + timedelta(days=45),
            "location": "Virtual",
            "is_remote": True,
            "eligibility": [
                "Students of any year",
                "Basic ML knowledge",
                "Team of 2-4 people",
            ],
            "skills_required": [
                "Machine Learning",
                "Python",
                "Data Analysis",
                "API Integration",
            ],
            "summary": "Win $50k building AI solutions with open data. Virtual, Global.",
            "apply_link": "https://example.com/hackathon/1",
            "source_url": "https://example.com/hackathon/1",
            "source_platform": "mlh",
            "status": "active",
            "is_verified": True,
        },
        {
            "title": "CodeChef June Long Challenge",
            "company": "CodeChef",
            "description": "Monthly programming contest with amazing prizes. Code in 60+ languages. Compete with 50,000+ programmers from around the world.",
            "opportunity_type": "coding_contest",
            "deadline": datetime.utcnow() + timedelta(days=10),
            "location": "Online",
            "is_remote": True,
            "eligibility": ["No eligibility restrictions", "Ages 13+"],
            "skills_required": [
                "Problem Solving",
                "Data Structures",
                "Algorithms",
                "Any Programming Language",
            ],
            "summary": "Monthly competitive programming contest. Prizes for top performers.",
            "apply_link": "https://www.codechef.com/contests",
            "source_url": "https://www.codechef.com/contests",
            "source_platform": "hackerearth",
            "status": "active",
            "is_verified": True,
        },
        {
            "title": "Backend Engineer - Python/FastAPI",
            "company": "Fintech Company ABC",
            "description": "Build scalable backend services using Python and FastAPI. Work on payment processing, API design, and database optimization. Great learning opportunity!",
            "opportunity_type": "internship",
            "deadline": datetime.utcnow() + timedelta(days=25),
            "location": "Bangalore",
            "is_remote": False,
            "eligibility": [
                "2nd year and above",
                "Python knowledge",
                "Database basics",
            ],
            "skills_required": ["Python", "FastAPI", "PostgreSQL", "REST APIs"],
            "summary": "Build payment processing backends. Bangalore, on-site.",
            "apply_link": "https://example.com/apply/2",
            "source_url": "https://example.com/job/2",
            "source_platform": "unstop",
            "status": "active",
            "is_verified": True,
        },
        {
            "title": "MS in Computer Science - Full Scholarship",
            "company": "University of Illinois",
            "description": "Full-funded MS program in Computer Science. Tuition + living expenses covered. Exceptional students in AI/ML, Systems, or Security welcome.",
            "opportunity_type": "graduate_program",
            "deadline": datetime.utcnow() + timedelta(days=60),
            "location": "Urbana-Champaign, Illinois",
            "is_remote": False,
            "eligibility": [
                "Bachelor's degree in CS or related field",
                "GRE score",
                "TOEFL (for international)",
            ],
            "skills_required": [
                "Programming",
                "Data Structures",
                "Algorithms",
                "Mathematics",
            ],
            "summary": "Full scholarship MS in CS. World-class faculty and research opportunities.",
            "apply_link": "https://example.com/apply-ms/1",
            "source_url": "https://example.com/ms/1",
            "source_platform": "devfolio",
            "status": "active",
            "is_verified": True,
        },
        {
            "title": "Data Science Hiring Challenge",
            "company": "Analytics Corp",
            "description": "Solve real-world data science problems. Top performers get interviews and potential job offers. Cash prizes for winners.",
            "opportunity_type": "hiring_challenge",
            "deadline": datetime.utcnow() + timedelta(days=15),
            "location": "Remote",
            "is_remote": True,
            "eligibility": ["Strong statistical foundation", "Python/R skills"],
            "skills_required": [
                "Data Science",
                "Python",
                "Statistics",
                "Machine Learning",
            ],
            "summary": "Win interviews and job offers by solving DS challenges.",
            "apply_link": "https://example.com/challenge/1",
            "source_url": "https://example.com/challenge/1",
            "source_platform": "unstop",
            "status": "active",
            "is_verified": True,
        },
        {
            "title": "Mobile App Developer - iOS",
            "company": "Startup Mobile Corp",
            "description": "Develop iOS applications in Swift. Work on a real product used by 100k+ users. Great for building your portfolio.",
            "opportunity_type": "internship",
            "deadline": datetime.utcnow() + timedelta(days=20),
            "location": "Mumbai",
            "is_remote": False,
            "eligibility": ["3rd/4th year preferred", "Basic Swift knowledge"],
            "skills_required": ["Swift", "iOS Development", "UIKit", "Xcode"],
            "summary": "Develop real iOS apps. Portfolio building opportunity.",
            "apply_link": "https://example.com/apply/3",
            "source_url": "https://example.com/job/3",
            "source_platform": "hackerearth",
            "status": "active",
            "is_verified": True,
        },
    ]

    try:
        for opp_data in sample_opportunities:
            existing = (
                db.query(Opportunity)
                .filter(Opportunity.title == opp_data["title"])
                .first()
            )

            if not existing:
                opportunity = OpportunityService.create_opportunity(db, **opp_data)
                print(f"✓ Created: {opportunity.title}")
            else:
                print(f"✗ Already exists: {opp_data['title']}")

        print(f"\n✓ Database seeded successfully!")
        print(f"Total opportunities: {db.query(Opportunity).count()}")

    except Exception as e:
        print(f"✗ Error seeding database: {str(e)}")
        db.rollback()

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
