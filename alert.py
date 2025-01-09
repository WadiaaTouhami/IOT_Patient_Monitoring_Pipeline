from kafka import KafkaConsumer
import json

# Topics to consume data from
topics = ['normal', 'emergency']

# Initialize Kafka consumer for the specified topics
consumer = KafkaConsumer(
    *topics,  # subscribe to both normal and emergency topics
    group_id='patient-monitoring-group',
    auto_offset_reset="earliest",
    bootstrap_servers='localhost:9092'
)

# Start consuming messages
for msg in consumer:
    # Deserialize the message
    message = json.loads(msg.value.decode('utf-8'))
    
    # Print the message to simulate processing it
    print(f"Message received from {msg.topic}:")
    print(message)
    
    # Check if the message is from the emergency topic
    if msg.topic == 'emergency':
        print("ALERT: Emergency condition detected!")
        # You could add further action here like sending a notification or triggering an alarm
