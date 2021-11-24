FROM python:3.10-slim-buster

RUN pip install .

ENTRYPOINT ["python", "gps_tracker/main.py"]
