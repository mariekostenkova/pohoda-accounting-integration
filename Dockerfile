FROM python:3.11-slim

RUN apt-get update

WORKDIR /code

COPY ./app/requirements.txt /code/requirements.txt

COPY ./app /code/app

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]