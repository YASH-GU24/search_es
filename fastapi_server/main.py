import os

from elasticsearch import Elasticsearch
from elasticsearch import exceptions as es_exceptions
from fastapi import FastAPI, HTTPException, Query
from schema.search import SearchListResponse

app = FastAPI()

# Connect to Elasticsearch
ES_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
try:
    es = Elasticsearch(ES_URL)
    if not es.ping():
        raise HTTPException(
            status_code=500, detail="Elasticsearch server is not reachable"
        )
except es_exceptions.ConnectionError:
    raise HTTPException(status_code=500, detail="Failed to connect to Elasticsearch")

INDEX_NAME = "movies"


@app.get("/search/", response_model=SearchListResponse)
async def search_movies(
    query: str = Query(None, title="Search Query"),
    genre: str = Query(None, title="Genre Filter"),
    director: str = Query(None, title="Director Filter"),
    limit: int = Query(10, title="Limit Results"),
):
    """Search movies in Elasticsearch with optional filters"""
    try:
        es_query = {
            "bool": {
                "must": (
                    [
                        {
                            "multi_match": {
                                "query": query,
                                "fields": ["Name", "Description", "Actors"],
                            }
                        }
                    ]
                    if query
                    else []
                ),
                "filter": [],
            }
        }
        if genre:
            es_query["bool"]["filter"].append({"term": {"Genres": genre}})
        if director:
            es_query["bool"]["filter"].append({"term": {"Director": director}})

        response = es.search(index=INDEX_NAME, query=es_query, size=limit)
    except es_exceptions.NotFoundError:
        raise HTTPException(status_code=404, detail="Index not found")
    except es_exceptions.RequestError as e:
        raise HTTPException(
            status_code=400, detail=f"Elasticsearch request error: {str(e)}"
        )
    except es_exceptions.ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=f"Elasticsearch error: {str(e)}")

    results = []
    for hit in response.get("hits", {}).get("hits", []):
        source = hit.get("_source", {})
        results.append(
            {
                "Name": source.get("Name", "Unknown"),
                "Genres": source.get("Genres", []),
                "Actors": source.get("Actors", []),
                "Director": source.get("Director", "Unknown"),
                "Description": source.get("Description", "No description available"),
                "Score": hit.get("_score", 0),
            }
        )

    return SearchListResponse(results=results)
