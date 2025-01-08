FROM cnstark/pytorch:2.3.1-py3.10.15-cuda12.1.0-ubuntu22.04

WORKDIR /app


COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 50001

ENTRYPOINT [ "python", "main.py" ]