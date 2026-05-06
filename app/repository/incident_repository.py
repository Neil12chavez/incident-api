from sqlalchemy.orm import Session
from app.db import models

def create(db: Session, data):
    incident = models.Incident(**data.dict())
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident

def get_all(db: Session):
    return db.query(models.Incident).all()

def get_by_id(db: Session, incident_id: int):
    return db.query(models.Incident).filter(models.Incident.id == incident_id).first()