FROM python:3.10-slim

RUN apt-get update && apt-get install -y postgresql-client

COPY ./etl/etl_script.py .

CMD ["python", "etl_script.py"]