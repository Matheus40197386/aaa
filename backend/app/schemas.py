from pydantic import BaseModel
from typing import List, Optional

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    cnpj: str
    password: str

class UserCreate(BaseModel):
    cnpj: str
    name: str
    email: Optional[str] = None
    password: str
    access_level_ids: List[int]
    is_admin: bool = False

class SpreadsheetCreate(BaseModel):
    title: str
    access_level_ids: List[int]

class SpreadsheetItem(BaseModel):
    id: int
    title: str

class SpreadsheetData(BaseModel):
    columns: List[str]
    rows: List[dict]
