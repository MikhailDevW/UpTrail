FROM python:3.10

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

# Скопировать всё необходимое содержимое 
# той директории локального компьютера, где сохранён Dockerfile,
# в текущую рабочую директорию образа — /app.
COPY . .

RUN chmod a+x docker.sh
CMD gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0:8888
