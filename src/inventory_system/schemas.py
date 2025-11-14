from pydantic import BaseModel
from datetime import date


class DisplayMainPageCard(BaseModel):
    inventory_number: str
    inventory_number_eskd: str

    gas_pipeline_section: str

    property_type: str

    # TODO Clarify what does this column in original table even mean
    main_tool: str

    # TODO Clarify what does 'OZ' mean
    build_date_oz: date

    total_length: float

    district: str
    object_name: str


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
