from typing import Generic, TypeVar, List
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")

class LookupCreateSchema(BaseModel):
    value: str

class LookupItemSchema(BaseModel):
    id: int
    value: str

    model_config = ConfigDict(from_attributes=True)

class LookupUpdateSchema(BaseModel):
    value: str

class CutTypeCreateSchema(LookupCreateSchema):
    code: str

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]

    total: int
    current_page: int
    total_pages: int
    size: int

    model_config = ConfigDict(
        from_attributes=True, 
        arbitrary_types_allowed=True
    )
