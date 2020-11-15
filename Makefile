#Dockerfile vars
py_ver=3.8-slim-buster

#vars
IMAGENAME=nginx_log_parser
CONTAINERNAME=nginx_log_parser_app
TAG=akhila_jakkam

#Help
.PHONY: help

help:
	@echo "make py_ver=3.8.6-slim-buster"
	@echo "				py_ver - Docker official python imagename. Default = 3.8-slim-buster"
	@echo "make build"
	@echo "				Builds docker image"
	@echo " "
	@echo "make start LOGS_URL=url_for_logs.txt START=start_time END=end_time ERRORCODE=error_code"
	@echo " "
	@echo "				Runs the docker image as container and runs the python script"
	@echo "make stop"
	@echo "				Stops and removes the docker container"

build: Dockerfile
	@echo "Building Docker Image..."
	docker build -t $(IMAGENAME):$(TAG) .

start:
	@echo "Starting Docker Container..."
	docker run -it --name $(CONTAINERNAME) $(IMAGENAME):$(TAG) --log_file_url $(LOGS_URL) --start_time $(START) --end_time $(END) --error_code $(ERRORCODE)

stop:
	@echo "Stopping the Container..."
	docker stop $(CONTAINERNAME)
	@echo "Removing the Container..."
	docker rm $(CONTAINERNAME)