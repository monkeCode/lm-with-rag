FROM python

WORKDIR /project

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 50001

ENTRYPOINT [ "python", "main.py" ]