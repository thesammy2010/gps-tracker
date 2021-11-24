SHELL = /bin/bash

run-mongo:
		docker-compose up --build --force-recreate --renew-anon-volumes -d

run-local: run-mongo
		python gps_tracker/main.py

run-no-docker:
		python gps_tracker/main.py
