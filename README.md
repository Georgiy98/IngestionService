# Investigation Service

It's a service that allows you to connect to PostgreSQL database and load entire table as one json-file

## Installation

If you are going to use it for development, pull project from git

```commandline
git clone https://github.com/Georgiy98/IngestionService
```

Be sure, you have docker/docker-compose on your computer Then, if you would like to run it from docker, execute next
commands:

```commandline
docker build --tag ingestion_service .
```

## Usage

To gather data run:
```commandline
docker run ingestion_service host port db_name username password table_name column_name minimum_value
```
For help run:
```commandline
docker run ingestion_service --help 
```
To be continued..
