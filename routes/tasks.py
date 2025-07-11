from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from bson import ObjectId
from pydantic import ValidationError

from models.task import Task, TaskCreate, TaskUpdate
from database.connection import tasks_collection, task_helper, get_next_task_id

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=List[Task])
async def get_tasks():
    """Buscar todas as tarefas ordenadas por prioridade"""
    tasks = []
    async for task in tasks_collection.find().sort("priority", 1):
        tasks.append(task_helper(task))
    return tasks

@router.post("/", response_model=Task)
async def create_task(task: TaskCreate):
    """Criar uma nova tarefa"""
    try:
        # Gerar task_id incremental se não fornecido
        if task.task_id is None:
            task.task_id = await get_next_task_id()
        
        task_dict = task.dict()
        task_dict["created_at"] = datetime.now()
        task_dict["updated_at"] = datetime.now()
        
        result = await tasks_collection.insert_one(task_dict)
        new_task = await tasks_collection.find_one({"_id": result.inserted_id})
        return task_helper(new_task)
        
    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Validation Error",
                "message": "Dados inválidos fornecidos",
                "details": e.errors()
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal Server Error",
                "message": "Erro interno do servidor ao criar a tarefa",
                "details": str(e)
            }
        )

@router.put("/{task_id}", response_model=Task)
async def update_task(task_id: str, task: TaskUpdate):
    """Atualizar uma tarefa existente (aceita ObjectId ou task_id)"""
    try:
        # Determinar se é ObjectId ou task_id incremental
        query = _build_query(task_id)
        
        # Verificar se a tarefa existe
        existing_task = await tasks_collection.find_one(query)
        if not existing_task:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "Not Found",
                    "message": "Tarefa não encontrada",
                    "field": "task_id",
                    "value": task_id
                }
            )
        
        # Atualizar campos modificados
        update_data = {k: v for k, v in task.dict().items() if v is not None}
        if update_data:
            update_data["updated_at"] = datetime.now()
            await tasks_collection.update_one(query, {"$set": update_data})
        
        updated_task = await tasks_collection.find_one(query)
        return task_helper(updated_task)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal Server Error",
                "message": "Erro interno do servidor ao atualizar a tarefa",
                "details": str(e)
            }
        )

@router.delete("/{task_id}")
async def delete_task(task_id: str):
    """Deletar uma tarefa (aceita ObjectId ou task_id)"""
    try:
        # Determinar se é ObjectId ou task_id incremental
        query = _build_query(task_id)
        
        # Verificar se a tarefa existe antes de deletar
        existing_task = await tasks_collection.find_one(query)
        if not existing_task:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "Not Found",
                    "message": "Tarefa não encontrada",
                    "field": "task_id",
                    "value": task_id
                }
            )
        
        await tasks_collection.delete_one(query)
        return {
            "message": "Tarefa deletada com sucesso",
            "deleted_task": {
                "id": str(existing_task["_id"]),
                "task_id": existing_task["task_id"],
                "title": existing_task["title"]
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal Server Error",
                "message": "Erro interno do servidor ao deletar a tarefa",
                "details": str(e)
            }
        )

def _build_query(task_id: str) -> dict:
    """Constrói a query para buscar uma tarefa por ID"""
    if task_id.isdigit():
        return {"task_id": int(task_id)}
    elif ObjectId.is_valid(task_id):
        return {"_id": ObjectId(task_id)}
    else:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Invalid ID",
                "message": "ID deve ser um ObjectId válido ou um task_id numérico",
                "field": "task_id",
                "value": task_id
            }
        )
