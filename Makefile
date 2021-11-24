SHELL = /bin/bash

start-mongo:
		docker-compose up --build --force-recreate --renew-anon-volumes -d

run-docker: start-mongo
		python gps_tracker/main.py

run-no-docker:
		python gps_tracker/main.py
