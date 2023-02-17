FROM python:3.11

WORKDIR /app

COPY requirements.txt . 

RUN pip install -r requirements.txt 

COPY tools.py .
COPY main.py . 

ENTRYPOINT ["python", "-m", "main"]