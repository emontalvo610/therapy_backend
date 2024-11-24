from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv


load_dotenv()

es = Elasticsearch(
    cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
    basic_auth=(os.getenv("ELASTIC_USERNAME"), os.getenv("ELASTIC_PASSWORD"))
)

# 1. Get total count of documents
count = es.count(index="train_data")
print(f"Total documents: {count['count']}")

# 2. Get the first 10 documents
results = es.search(
    index="train_data",
    body={
        "query": {"match_all": {}},
        "size": 10
    }
)

# Print results in a readable format
for hit in results['hits']['hits']:
    print("\nDocument ID:", hit['_id'])
    print("Document content:", json.dumps(hit['_source'], indent=2))

# 3. Get index mapping
mapping = es.indices.get_mapping(index="train_data")
print("\nIndex mapping:", json.dumps(mapping, indent=2))

# 4. Get index settings
settings = es.indices.get_settings(index="train_data")
print("\nIndex settings:", json.dumps(settings, indent=2))