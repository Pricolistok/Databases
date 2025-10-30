FROM python:3.9-alpine

WORKDIR /app

RUN pip install psycopg2-binary

COPY data_changer.py .

CMD ["python", "data_changer.py"]