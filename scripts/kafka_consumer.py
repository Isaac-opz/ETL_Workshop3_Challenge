import json
import pandas as pd
import pickle
from kafka import KafkaConsumer
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import os
from dotenv import load_dotenv
import logging

def consume_messages(consumer, model, engine):
    for message in consumer:
        record = json.loads(message.value)
        logging.info(f"Received record: {record}")
        features = pd.DataFrame([{
            'log_gdp_per_capita': record['log_gdp_per_capita'],
            'log_social_support': record['log_social_support'],
            'freedom_to_make_life_choices': record['freedom_to_make_life_choices'],
            'generosity': record['generosity'],
            'perceptions_of_corruption': record['perceptions_of_corruption'],
            'gdp_health_interaction': record['gdp_health_interaction']
        }])
        logging.info(f"Features for prediction: {features}")
        prediction = model.predict(features)[0]
        record['predicted_happiness_score'] = prediction
        save_to_db(record, engine)

def save_to_db(record, engine):
    df = pd.DataFrame([record])
    try:
        df.to_sql('happiness_predictions', engine, if_exists='append', index=False)
        logging.info(f"Inserted record into database: {record}")
    except SQLAlchemyError as e:
        logging.error(f"Error saving to database: {e}")

if __name__ == "__main__":
    load_dotenv()
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')

    DATABASE_URI = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    consumer = KafkaConsumer(
        'happiness_topic',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='happiness_group',
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    
    with open('models/best_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    engine = create_engine(DATABASE_URI)
    
    consume_messages(consumer, model, engine)


