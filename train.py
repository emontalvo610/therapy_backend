from elasticsearch import Elasticsearch
import pandas as pd
from elasticsearch.helpers import bulk
import os
from dotenv import load_dotenv


load_dotenv()

es = Elasticsearch(
    cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
    basic_auth=(os.getenv("ELASTIC_USERNAME"), os.getenv("ELASTIC_PASSWORD"))
)

# Read CSV file
df = pd.read_csv('train.csv')

# Clean data: remove NaN values and convert them to None
df = df.where(pd.notnull(df), None)

# Prepare data for bulk indexing
def generate_actions():
    for index, row in df.iterrows():
        doc = {
            "_index": "train_data",
            "_source": {k: v for k, v in row.to_dict().items() if v is not None}  # Remove None values
        }
        yield doc

# Bulk upload to Elasticsearch with error handling
try:
    success, failed = bulk(es, generate_actions(), stats_only=True)
    print(f"Successfully indexed {success} documents")
    print(f"Failed to index {failed} documents")
except Exception as e:
    print(f"Error during bulk indexing: {str(e)}")

# Verify the index exists and count documents
try:
    count = es.count(index="train_data")
    print(f"Total documents in index: {count['count']}")
except Exception as e:
    print(f"Error checking index: {str(e)}")