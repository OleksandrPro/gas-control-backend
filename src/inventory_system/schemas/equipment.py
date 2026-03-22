from typing import Literal, Union, Optional, List, Annotated
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field

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

class EquipmentItemBase(BaseModel):
    item_type: str # "pipe" or "valve"
    description: str

# Item Schema (Container)
class EquipmentItemCreate(BaseModel):
    data_entries: List[EquipmentDataCreate]

    model_config = ConfigDict(from_attributes=True)

class PipeDataUpdate(PipeDataCreate):
    id: Optional[int] = None

class ValveDataUpdate(ValveDataCreate):
    id: Optional[int] = None

EquipmentDataUpdateType = Union[PipeDataUpdate, ValveDataUpdate]

class EquipmentItemUpdate(BaseModel):
    description: Optional[str] = None
    data_entries: Optional[List[EquipmentDataUpdateType]] = None 

class PipeDataRead(PipeDataCreate):
    id: int

class ValveDataRead(ValveDataCreate):
    id: int

EquipmentDataRead = Annotated[
    Union[PipeDataRead, ValveDataRead], 
    Field(discriminator='type')
]

class EquipmentItemRead(EquipmentItemBase):
    id: int
    card_id: int
    data_entries: List[EquipmentDataRead]

    model_config = ConfigDict(from_attributes=True)