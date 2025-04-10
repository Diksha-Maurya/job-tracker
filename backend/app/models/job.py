import uuid
from sqlalchemy import Column, String, Date, Text, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.database import Base
import enum

# Define status choices as Enum
class StatusEnum(str, enum.Enum):
    applied = "applied"
    interview = "interview"
    rejected = "rejected"
    offer = "offer"
    accepted = "accepted"

# Define the JobApplication table
class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name = Column(String, nullable=False)
    position_title = Column(String, nullable=False)
    status = Column(Enum(StatusEnum), nullable=False)
    applied_on = Column(Date, nullable=False)
    source = Column(String)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
