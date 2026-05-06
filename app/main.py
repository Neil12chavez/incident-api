from fastapi import FastAPI
from app.api.v1.routes import incident
from app.db.database import Base, engine
from app.api.v1.routes import health
from app.core.exceptions import global_exception_handler

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Incidente API")

app.include_router(incident.router)
app.include_router(health.router)
app.add_exception_handler(Exception, global_exception_handler)