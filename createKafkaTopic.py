from kafka.admin import KafkaAdminClient, NewTopic

BROKER = "localhost:9092"

TOPICS = [
    {"name": "emergency", "partitions": 1, "replication_factor": 1},
    {"name": "normal", "partitions": 1, "replication_factor": 1},
    {"name": "logs", "partitions": 1, "replication_factor": 1},
]


def create_topics():
    try:
        # Create an admin client
        admin_client = KafkaAdminClient(
            bootstrap_servers=BROKER, client_id="health-monitoring-admin"
        )

        topic_list = [
            NewTopic(
                name=topic["name"],
                num_partitions=topic["partitions"],
                replication_factor=topic["replication_factor"],
            )
            for topic in TOPICS
        ]
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
        print("Kafka topics created successfully!")

    except Exception as e:
        print(f"Error creating topics: {e}")


if __name__ == "__main__":
    create_topics()
