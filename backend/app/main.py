from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app import models
from app.constants import UF_CODES
from app.db import SessionLocal
from app.routers import auth, admin, spreadsheets

app = FastAPI(title="Portal Clientes")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://chatbot-frontend.mmidem.easypanel.host",
        "https://chatbot-aaa.mmidem.easypanel.host",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(spreadsheets.router)


@app.on_event("startup")
def ensure_state_access_levels():
    db: Session = SessionLocal()
    try:
        existing_names = {name for (name,) in db.query(models.AccessLevel.name).all()}
        missing = [uf for uf in UF_CODES if uf not in existing_names]
        if missing:
            db.add_all([models.AccessLevel(name=uf) for uf in missing])
            db.commit()
    finally:
        db.close()
