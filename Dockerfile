FROM python:3.8.16-bullseye 

WORKDIR /app

COPY requirements.txt . 

RUN pip install -r requirements.txt 

COPY tools.py .
COPY main.py . 

ENTRYPOINT ["python", "-m", "main"]