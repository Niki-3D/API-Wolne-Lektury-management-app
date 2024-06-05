from pydantic import BaseModel
from typing import List, Optional

class BookModel(BaseModel):
    title: str
    author: str
    genre: str

class FiltersModel(BaseModel):
    author: Optional[List[str]] = None
    genre: Optional[List[str]] = None
