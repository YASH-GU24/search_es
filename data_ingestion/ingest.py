import json
import os

import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch import exceptions as es_exceptions

# Connect to Elasticsearch
ES_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
try:
    es = Elasticsearch(ES_URL)
    if not es.ping():
        raise ConnectionError("Elasticsearch server is not reachable")
except es_exceptions.ConnectionError:
    raise SystemExit("Failed to connect to Elasticsearch. Exiting...")
except Exception as e:
    raise SystemExit(f"Unexpected error: {str(e)}")

INDEX_NAME = "movies"
DATASET_PATH = "/dataset/final_data.csv"


def get_mapping():
    try:
        with open("mapping/mapping.json", "r") as f:
            mapping = json.load(f)
        return mapping
    except FileNotFoundError:
        raise SystemExit("Mapping file not found. Exiting...")
    except json.JSONDecodeError:
        raise SystemExit("Error parsing mapping file. Exiting...")


def preprocess_data(df):
    try:
        df = df[
            ["Name", "Genres", "Actors", "Director", "Description"]
        ]  # Taking just 5 columns
        df = df.where(pd.notna(df), None)
        df["Genres"] = df["Genres"].apply(
            lambda x: x.split(",") if isinstance(x, str) else []
        )
        df["Actors"] = df["Actors"].apply(
            lambda x: x.split(",") if isinstance(x, str) else []
        )
        df["Name"] = df["Name"].astype(str)
        df["Description"] = df["Description"].astype(str)
        df["Director"] = df["Director"].astype(str)
        return df
    except KeyError as e:
        raise SystemExit(f"Missing expected column in dataset: {str(e)}")
    except Exception as e:
        raise SystemExit(f"Unexpected error during preprocessing: {str(e)}")


# Loading mapping
mapping = get_mapping()

# Load dataset
try:
    df = pd.read_csv(DATASET_PATH)
    df = preprocess_data(df)
except FileNotFoundError:
    raise SystemExit("Dataset file not found. Exiting...")
except pd.errors.ParserError:
    raise SystemExit("Error parsing dataset file. Exiting...")
except Exception as e:
    raise SystemExit(f"Unexpected error loading dataset: {str(e)}")

# Create index if not exists
try:
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME, body=mapping)
        print(f"Index '{INDEX_NAME}' created successfully!")
except es_exceptions.RequestError as e:
    raise SystemExit(f"Error creating index: {str(e)}")
except es_exceptions.ElasticsearchException as e:
    raise SystemExit(f"Elasticsearch error: {str(e)}")
except Exception as e:
    raise SystemExit(f"Unexpected error during index creation: {str(e)}")

# Index data
for _, row in df.iterrows():
    doc = {
        "Name": row["Name"],
        "Genres": row["Genres"] if row["Genres"] else [],
        "Actors": row["Actors"] if row["Actors"] else [],
        "Director": row["Director"],
        "Description": row["Description"],
    }
    try:
        es.index(index=INDEX_NAME, document=doc)
    except es_exceptions.RequestError as e:
        print(f"Error indexing document: {str(e)}")
    except es_exceptions.ElasticsearchException as e:
        print(f"Elasticsearch error while indexing: {str(e)}")
    except Exception as e:
        print(f"Unexpected error while indexing document: {str(e)}")

print("Data indexed successfully!")
