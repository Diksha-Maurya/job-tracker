from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from uuid import UUID

class JobCreate(BaseModel):
    company_name: str
    application_id: Optional[str] = None
    position_title: str
    status: Optional[str] = "applied"
    applied_on: Optional[date]
    source: Optional[str]
    notes: Optional[str]

class Job(JobCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
