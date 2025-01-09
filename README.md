# IOT_Patient_Monitoring_Pipeline

This is a ....

## Environment structure
/
├── spark-streaming/streaming.py
├── alert.py
├── createKafkaTopic.py
├── docker-compose.yml
├── Dockerfile
├── gateway.py
├── iot_patient_data.csv
├── mongo.py
├── README.md
├── requirements.txt
├── sink_fire.json
└── sink_normal.json

## Dataset Description

The dataset contains IoT medical monitoring data with fields:

    Timestamp: Reading time
    PatientID (P1-P10): Unique patient identifier
    DeviceID (D1-D5): Monitoring device identifier
    Metric: Vital sign being measured (Temperature, HeartRate, OxygenLevel)
    Value: Numerical measurement
    Unit: Measurement unit (°C, bpm, %)


## Kafka Topics:

"emergency": Receives data when measurements exceed thresholds:

    Temperature > 39°C
    Heart Rate > 120 bpm
    Oxygen Level < 90%


"normal": Receives all other measurements within normal ranges


## Requirements

1- Python 3.11

2- Docker

3- Create a new environment using the following command:

```bash
$ python -m venv venv
```

3- Activate the environment:

```bash
$ .\venv\Scripts\activate
```

## Installation

### Install the required packages

```bash
$ pip install -r requirements.txt
```

## Create docker containers
```bash
$ docker-compose up -d --build
```

## Create kafka topics

```bash
$ python createKafkaTopic.py
```

## Run the kafka producer

```bash
$ python gateway.py
```

## Run the alert program notifying about an abnormal data

```bash
$ python alert.py
```

## Connect mongo to kafka

```bash
$ Invoke-RestMethod -Uri "http://localhost:8083/connectors" -Method POST -ContentType "application/json" -Body (Get-Content -Raw sink_emergency.json)
```

```bash
$ Invoke-RestMethod -Uri "http://localhost:8083/connectors" -Method POST -ContentType "application/json" -Body (Get-Content -Raw sink_normal.json)
```

## Show data stored in mongodb

```bash
$ python mongo.py
```

## Start the spark streaming processing script

```bash
$ docker exec -it Spark-submit /opt/bitnami/spark/bin/spark-submit --master spark://spark-master:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 /app/streaming.py
```