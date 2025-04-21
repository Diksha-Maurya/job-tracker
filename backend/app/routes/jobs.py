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

@router.get("/jobs/daily-counts/")
def get_daily_application_counts(
    days: int = 30,
    db: Session = Depends(get_db)
):
    today = date.today()
    start_date = today - timedelta(days=days)

    results = (
        db.query(JobApplication.applied_on, func.count(JobApplication.id))
        .filter(JobApplication.applied_on >= start_date)
        .group_by(JobApplication.applied_on)
        .order_by(JobApplication.applied_on)
        .all()
    )

    return [{"date": day.strftime("%Y-%m-%d"), "count": count} for day, count in results]