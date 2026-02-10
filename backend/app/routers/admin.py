from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.dependencies import get_db, get_current_admin
from app.auth import hash_password
from app.core.config import settings
import os
import uuid

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/users")
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    if db.query(models.User).filter(models.User.cnpj == payload.cnpj).first():
        raise HTTPException(status_code=400, detail="CNPJ already exists")

    user = models.User(
        cnpj=payload.cnpj,
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        is_admin=payload.is_admin,
    )
    access_levels = db.query(models.AccessLevel).filter(models.AccessLevel.id.in_(payload.access_level_ids)).all()
    user.access_levels = access_levels
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id}

@router.post("/spreadsheets")
def upload_spreadsheet(
    title: str = Form(...),
    access_level_ids: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    os.makedirs(settings.upload_dir, exist_ok=True)
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".xlsx", ".xls", ".csv"]:
        raise HTTPException(status_code=400, detail="Unsupported file")

    filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(settings.upload_dir, filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    spreadsheet = models.Spreadsheet(title=title, file_path=file_path, uploaded_by=admin.id)
    access_ids = [int(x) for x in access_level_ids.split(",") if x.strip()]
    access_levels = db.query(models.AccessLevel).filter(models.AccessLevel.id.in_(access_ids)).all()
    spreadsheet.access_levels = access_levels
    db.add(spreadsheet)
    db.commit()
    db.refresh(spreadsheet)
    return {"id": spreadsheet.id}
