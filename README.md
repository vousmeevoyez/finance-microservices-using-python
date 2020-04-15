# Lending Microservices

Lending Engine, Transaction Engine, BNI OPG gRPC, BNI RDL gRPC , BNI VA gRPC and Notification gRPC
all of this is connected together

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

## Tech Used
<b>Built with</b>
- [gRPC](http://flask.pocoo.org)
- [Flask](http://flask.pocoo.org)
- [RabbitMQ](http://flask.pocoo.org)
- [Celery](http://flask.pocoo.org)
- [Requests](http://flask.pocoo.org)
- [Docker](https://www.docker.com)
- [Postgresql](https://www.postgresql.org)

### Prerequisite

* Python 3 +
* PIP 
* Docker
* Docker Compose
* MongoDB + MongoDB with ReplicaSet

### Running Locally

A step by step series of examples that tell you how to get a development env running
```
clone this repository
```

Say what the step will be

* bni-opg-grpc
```
cd bni-opg-grpc
virtualenv venv
pip install -r requirements.txt
python manage.py or make start-local
```

* bni-rdl-grpc
```
cd bni-rdl-grpc
virtualenv venv
pip install -r requirements.txt
python manage.py or make start-local
```

* bni-va-grpc
```
cd bni-va-grpc
virtualenv venv
pip install -r requirements.txt
python manage.py or make start-local
```

* lending-engine
```
cd lending-engine
virtualenv venv
pip install -r requirements.txt
python manage.py init # this will load all required data
python manage.py run or make run
```

* notif-grpc
```
cd notif-grpc
virtualenv venv
pip install -r requirements.txt
python manage.py or make start-local
```

* transaction-engine
```
cd lending-engine
virtualenv venv
pip install -r requirements.txt
python manage.py init # this will load all required data
python manage.py run or make run
```

there's more information in each directory please checkout inside
