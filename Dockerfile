FROM python:3.11-slim

RUN apt-get update

WORKDIR /usr/src/app

WORKDIR /code
COPY ./app/requirements.txt /code/requirements.txt
COPY ./app /code/app

ARG AZURE_DEVOPS_PAT
RUN sed -i -e "s/<PERSONAL_ACCESS_TOKEN>/$AZURE_DEVOPS_PAT/g" /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
