from typing import List

from pydantic import BaseModel


class SearchResponse(BaseModel):
    Name: str
    Genres: List[str]
    Actors: List[str]
    Director: str
    Description: str
    Score: float


class SearchListResponse(BaseModel):
    results: List[SearchResponse]
