FROM python:3.12.8

RUN pip install pandas

WORKDIR /app
COPY pipeline.py pipeline.py

#Create an Entrypoint
ENTRYPOINT [ "python","pipeline.py" ]