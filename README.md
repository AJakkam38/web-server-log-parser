# Web Server Logs Parser
* A simple Python3 application for Web Server log processing.
* In general, log entry looks like this 
```
81.174.152.222 - - [30/Jun/2020:23:38:03 +0000] "GET / HTTP/1.1" 200 6763 "-" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0"
```

### Prerequisites
* Python 3.8 or above
* Docker 19.03
* make Utility

### Usage
1. Clone this repo
```
git clone https://github.com/AJakkam38/web-server-log-parser.git
```
2. Change directory to `web-server-log-parser`
```
cd web-server-log-parser
```
3. Default docker python image is 3.8.6-slim-buster.
   You can change it by
```
make py_ver=DOCKER_PYTHON_IMAGE
```
4. Build docker image
```
make build
```
5. Run the docker image as container with python script arguments
```
make start LOGS_URL=pass_logsfile.txt_url START="30/Jun/2020:23:38:03\ +0000" END="30/Jun/2020:23:55:12\ +0000" ERRORCODE=404
```
6. You can stop and remove the container in the end
```
make stop
```
