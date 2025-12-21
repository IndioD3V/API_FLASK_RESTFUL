FROM python:3.13.11

WORKDIR /app
COPY . /app

# Copiar o arquivo .env para o contêiner
COPY .env .env

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
