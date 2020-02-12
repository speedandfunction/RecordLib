include .env

.PHONY: build-frontend
build-frontend:
	sudo docker build -f deployment/FrontendDockerfile -t "${CONTAINER_REGISTRY}/recordlibfrontend:${CONTAINER_TAG}" ./deployment

.PHONY: build-webapp
build-webapp:
	rm frontend/bundles/*
	yarn run build
	sudo docker build -f deployment/DjangoDockerfile -t "${CONTAINER_REGISTRY}/recordlibdjango:${CONTAINER_TAG}" .


.PHONY: build-db
build-db:
	sudo docker build -f deployment/PG_Dockerfile -t "${CONTAINER_REGISTRY}/recordlibdb:${CONTAINER_TAG}" ./deployment

build: build-frontend build-webapp build-db


.PHONY: docker-pull-up
docker-pull-up:
ifeq ("","$(wildcard ./deployment/.docker.env)")
	echo "Copying file"
	cp .env.example ./deployment/.docker.env
endif
	sudo docker-compose -f deployment/docker-compose-pull.yml up --build

# Start the web app as a docker compose service,
# building the images. 
.PHONY: docker-build-up
docker-build-up:
ifeq ("","$(wildcard ./deployment/.docker.env)")
	echo "Copying file"
	cp .env.example ./deployment/.docker.env
endif
ifneq ("","$(wildcard ./frontend/bundles/*.js)")
	rm frontend/bundles/*
endif
	yarn run build
	sudo docker-compose -f deployment/docker-compose-build.yml up --build

# Start the docker development environment. If necessary, copy 
# .env.example to deployment/.production.env to get things started
# quickly.
.PHONY: docker-dev-up
docker-dev-up:
ifeq ("","$(wildcard .env)")
	# local environment needs CONTAINER_REGISTRY and CONTAINER_TAG vars.
	cp .env.example .env
endif
ifeq ("","$(wildcard ./deployment/.docker.env)")
	cp .env.example ./deployment/.docker.env
endif
ifneq ("","$(wildcard ./frontend/bundles/*.js)")
	rm frontend/bundles/*
endif
	yarn run build
	sudo docker-compose -f deployment/docker-compose-dev.yml up --build

# Push to a registry
.PHONY: push
push:
	sudo docker push ${CONTAINER_REGISTRY}/recordlibfrontend:${CONTAINER_TAG}
	sudo docker push ${CONTAINER_REGISTRY}/recordlibdjango:${CONTAINER_TAG}
	sudo docker push ${CONTAINER_REGISTRY}/recordlibdb:${CONTAINER_TAG}

# deploy is used to get the newest images running on a remote host.
# Assumes that the host is set up to receive this command. 
.PHONY: deploy
deploy:
	ssh ${HOST}; cd recordlib; ./update.sh 

build-push-deploy: build push deploy
