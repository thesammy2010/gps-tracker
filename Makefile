SHELL = /bin/bash

install:  ## setup for local development
		./scripts/install.sh


start-mongo:  ## start up the Mongo docker container
		docker-compose up --build --force-recreate --renew-anon-volumes -d mongo

run: start-mongo  ## run api
		./scripts/run.sh

stop-docker: ## tear down mongo
		docker compose down
