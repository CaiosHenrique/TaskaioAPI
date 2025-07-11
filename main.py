from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from typing import List, Optional
import os
from datetime import datetime
from bson import ObjectId

app = FastAPI(title="Taskaio API", version="1.0.0")

# Configuração CORS para permitir requisições do app mobile
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexão com MongoDB
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGODB_URL)
db = client.taskaio
tasks_collection = db.tasks

# Modelos Pydantic
class Task(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    title: str
    done: bool = False
    priority: int
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class TaskCreate(BaseModel):
    title: str
    priority: int
    done: bool = False

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None
    priority: Optional[int] = None

# Função para converter ObjectId para string
def task_helper(task) -> dict:
    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "done": task["done"],
        "priority": task["priority"],
        "created_at": task["created_at"],
        "updated_at": task["updated_at"]
    }

# Seed de dados padrão para desenvolvimento
async def seed_default_tasks():
    count = await tasks_collection.count_documents({})
    if count == 0:
        default_tasks = [
            {
                "title": "Estudar React Native",
                "done": False,
                "priority": 1,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            },
            {
                "title": "Ler 10 páginas de um livro",
                "done": False,
                "priority": 2,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            },
            {
                "title": "Fazer exercício físico",
                "done": False,
                "priority": 3,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
        ]
        await tasks_collection.insert_many(default_tasks)
        print("Tasks padrão inseridas no banco de dados")

@app.on_event("startup")
async def startup_event():
    await seed_default_tasks()

# Rotas da API
@app.get("/")
async def root():
    return {"message": "Taskaio API - Gerencie suas metas e tarefas"}

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    tasks = []
    async for task in tasks_collection.find():
        tasks.append(task_helper(task))
    return tasks

@app.post("/tasks", response_model=Task)
async def create_task(task: TaskCreate):
    task_dict = task.dict()
    task_dict["created_at"] = datetime.now()
    task_dict["updated_at"] = datetime.now()
    
    result = await tasks_collection.insert_one(task_dict)
    new_task = await tasks_collection.find_one({"_id": result.inserted_id})
    return task_helper(new_task)

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, task: TaskUpdate):
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    update_data = {k: v for k, v in task.dict().items() if v is not None}
    if update_data:
        update_data["updated_at"] = datetime.now()
        await tasks_collection.update_one(
            {"_id": ObjectId(task_id)}, 
            {"$set": update_data}
        )
    
    updated_task = await tasks_collection.find_one({"_id": ObjectId(task_id)})
    if updated_task:
        return task_helper(updated_task)
    raise HTTPException(status_code=404, detail="Task não encontrada")

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    result = await tasks_collection.delete_one({"_id": ObjectId(task_id)})
    if result.deleted_count == 1:
        return {"message": "Task deletada com sucesso"}
    raise HTTPException(status_code=404, detail="Task não encontrada")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
