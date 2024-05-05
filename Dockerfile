FROM python:3.10.12

WORKDIR /app
COPY . .
RUN pip install -r ./requirements/dev.txt --no-cache-dir

CMD gunicorn src.main:app   \ 
    --workers 1 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind=0.0.0.0:8000 \
    -c ./src/log_conf.py \
    --log-level debug
