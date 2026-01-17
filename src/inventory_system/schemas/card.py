from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import date

class CardCreateSchema(BaseModel):
    inventory_number: str
    inventory_number_eskd: str
    gas_pipeline_section: str
    pressure_type: Optional[int] = None
    described_name: str
    build_date_dn: date
    total_length: float
    folder: str
    
    property_type_id: int = Field(alias="property_type")
    district_id: int = Field(alias="district")
    object_name_id: int = Field(alias="object_name")
    
    cut_type_id: Optional[int] = Field(default=None, alias="cut_type")

    model_config = ConfigDict(populate_by_name=True)

class CardUpdateSchema(BaseModel):
    inventory_number: Optional[str] = None
    inventory_number_eskd: Optional[str] = None
    gas_pipeline_section: Optional[str] = None
    address: Optional[str] = None
    folder: Optional[str] = None
    described_name: Optional[str] = None
    total_length: Optional[float] = None
    build_date_dn: Optional[date] = None
    
    property_type_id: Optional[int] = None
    district_id: Optional[int] = None
    object_name_id: Optional[int] = None
    cut_type_id: Optional[int] = None

class DisplayMainPageCard(BaseModel):
    inventory_number: str
    inventory_number_eskd: str

    gas_pipeline_section: str

    pressure_type_id: int

    # TODO Clarify what does this column in original table even mean
    described_name: str

    # TODO Clarify what does 'OZ' mean
    build_date_dn: date

    property_type_id: int

    total_length: float

    district_id: int
    object_name_id: int

    address: str

    folder: str
    cut_type_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)