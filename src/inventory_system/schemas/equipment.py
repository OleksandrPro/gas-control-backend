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
    material: Optional[str] = None
    placement: Optional[str] = None

class ValveDataCreate(EquipmentDataBase):
    type: Literal["valve_data"] = "valve_data"
    diameter: float
    count: int
    model_number: Optional[str] = None

# Union for creating data
EquipmentDataCreate = Union[PipeDataCreate, ValveDataCreate]


# Item Schema (Container)
class EquipmentItemCreate(BaseModel):
    item_type: str # "pipe" or "valve"
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
    data_entries: List[EquipmentDataRead]

    model_config = ConfigDict(from_attributes=True)