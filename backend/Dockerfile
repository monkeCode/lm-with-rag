FROM python:3.12.8-alpine

ARG rag_addr="localhost"
ARG rag_port="50001"
ARG model_addr="localhost"
ARG model_port="50001"

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENV rag_addr=$rag_addr
ENV rag_port=$rag_port
ENV model_addr=$model_addr
ENV model_port=$model_port

EXPOSE 8000

ENTRYPOINT [ "uvicorn", "app:app","--host", "0.0.0.0", "--reload" ]