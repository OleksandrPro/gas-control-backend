from typing import Literal, Union, Optional, List
from enum import Enum
from pydantic import BaseModel, ConfigDict

class ColumnTypeEnum(str, Enum):
    BALANCE = "balance"
    FACT = "fact"
    CUT = "cut"

class EquipmentDataBase(BaseModel):
    column_type: ColumnTypeEnum
    model_config = ConfigDict(from_attributes=True)

# Concrete Data Schemas
class PipeDataCreate(EquipmentDataBase):
    type: Literal["pipe_data"] = "pipe_data"
    diameter: float
    length: float
    material_id: Optional[int] = None
    groung_level_id: Optional[int] = None

class ValveDataCreate(EquipmentDataBase):
    type: Literal["valve_data"] = "valve_data"
    diameter: float
    quantity: int

# Union for creating data
EquipmentDataCreate = Union[PipeDataCreate, ValveDataCreate]


# Item Schema (Container)
class EquipmentItemCreate(BaseModel):
    item_type: str # "pipe" or "valve"
    description: str
    data_entries: List[EquipmentDataCreate]

    model_config = ConfigDict(from_attributes=True)

class PipeDataRead(PipeDataCreate):
    id: int

class ValveDataRead(ValveDataCreate):
    id: int

EquipmentDataRead = Union[PipeDataRead, ValveDataRead]

class EquipmentItemRead(BaseModel):
    id: int
    card_id: int
    item_type: str
    description: str
    data_entries: List[EquipmentDataRead]

    model_config = ConfigDict(from_attributes=True)