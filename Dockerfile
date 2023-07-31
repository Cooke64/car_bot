FROM python:3.10-slim
LABEL maintainer="Cooke09"

RUN mkdir /app

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY /src .

CMD ["python", "main.py"]