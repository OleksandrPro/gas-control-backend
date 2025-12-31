from typing import Optional
from pydantic import BaseModel, ConfigDict
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

    pressure_type: int

    # TODO Clarify what does this column in original table even mean
    described_name: str

    # TODO Clarify what does 'OZ' mean
    build_date_dn: date

    property_type: int

    total_length: float

    district: int
    object_name: str

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
