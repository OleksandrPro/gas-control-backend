from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from inventory_system.models import Card, PropertyType, District, ObjectName
from inventory_system.repository import CardRepository
from inventory_system.schemas import CardInputSchema

from src.utils import DatabaseManager

class CardService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.manager = DatabaseManager(session)
        self.repo = CardRepository(self.manager)

    async def _get_lookup_id(self, model, value: str, err_msg: str) -> int:
        query = select(model.id).where(model.value == value)
        result = await self.manager.get_first(query)
        
        if not result:
            raise HTTPException(status_code=400, detail=f"{err_msg}: '{value}' not found")
            
        return result

    async def create_card_from_strings(self, raw_data: CardInputSchema):
        """
        Transforms string values into ids
        """
        prop_type_id = await self._get_lookup_id(PropertyType, raw_data.property_type_value, "Property type")
        district_id = await self._get_lookup_id(District, raw_data.district_value, "District")
        object_name_id = await self._get_lookup_id(ObjectName, raw_data.object_name_value, "Object name")
        
        card_dict = raw_data.model_dump(exclude={
            "property_type_value", 
            "district_value", 
            "object_name_value"
        })
        
        card_dict["property_type_id"] = prop_type_id
        card_dict["district_id"] = district_id
        card_dict["object_name_id"] = object_name_id
        
        return await self.repo.create(**card_dict)