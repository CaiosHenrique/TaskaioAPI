import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

# Configuração da conexão com MongoDB
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGODB_URL)
db = client.taskaio
tasks_collection = db.tasks

async def get_next_task_id():
    """Gera o próximo task_id incremental"""
    result = await tasks_collection.find_one({}, sort=[("task_id", -1)])
    return result["task_id"] + 1 if result and "task_id" in result else 1

async def create_indexes():
    """Cria os índices necessários para melhor performance"""
    try:
        await tasks_collection.create_index("task_id", unique=True)
        await tasks_collection.create_index("priority")
        print("Índices criados com sucesso")
    except Exception as e:
        print(f"Erro ao criar índices: {e}")

async def seed_default_tasks():
    """Insere tasks padrão no banco de dados se não existirem tasks"""
    await create_indexes()
    
    if await tasks_collection.count_documents({}) == 0:
        default_tasks = [
            {
                "task_id": 1,
                "title": "Estudar React Native",
                "done": False,
                "priority": 1,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            },
            {
                "task_id": 2,
                "title": "Ler 10 páginas de um livro",
                "done": False,
                "priority": 2,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            },
            {
                "task_id": 3,
                "title": "Fazer exercício físico",
                "done": False,
                "priority": 3,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            },
            {
                "task_id": 4,
                "title": "Preparar jantar saudável",
                "done": False,
                "priority": 2,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
        ]
        await tasks_collection.insert_many(default_tasks)
        print("Tasks padrão inseridas no banco de dados")

def task_helper(task) -> dict:
    """Converte um documento do MongoDB para um dicionário Python"""
    return {
        "id": str(task["_id"]),
        "task_id": task["task_id"],
        "title": task["title"],
        "done": task["done"],
        "priority": task["priority"],
        "created_at": task["created_at"],
        "updated_at": task["updated_at"]
    }
