from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Incident(Base):
    __tablename__ = "incidentes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)