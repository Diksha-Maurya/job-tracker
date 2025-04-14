from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.job import JobApplication

router = APIRouter()

@router.get("/jobs/stats/daily")
def daily_stats(db: Session = Depends(get_db)):
    results = (
        db.query(JobApplication.applied_on, func.count())
        .group_by(JobApplication.applied_on)
        .order_by(JobApplication.applied_on)
        .all()
    )
    return [{"date": r[0], "count": r[1]} for r in results]

@router.get("/jobs/stats/monthly")
def monthly_stats(db: Session = Depends(get_db)):
    results = (
        db.query(func.date_trunc("month", JobApplication.applied_on), func.count())
        .group_by(func.date_trunc("month", JobApplication.applied_on))
        .order_by(func.date_trunc("month", JobApplication.applied_on))
        .all()
    )
    return [{"month": r[0].strftime("%Y-%m"), "count": r[1]} for r in results]

@router.get("/jobs/stats/company")
def company_stats(db: Session = Depends(get_db)):
    results = (
        db.query(JobApplication.company_name, func.count())
        .group_by(JobApplication.company_name)
        .order_by(func.count().desc())
        .all()
    )
    return [{"company": r[0], "count": r[1]} for r in results]
