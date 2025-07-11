from fastapi import APIRouter
from datetime import datetime
from database.connection import client, db

router = APIRouter()

@router.get("/")
async def root():
    """Rota principal da API"""
    return {"message": "Taskaio API - Gerencie suas metas e tarefas"}

@router.get("/health")
async def health_check():
    """Endpoint de saúde da aplicação"""
    try:
        # Testar conexão com o banco
        await client.admin.command('ping')
        db_status = "connected"
        db_error = None
    except Exception as e:
        db_status = "disconnected"
        db_error = str(e)
    
    return {
        "status": "ok" if db_status == "connected" else "error",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "database": {
            "status": db_status,
            "error": db_error
        },
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "tasks": "/tasks"
        }
    }
