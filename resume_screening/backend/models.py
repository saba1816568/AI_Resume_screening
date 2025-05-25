# Database models
from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, unique=True, nullable=False)
    file_path = Column(String, nullable=False)

class RankingResult(Base):
    __tablename__ = "ranking_results"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer)
    job_description = Column(String, nullable=False)
    score = Column(Float, nullable=False)
