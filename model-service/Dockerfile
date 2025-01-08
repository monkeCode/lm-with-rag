FROM python:3.12.8-alpine

ARG PORT=50001

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . . 

ENV grpc_port=$PORT

EXPOSE $PORT

ENTRYPOINT [ "python", "main.py" ]
