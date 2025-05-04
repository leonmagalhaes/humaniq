FROM python:3.9-slim

WORKDIR /app

# Copiar arquivos de dependências
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY . .

# Variáveis de ambiente
ENV FLASK_APP=run.py
ENV FLASK_CONFIG=production
ENV PYTHONUNBUFFERED=1

# Expor a porta 5000
EXPOSE 5000

# Executar o script de seed para popular o banco de dados
RUN python seed.py

# Comando para iniciar a aplicação com gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
