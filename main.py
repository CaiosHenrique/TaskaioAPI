"""
Taskaio API - Backend FastAPI para gerenciamento de metas e tarefas.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging

from routes.main import router as main_router
from routes.tasks import router as tasks_router
from database.connection import seed_default_tasks

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicialização da aplicação FastAPI
app = FastAPI(
    title="Taskaio API", 
    version="1.0.0",
    description="API para gerenciamento de metas e tarefas do aplicativo Taskaio"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tratador de exceções de validação
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Trata erros de validação do Pydantic"""
    logger.error(f"Validation error: {exc}")
    
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"],
            "input": error.get("input")
        })
    
    return JSONResponse(
        status_code=400,
        content={
            "error": "Validation Error",
            "message": "Dados inválidos fornecidos na requisição",
            "details": errors
        }
    )

# Incluir rotas da aplicação
app.include_router(main_router)
app.include_router(tasks_router)

@app.on_event("startup")
async def startup_event():
    """Evento executado na inicialização da aplicação."""
    await seed_default_tasks()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
