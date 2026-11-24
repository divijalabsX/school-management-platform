from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.connection import get_db


router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "School Management Platform"
    }


@router.get("/db-health")
def database_health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))

        return {
            "database": "connected",
            "status": "healthy"
        }

    except Exception:
        return {
            "database": "disconnected",
            "status": "unhealthy"
        }