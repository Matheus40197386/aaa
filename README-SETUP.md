# Portal Clientes - Setup

This repo contains:
- backend (FastAPI)
- frontend (React)
- sql/schema.sql

Backend env vars:
- DB_HOST
- DB_PORT
- DB_NAME
- DB_USER
- DB_PASS
- JWT_SECRET
- UPLOAD_DIR

Run local backend:
1) cd backend
2) python -m venv .venv
3) .venv\Scripts\activate
4) pip install -r requirements.txt
5) uvicorn app.main:app --reload

