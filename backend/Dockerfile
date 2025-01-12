FROM python:3.12.8-alpine

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT [ "uvicorn", "app:app","--host", "0.0.0.0", "--reload" ]