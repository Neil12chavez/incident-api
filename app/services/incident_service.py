from app.repository import incident_repository

def create_incident(db, data):
    return incident_repository.create(db, data)

def list_incidents(db):
    return incident_repository.get_all(db)

def get_incident(db, incident_id):
    return incident_repository.get_by_id(db, incident_id)