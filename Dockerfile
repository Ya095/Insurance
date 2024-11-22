FROM python:3.11-slim-buster

WORKDIR /app_dir

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

#CMD gunicorn insurance_app.main:main_app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
RUN chmod a+x app.sh