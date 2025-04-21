# backend/app/routes/sync.py
from fastapi import APIRouter
from app.redis_client import r, test_redis
from app.gmail_client import get_recent_job_emails
from fastapi import HTTPException
import logging

router = APIRouter()


@router.get("/sync/test")
def sync_test():
    r.set("last_checked:test@gmail.com", "2025-04-21T10:00:00")
    return {"last_checked": r.get("last_checked:test@gmail.com")}


@router.get("/redis/test")
def test_redis_connection():
    value = test_redis()
    return {"status": value}


@router.post("/redis/set")
def set_custom_key(key: str, value: str):
    r.set(key, value)
    return {"message": f"Set {key} = {value}"}


@router.get("/redis/get")
def get_custom_key(key: str):
    value = r.get(key)
    return {"key": key, "value": value}


@router.get("/sync/emails")
def sync_emails():
    try:
        emails = get_recent_job_emails()
        return {"fetched_emails": emails}
    except Exception as e:
        logging.exception("Failed to fetch emails")
        raise HTTPException(status_code=500, detail="Failed to fetch emails")
