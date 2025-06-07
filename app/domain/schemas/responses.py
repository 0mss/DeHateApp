from pydantic import BaseModel
from typing import Any, Dict, Generic, List, Optional, TypeVar

T = TypeVar('T')

class ResponseBase(BaseModel):
    success: bool
    message: str

    class Config:
        arbitrary_types_allowed = True

class DataResponse(ResponseBase, Generic[T]):
    data: T

class ErrorResponse(ResponseBase):
    errors: Optional[List[Dict[str, Any]]] = None

class PaginatedResponse(DataResponse, Generic[T]):
    total: int
    page: int
    page_size: int
