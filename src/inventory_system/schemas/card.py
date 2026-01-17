from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import date

class CardCreateSchema(BaseModel):
    inventory_number: str
    inventory_number_eskd: str
    gas_pipeline_section: str
    described_name: str
    build_date_dn: date
    total_length: float
    folder: str
    address: str

    pressure_type_id: int
    property_type_id: int
    district_id: int
    object_name_id: int

    cut_type_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class CardUpdateSchema(BaseModel):
    inventory_number: Optional[str] = None
    inventory_number_eskd: Optional[str] = None
    gas_pipeline_section: Optional[str] = None
    address: Optional[str] = None
    folder: Optional[str] = None
    described_name: Optional[str] = None
    total_length: Optional[float] = None
    build_date_dn: Optional[date] = None
    
    pressure_type_id: Optional[int] = None
    property_type_id: Optional[int] = None
    district_id: Optional[int] = None
    object_name_id: Optional[int] = None
    cut_type_id: Optional[int] = None

class DisplayMainPageCard(BaseModel):
    id: int
    inventory_number: str
    inventory_number_eskd: str
    gas_pipeline_section: str
    pressure_type_id: int
    described_name: str
    build_date_dn: date
    property_type_id: int
    total_length: float
    district_id: int
    object_name_id: int
    address: str
    folder: str
    cut_type_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)