from kafka import KafkaProducer
import json
import datetime
import pandas as pd
from time import sleep


# nb: The number of records to send from the dataset
# n: The time interval (in seconds) between sending each record to Kafka
def data_to_kafka(nb=10, n=1):
    # Create Kafka producer
    producer = KafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    # Read the data
    data = pd.read_csv("./iot_patient_data.csv", sep=",").iloc[:nb, :]

    for i in data.index:
        X = data.iloc[[i], :]
        if "Metric" in X.columns:
            # Get the metric and its value
            metric_value = X.loc[i, "Value"]
            metric_name = X.loc[i, "Metric"]

            # Define topics based on conditions
            if (
                metric_name == "Temperature" and metric_value > 39
            ):  # Threshold for emergency temperature
                topic_name = "emergency"
            elif (
                metric_name == "HeartRate" and metric_value > 120
            ):  # Threshold for emergency heart rate
                topic_name = "emergency"
            elif (
                metric_name == "OxygenLevel" and metric_value < 90
            ):  # Threshold for emergency oxygen level
                topic_name = "emergency"
            else:
                topic_name = "normal"

            # Add timestamp, date, and sensor ID
            doc = X.to_dict("records")[0]
            doc["date"] = str(datetime.datetime.now().date())
            doc["time"] = str(datetime.datetime.now().time())[:5]
            doc["Sensor_ID"] = i + 1  # Unique ID based on row index

            # Send the data to Kafka
            producer.send(topic_name, doc)
            print(f"Data sent to {topic_name}: {doc}")

            # Sleep between messages to simulate real-time data flow
            sleep(n)
            producer.flush()


# Example: Sending the first 10 records
data_to_kafka(nb=1000)
