FROM python:3.11

WORKDIR /code
# Allows docker to cache installed dependencies between builds
# COPY requirements.dev.txt requirements.dev.txt
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

# Mounts the application code to the image
COPY ./app /code/app

# runs the production server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
