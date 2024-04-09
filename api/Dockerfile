# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12
WORKDIR /code

EXPOSE 5050

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY ./requirements.txt /code/requirements.txt

RUN apt-get update \
    && apt-get install -y unixodbc \
    && apt-get install -y odbc-postgresql \
    && apt-get install -y odbc-mariadb

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
#CMD ["gunicorn", "--bind", "0.0.0.0:5050", "-k", "uvicorn.workers.UvicornWorker", "app.app:app"]
# CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "5050", "--reload"]