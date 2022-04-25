# Monitor Them
A Server Monitoring tool :
* Connecting to all the machines "to be monitored", which are specified in a json file monitors.json, through SSH.
* Get CPU & RAM info from these distant machines.
* Extract info from LOGs on the machines.
* Continuous delivery of the project in a Docker image.
This was a project developed in a ***DevOps*** context, which means all the following points were respected : 
* Writing tests and running them on each push.
* Continuous integration.
* Using a linter.
* Computing code covergae statistics.

## Installation
To run this project all you need is to pull & run our Docker image :

To run the docker image that contains our project, run the following commands :

```bash
docker login
```
The username is: group8tse

The password is: group8Interface

```bash
docker pull group8tse/project_image:latest
```
```bash
docker run -p 8050:8050 group8tse/project_image:latest
```

## Built With
* Python
* Docker
* Dart
