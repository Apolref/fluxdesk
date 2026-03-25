# 1. Pega uma versão oficial e leve do Python 3.13
FROM python:3.13-slim

# 2. Cria uma pasta chamada /app dentro do contêiner e entra nela
WORKDIR /app

# 3. Copia o arquivo de dependências para dentro da caixa
COPY requirements.txt .

# 4. Instala tudo o que o seu projeto precisa (FastAPI, SQLAlchemy, etc)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia todo o resto do seu código para dentro da pasta /app
COPY . .

# 6. Avisa que o contêiner vai usar a porta 8000
EXPOSE 8000

# 7. O comando final que o Docker vai rodar para ligar o servidor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]