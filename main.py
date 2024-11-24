from fastapi import FastAPI, Query, HTTPException
from elasticsearch import Elasticsearch
from typing import Optional
from math import ceil
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

load_dotenv()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

es = Elasticsearch(
    cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
    basic_auth=(os.getenv("ELASTIC_USERNAME"), os.getenv("ELASTIC_PASSWORD"))
)

@app.get("/")
def health_check():
    return "App is running!"

@app.get("/search")
async def search_data(
    query: str = Query(..., description="Search query"),
    page: Optional[int] = Query(1, description="Page number", ge=1),
    size: Optional[int] = Query(10, description="Results per page", ge=1, le=100),
):
    try:
        # Calculate skip/from value
        skip = (page - 1) * size

        body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["*"]
                }
            },
            "from": skip,
            "size": size,
            "track_total_hits": True  # This ensures we get accurate total hits
        }
        
        result = es.search(index="train_data", body=body)
        
        total_hits = result["hits"]["total"]["value"]
        total_pages = ceil(total_hits / size)
        
        return {
            "data": result["hits"]["hits"],
            "pagination": {
                "current_page": page,
                "total_pages": total_pages,
                "total_records": total_hits,
                "page_size": size,
                "has_next": page < total_pages,
                "has_previous": page > 1
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# You might also want to add a method to get all records with pagination
@app.get("/records")
async def get_all_records(
    page: Optional[int] = Query(1, description="Page number", ge=1),
    size: Optional[int] = Query(10, description="Results per page", ge=1, le=100),
    sort_by: Optional[str] = Query(None, description="Field to sort by"),
    order: Optional[str] = Query("asc", description="Sort order (asc/desc)")
):
    try:
        skip = (page - 1) * size
        
        body = {
            "query": {
                "match_all": {}
            },
            "from": skip,
            "size": size,
            "track_total_hits": True
        }
        
        # Add sorting if specified
        if sort_by:
            body["sort"] = [{
                sort_by: {
                    "order": order.lower()
                }
            }]
        
        result = es.search(index="train_data", body=body)
        
        total_hits = result["hits"]["total"]["value"]
        total_pages = ceil(total_hits / size)
        
        return {
            "data": result["hits"]["hits"],
            "pagination": {
                "current_page": page,
                "total_pages": total_pages,
                "total_records": total_hits,
                "page_size": size,
                "has_next": page < total_pages,
                "has_previous": page > 1
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))