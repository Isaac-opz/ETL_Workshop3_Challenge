from kafka import KafkaProducer
import pandas as pd
import json
import time

def produce_messages(producer, topic, df):
    for _, row in df.iterrows():
        message = row.to_json()
        producer.send(topic, value=message)
        time.sleep(0.1)

if __name__ == "__main__":
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    
    df = pd.read_csv('data/transformed_test_data.csv')
    
    produce_messages(producer, 'happiness_topic', df)

