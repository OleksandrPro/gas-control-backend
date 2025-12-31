from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import date


class LookupCreateSchema(BaseModel):
    value: str

class LookupUpdateSchema(BaseModel):
    value: str

class LookupItemSchema(BaseModel):
    """
    Versatile schema for every lookup table item (id + value).
    """
    id: int
    value: str

    model_config = ConfigDict(from_attributes=True)

class CardCreateSchema(BaseModel):
    inventory_number: str
    inventory_number_eskd: str
    gas_pipeline_section: str
    pressure_type: Optional[int] = None
    described_name: str
    build_date_dn: date
    total_length: float
    folder: str
    
    # --- ВАЖНО: Маппинг полей ---
    # alias="property_type" позволяет принимать JSON {"property_type": 1}
    # Но в Python это будет self.property_type_id = 1
    property_type_id: int = Field(alias="property_type")
    district_id: int = Field(alias="district")
    object_name_id: int = Field(alias="object_name")
    
    # cut_type делаем Optional, чтобы его можно было не передавать
    cut_type_id: Optional[int] = Field(default=None, alias="cut_type")

    class Config:
        # Разрешаем использовать и алиасы, и реальные имена при создании
        populate_by_name = True

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


"""
ПРИ открытии карточки (есть баланс, есть по факту)
Дільниця газопровода
Діаметр
Довжина, км
Розташування
Матеріал труб
"""


class EquipmentBase(BaseModel):

    # Also known as gas_pipeline_section or 'Дільниця газопровода'
    # В заголовке секции содержится информация о 'Дільниця газопровода'
    # А само содержимое обычных строк - данные об оборудовании
    equipment: str


class PipeData(EquipmentBase):
    diameter: float
    total_length: float

    ground_level: str
    pipe_material: str


class CardEquipment(BaseModel):
    equipment: list[EquipmentBase]
