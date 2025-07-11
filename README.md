# Taskaio API

Backend FastAPI para o aplicativo mobile Taskaio, desenvolvido em Python com integração ao MongoDB.

## Funcionalidades

- ✅ CRUD completo de tasks (Criar, Ler, Atualizar, Deletar)
- ✅ Conexão com MongoDB
- ✅ Seed automático de tasks padrão em desenvolvimento
- ✅ CORS configurado para apps mobile
- ✅ Documentação automática da API

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Configure a conexão com MongoDB:
   - Por padrão, a API conecta em `mongodb://localhost:27017`
   - Para usar uma URL diferente, defina a variável de ambiente `MONGODB_URL`

3. Execute a API:
```bash
python main.py
```

A API estará disponível em `http://localhost:8000`

## Endpoints

- `GET /tasks` - Lista todas as tasks
- `POST /tasks` - Cria uma nova task
- `PUT /tasks/{task_id}` - Atualiza uma task existente
- `DELETE /tasks/{task_id}` - Deleta uma task

## Documentação

Acesse `http://localhost:8000/docs` para ver a documentação interativa da API.

## Estrutura do Projeto

```
TaskaioAPI/
├── main.py           # Aplicação FastAPI principal
├── requirements.txt  # Dependências do projeto
└── README.md        # Este arquivo
```

## Modelo de Dados

```json
{
  "id": "string",
  "title": "string",
  "done": "boolean",
  "priority": "integer",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```
