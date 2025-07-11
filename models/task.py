from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class Task(BaseModel):
    """
    Modelo completo de uma Task.
    
    Attributes:
        id: ID único da task (gerado automaticamente pelo MongoDB)
        task_id: ID incremental único para o frontend
        title: Título/descrição da task
        done: Status de conclusão da task (True/False)
        priority: Prioridade da task (1 = alta, 2 = média, 3 = baixa)
        created_at: Data/hora de criação
        updated_at: Data/hora da última atualização
    """
    id: Optional[str] = Field(None, alias="_id")
    task_id: int = Field(..., description="ID incremental único")
    title: str = Field(..., min_length=1, max_length=200, description="Título da tarefa")
    done: bool = Field(False, description="Status de conclusão da tarefa")
    priority: int = Field(..., ge=1, le=3, description="Prioridade: 1=alta, 2=média, 3=baixa")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class TaskCreate(BaseModel):
    """
    Modelo para criação de uma nova Task.
    
    Attributes:
        title: Título/descrição da task
        priority: Prioridade da task (1 = alta, 2 = média, 3 = baixa)
        done: Status inicial da task (opcional, padrão False)
        task_id: ID incremental (será gerado automaticamente se não fornecido)
    """
    title: str = Field(..., min_length=1, max_length=200, description="Título da tarefa")
    priority: int = Field(..., ge=1, le=3, description="Prioridade: 1=alta, 2=média, 3=baixa")
    done: bool = Field(False, description="Status inicial da tarefa")
    task_id: Optional[int] = Field(None, description="ID incremental único (gerado automaticamente)")

    @validator('title')
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError('O título não pode estar vazio')
        return v.strip()

    @validator('priority')
    def validate_priority(cls, v):
        if v not in [1, 2, 3]:
            raise ValueError('A prioridade deve ser 1 (alta), 2 (média) ou 3 (baixa)')
        return v

class TaskUpdate(BaseModel):
    """
    Modelo para atualização de uma Task existente.
    Todos os campos são opcionais.
    
    Attributes:
        title: Novo título/descrição da task
        done: Novo status de conclusão da task
        priority: Nova prioridade da task
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Novo título da tarefa")
    done: Optional[bool] = Field(None, description="Novo status de conclusão")
    priority: Optional[int] = Field(None, ge=1, le=3, description="Nova prioridade: 1=alta, 2=média, 3=baixa")

    @validator('title')
    def validate_title(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('O título não pode estar vazio')
        return v.strip() if v else v

    @validator('priority')
    def validate_priority(cls, v):
        if v is not None and v not in [1, 2, 3]:
            raise ValueError('A prioridade deve ser 1 (alta), 2 (média) ou 3 (baixa)')
        return v
