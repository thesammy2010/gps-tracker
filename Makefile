SHELL = /bin/bash

start-mongo:  ## start up the Mongo docker container
		docker-compose up --build --force-recreate --renew-anon-volumes -d mongo

run: start-mongo  ## run api
		./scripts/run.sh

stop-docker: ## tear down mongo
		docker compose down
