FROM python:3.10-slim-buster

WORKDIR "/home"

COPY . .

RUN pip install .

ENTRYPOINT ["python", "gps_tracker/main.py"]
