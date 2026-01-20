from pydantic import BaseModel, ConfigDict

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