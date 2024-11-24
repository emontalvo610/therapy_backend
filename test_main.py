from fastapi.testclient import TestClient
from main import app  # Replace with the correct import path for your FastAPI app
import pytest

# Create a test client for your FastAPI app
client = TestClient(app)

# Test case for the "/search" endpoint
def test_search_data():
    query = "example search"
    page = 1
    size = 10
    response = client.get("/search", params={"query": query, "page": page, "size": size})

    # Assert the status code is 200 OK
    assert response.status_code == 200

    # Check if the response contains the expected structure
    response_data = response.json()
    
    assert "data" in response_data
    assert "pagination" in response_data
    
    # Assert pagination values are correct
    pagination = response_data["pagination"]
    assert pagination["current_page"] == page
    assert pagination["page_size"] == size

    # Optional: Check if the 'data' contains hits
    assert isinstance(response_data["data"], list)

    # Optional: Assert pagination logic (optional based on total records in your ES index)
    # Example: Ensure that total_records are greater than 0 if there are any hits
    if pagination["total_records"] > 0:
        assert len(response_data["data"]) > 0
