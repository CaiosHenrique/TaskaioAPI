# Dockerfile para Taskaio API
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependências
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Expõe a porta da aplicação
EXPOSE 8000

# Comando para executar a aplicação
CMD ["python", "main.py"]
