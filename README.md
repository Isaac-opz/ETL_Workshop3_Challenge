# Machine Learning and Data Streaming Workshop

## Introduction
Welcome. This project is focused on predicting happiness scores across different countries using historical CSV data files. The entire workflow from data ingestion, processing, training a regression model, and predicting results, to storing outputs in a database is automated using Python and Kafka.

## Project Structure

- **data/**: Contains CSV files with the happiness scores.
- **data-README.md/**: Files used in the README.
- **doc/**: Document files.
- **models/**: Trained model(s) stored in PKL format.
- **notebooks/**: Jupyter notebook for EDA, feature selection, and model evaluation.
- **scripts/**: Scripts for data preprocessing, model training, and streaming with Kafka.
- **.env-template**: Template for environment variables.
- **.gitignore**: Files and directories to be ignored by Git.
- **docker-compose.yml**: Docker Compose file for setting up Kafka.
- **requirements.txt**: List of Python dependencies.

## Technologies Used

- **Python**: Primary programming language.
- **Jupyter Notebook**: For running interactive coding sessions.
- **Kafka**: For data streaming.
- **Scikit-Learn**: For implementing machine learning models.
- **PSQL Database**: For storing data.
- **Docker**: For containerization of Kafka.

## Setup and Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Isaac-opz/ETL_Workshop3_Challenge.git
   cd ETL_Workshop3_Challenge
   ```

2. **Create a `.env` File**
   make a copy of the `.env-template` file and rename it to `.env`. Fill in the required environment variables.

   ```bash
   cp .env-template .env
   ```

3. **Install Dependencies**
   Ensure Python is installed and then run:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

- **Running the Notebooks**: 
  Navigate to the `/notebooks` directory and launch Jupyter Notebook to open and run the provided notebooks.
  ```bash
  jupyter notebook
  ```

- **Executing Scripts**:
  Run the Python scripts located in the `/scripts` directory for streaming and prediction operations.
  ```bash
  python3 scripts/data_transformer.py
  ```
  now run the kafka container using the following command
   ```bash
   docker-compose up -d
   ```
   then run the following commands in two different terminals to start the producer and consumer
  ```bash
  python3 scripts/kafka_consumer.py
  python3 scripts/kafka_producer.py
  ```
  You can run the following command to check the performance of the model
  ```bash
   python3 scripts/performance_metrics.py
   ```

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgements

- [Kafka](https://kafka.apache.org/)
- [Scikit-Learn](https://scikit-learn.org/)
- [NeonDB](https://neon.tech/)
- [Docker](https://www.docker.com/)

