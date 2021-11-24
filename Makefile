SHELL = /bin/bash

start-mongo:
		docker-compose up --build --force-recreate --renew-anon-volumes -d mongo

run-docker:
		docker-compose up -d

run-no-docker: start-mongo
		python gps_tracker/main.py

stop-docker:
		docker compose down
