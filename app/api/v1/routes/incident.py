from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.incident import IncidentCreate, IncidentResponse
from app.services import incident_service
from app.db.database import SessionLocal

router = APIRouter(prefix="/api/v1/incidents", tags=["Incidents"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=IncidentResponse)
def create(data: IncidentCreate, db: Session = Depends(get_db)):
    return incident_service.create_incident(db, data)

@router.get("/")
def list_all(db: Session = Depends(get_db)):
    return incident_service.list_incidents(db)

@router.get("/{id}")
def get_by_id(id: int, db: Session = Depends(get_db)):
    incident = incident_service.get_incident(db, id)
    if not incident:
        raise HTTPException(status_code=404, detail="Not found")
    return incident