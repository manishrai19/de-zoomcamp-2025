FROM python:3.12.8

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2 pyarrow

WORKDIR /app
COPY ingest_data.py ingest_data.py

#Create an Entrypoint
ENTRYPOINT [ "python","ingest_data.py" ]