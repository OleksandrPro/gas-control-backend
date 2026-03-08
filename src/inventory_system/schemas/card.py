from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from datetime import date
from fastapi import Query

class CardCreateSchema(BaseModel):
    inventory_number: str
    inventory_number_eskd: str
    gas_pipeline_section: str
    described_name: str
    build_date_dn: date
    total_length_balance: float
    total_length_fact: float
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
    total_length_balance: Optional[float] = None
    total_length_fact: Optional[float] = None
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
    total_length_balance: float
    total_length_fact: float
    district_id: int
    object_name_id: int
    address: str
    folder: str
    cut_type_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class CardFilter(BaseModel):
    # Search filters
    inventory_number_like: Optional[str] = None

    inventory_numbers: Optional[List[str]] = Field(Query(None, alias="inventory_number"))
    folders: Optional[List[str]] = Field(Query(None, alias="folder"))
    district_ids: Optional[List[int]] = Field(Query(None, alias="district_id"))
    pressure_type_ids: Optional[List[int]] = Field(Query(None, alias="pressure_type_id"))
    property_type_ids: Optional[List[int]] = Field(Query(None, alias="property_type_id"))
    object_name_ids: Optional[List[int]] = Field(Query(None, alias="object_name_id"))
    cut_type_ids: Optional[List[int]] = Field(Query(None, alias="cut_type_id"))

    pipe_material_ids: Optional[List[int]] = Field(Query(None, alias="pipe_material_id"))
    pipe_diameter_equal: Optional[float] = None
    pipe_diameter_min: Optional[float] = None
    pipe_diameter_max: Optional[float] = None
    groung_level_ids: Optional[List[int]] = Field(Query(None, alias="groung_level_id"))

    data_column_types: Optional[List[str]] = Field(Query(None, alias="column_type"))

    # Pagination
    page: int = Field(default=1, ge=1)
    size: int = Field(default=50, ge=1, le=100)