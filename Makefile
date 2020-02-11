


.PHONY: build
build:
	rm frontend/bundles/*
	yarn run build
	sudo docker-compose -f deployment/docker-compose.yml --build




# Start the web app as a docker compose service. 
.PHONY: docker-up 
docker-up:
ifeq ("","$(wildcard ./deployment/.docker.env)")
	echo "Copying file"
	cp .env.example ./deployment/.docker.env
endif
ifneq ("","$(wildcard ./frontend/bundles/*.js)")
	rm frontend/bundles/*
endif
	yarn run build
	sudo docker-compose -f deployment/docker-compose.yml up --build

# Start the docker development environment. If necessary, copy 
# .env.example to deployment/.production.env to get things started
# quickly.
.PHONY: docker-dev-up
docker-dev-up:
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
