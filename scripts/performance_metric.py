import pandas as pd
from sqlalchemy import create_engine
from sklearn.metrics import mean_squared_error, r2_score
import os
from dotenv import load_dotenv

def load_data_from_db(engine):
    query = "SELECT * FROM happiness_predictions"
    return pd.read_sql(query, engine)

def calculate_metrics(df):
    y_true = df['happiness_score']
    y_pred = df['predicted_happiness_score']
    
    mse = mean_squared_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    
    return mse, r2

if __name__ == "__main__":
    load_dotenv()
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')

    DATABASE_URI = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    engine = create_engine(DATABASE_URI)

    df = load_data_from_db(engine)
    print(f"Data loaded from database:\n{df.head()}")

    mse, r2 = calculate_metrics(df)
    
    print(f"Mean Squared Error: {mse}")
    print(f"R^2 Score: {r2}")
