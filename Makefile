SHELL = /bin/bash

install:  ## setup for local development
		./scripts/install.sh

lint:  ## used to lint files
		black .
		isort .

test-integration: start-mongo  ## run integration tests
		pytest -m integration

test: ## run all python tests
		coverage run -m pytest
		coverage report

start-mongo:  ## start up the Mongo docker container
		docker-compose up --build --force-recreate --renew-anon-volumes -d mongo

run: start-mongo  ## run api
		./scripts/run.sh

stop-docker: ## tear down mongo
		docker compose down
