import asyncio
from database.connection import client, db

async def test_connection():
    """Testa a conexão com o MongoDB"""
    try:
        # Testar conexão
        await client.admin.command('ping')
        print("✅ Conexão com MongoDB bem-sucedida!")
        
        # Listar bancos de dados
        db_list = await client.list_database_names()
        print(f"📂 Bancos de dados disponíveis: {db_list}")
        
        # Testar coleção
        collections = await db.list_collection_names()
        print(f"📋 Coleções no banco 'taskaio': {collections}")
        
        # Contar documentos na coleção tasks
        from database.connection import tasks_collection
        count = await tasks_collection.count_documents({})
        print(f"📊 Total de tasks na coleção: {count}")
        
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        print(f"🔍 Tipo do erro: {type(e).__name__}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(test_connection())