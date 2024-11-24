# Therapy Analysis

## Requirements

- Use this kaggle dataset for data. https://www.kaggle.com/datasets/thedevastator/nlp-mental-health-conversations (train.csv)
- Create a Python/FastAPI service for serving API endpoint. (Write a single unit test for this endpoint)
- API should return k-most relevant conversation list by keyword. Query parameters: k, keyword (Use elasticsearch for storing data and searching data)
- Need to setup CI/CD pipeline for automatic deployment.

## Tech-Stack

ElasticSearch, FastAPI

## Challenges

Getting started with ElasticSearch was challenging. There are 3 options to use the ElasticSearch service but selected the cloud based ElasticSearch here.

## Available API endpoints

- `/search`: Searches the records for given query.
- `/records`: Fetches all the records

## How to run

- Run the app

```shell
    uvicorn main:app --reload
```

- Test the app

```shell
    pytest test_main.py
```
