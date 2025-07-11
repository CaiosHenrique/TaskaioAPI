# Taskaio API

Backend FastAPI para o aplicativo mobile Taskaio, desenvolvido em Python com integração ao MongoDB.

## 🚀 Funcionalidades

- ✅ **CRUD completo** de tasks com IDs incrementais
- ✅ **Flexibilidade** - Aceita ObjectId ou task_id numérico
- ✅ **Ordenação automática** por prioridade
- ✅ **Validações robustas** com Pydantic
- ✅ **Tratamento de erros** detalhado
- ✅ **Seed automático** de dados para desenvolvimento
- ✅ **CORS configurado** para apps mobile
- ✅ **Documentação automática** da API
- ✅ **Health check** integrado
- ✅ **Arquitetura modular** e escalável

## 📦 Instalação

### Instalação Local

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar variáveis de ambiente
cp .env.example .env

# 3. Executar a API
python main.py
```

### Instalação com Docker

```bash
# Usando NPM Script (Recomendado)
npm run docker

# Ou usando Docker Compose diretamente
docker-compose up -d
```

A API estará disponível em `http://localhost:8000`

## 🔧 Scripts NPM Disponíveis

```bash
# Executar com Docker (construir + executar + mostrar informações)
npm run docker

# Construir apenas as imagens
npm run docker:build

# Executar containers
npm run docker:up

# Parar containers
npm run docker:down

# Ver logs em tempo real
npm run docker:logs

# Reiniciar containers
npm run docker:restart

# Ver status dos containers
npm run docker:status

# Limpar tudo (containers, volumes, imagens)
npm run docker:clean

# Executar localmente (sem Docker)
npm run dev

# Testar se a API está rodando
npm run test

# Abrir documentação no navegador
npm run docs
```

## 🛠 Endpoints da API

### Rota Principal
- `GET /` - Mensagem de boas-vindas da API
- `GET /health` - Health check da aplicação e banco de dados

### Tasks
- `GET /tasks` - Lista todas as tasks ordenadas por prioridade
- `POST /tasks` - Cria uma nova task
- `PUT /tasks/{id}` - Atualiza uma task (aceita ObjectId ou task_id)
- `DELETE /tasks/{id}` - Deleta uma task (aceita ObjectId ou task_id)

### Exemplos de Uso

#### Criar uma nova task
```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Estudar FastAPI",
    "priority": 1,
    "done": false
  }'
```

#### Atualizar uma task (usando task_id)
```bash
curl -X PUT "http://localhost:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{
    "done": true
  }'
```

#### Deletar uma task (usando task_id)
```bash
curl -X DELETE "http://localhost:8000/tasks/1"
```

## 📚 Documentação

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🏗 Estrutura do Projeto

```
TaskaioAPI/
├── main.py                    # Aplicação FastAPI principal
├── requirements.txt          # Dependências do projeto
├── package.json             # Scripts NPM para automação
├── README.md                # Documentação do projeto
├── BACKEND_REQUIREMENTS.md  # Requisitos técnicos detalhados
├── .env.example             # Exemplo de variáveis de ambiente
├── Dockerfile               # Configuração do Docker
├── docker-compose.yml       # Orquestração dos serviços
├── scripts/
│   ├── start-docker.ps1     # Script PowerShell para Windows
│   └── start-docker.sh      # Script Bash para Unix/Linux/macOS
├── database/
│   ├── __init__.py
│   └── connection.py        # Conexão com MongoDB e helpers
├── models/
│   ├── __init__.py
│   └── task.py             # Modelos Pydantic para Tasks
└── routes/
    ├── __init__.py
    ├── main.py             # Rota principal e health check
    └── tasks.py            # Rotas das tasks (CRUD)
```

## ⚙️ Configuração

### Variáveis de Ambiente

- `MONGODB_URL`: URL de conexão com MongoDB (padrão: `mongodb://localhost:27017`)
- `HOST`: Host do servidor (padrão: `0.0.0.0`)
- `PORT`: Porta do servidor (padrão: `8000`)
- `ENV`: Ambiente de execução (`development` ou `production`)
- `DEBUG`: Ativa modo debug (`True` ou `False`)

### Modelo de Dados

```python
class Task:
    id: str              # MongoDB ObjectId
    task_id: int         # ID incremental único (1, 2, 3...)
    title: str           # Título da tarefa
    done: bool           # Status de conclusão
    priority: int        # Prioridade (1=alta, 2=média, 3=baixa)
    created_at: datetime # Data de criação
    updated_at: datetime # Data de atualização
```

## 🔍 Funcionalidades Técnicas

### IDs Incrementais
- Cada task recebe um `task_id` sequencial (1, 2, 3...)
- Facilita o uso no frontend React Native
- Mantém compatibilidade com ObjectId do MongoDB

### Validações
- Título não pode estar vazio
- Prioridade deve ser 1, 2 ou 3
- IDs são validados automaticamente

### Tratamento de Erros
- Respostas estruturadas com detalhes específicos
- Logs detalhados para debugging
- Códigos de status HTTP apropriados

### Performance
- Índices otimizados no MongoDB
- Ordenação automática por prioridade
- Queries eficientes

## 🧪 Testando a API

```bash
# Health check
curl http://localhost:8000/health

# Listar todas as tasks
curl http://localhost:8000/tasks

# Criar nova task
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title": "Nova Task", "priority": 1}'

# Atualizar task por task_id
curl -X PUT "http://localhost:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{"done": true}'

# Deletar task por task_id
curl -X DELETE "http://localhost:8000/tasks/1"
```

## 🤝 Compatibilidade

- ✅ **Frontend React Native** - IDs incrementais facilitam o uso
- ✅ **MongoDB** - Mantém compatibilidade com ObjectId
- ✅ **Docker** - Containerização completa
- ✅ **Desenvolvimento** - Seed automático de dados
- ✅ **Produção** - Configurações otimizadas

## 📈 Desenvolvimento

### Executando em Modo de Desenvolvimento

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd TaskaioAPI

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env

# Execute a API
python main.py
```

### Executando com Docker

```bash
# Método rápido com NPM
npm run docker

# Método manual
docker-compose up -d
```

A API estará disponível em `http://localhost:8000` e o MongoDB em `localhost:27017`.

---

**Taskaio API** - Desenvolvido com ❤️ usando FastAPI, MongoDB e Docker.

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
