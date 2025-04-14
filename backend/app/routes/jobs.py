from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.job import JobApplication
from app.schemas.jobs import JobCreate, Job
from datetime import datetime
from fastapi import HTTPException
from typing import List

router = APIRouter()

@router.post("/jobs/", response_model=Job)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    if job.application_id:
        existing = db.query(JobApplication).filter_by(
            company_name=job.company_name,
            application_id=job.application_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail="An application with this ID already exists for the selected company."
            )

    db_job = JobApplication(
        **job.dict(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.get("/jobs/", response_model=List[Job])
def read_jobs(db: Session = Depends(get_db)):
    return db.query(JobApplication).all()