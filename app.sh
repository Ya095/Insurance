#!/bin/bash


sleep 10
alembic upgrade head
gunicorn insurance_app.main:main_app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000