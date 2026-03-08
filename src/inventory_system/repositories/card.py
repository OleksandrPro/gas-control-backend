from typing import Optional, List
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from inventory_system.models import Card, EquipmentItem, EquipmentData, PipeData
from utils.db_utils import DatabaseManager
from utils.pagination import Paginator
from inventory_system.schemas.base import PaginatedResponse
from inventory_system.schemas.card import CardFilter

class CardRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.manager = db_manager
        self.paginator = Paginator(self.manager)

    async def create(self, **data) -> Card:
        new_card = Card(**data)
        result = await self.manager.add_record(new_card)
        return result

    async def get_all_cards(self) -> List[Card]:
        query = select(Card)
        return await self.manager.get_all(
            query=query, 
            err_msg=f"Error loading card table {Card.__tablename__}"
        )

    async def get_by_id(self, card_id: int) -> Optional[Card]:
        query = select(Card).where(Card.id == card_id).options(
            selectinload(Card.cut_type)
        )
        return await self.manager.get_first(
            query=query,
            err_msg=f"Error finding card with ID {card_id}"
        )
    
    async def get_card(self, id: int) -> Card:
        query = select(Card).where(Card.id == id)
        card = await self.manager.get_first(query, err_msg="Error finding card with id '{id}'")
        
        if not card:
            raise HTTPException(status_code=404, detail=f"Record with id={id} not found")
        
        return card

    def _build_filtered_query(self, filter_params: CardFilter, force_pipe_joins: bool = False):
        query = select(Card)

        if filter_params.district_ids:
            query = query.where(Card.district_id.in_(filter_params.district_ids))

        if filter_params.property_type_ids:
            query = query.where(Card.property_type_id.in_(filter_params.property_type_ids))
            
        if filter_params.pressure_type_ids:
            query = query.where(Card.pressure_type_id.in_(filter_params.pressure_type_ids))
            
        if filter_params.object_name_ids:
            query = query.where(Card.object_name_id.in_(filter_params.object_name_ids))
            
        if filter_params.cut_type_ids:
            query = query.where(Card.cut_type_id.in_(filter_params.cut_type_ids))
            
        if filter_params.folders:
            query = query.where(Card.folder.in_(filter_params.folders))
            
        if filter_params.inventory_numbers:
            query = query.where(Card.inventory_number.in_(filter_params.inventory_numbers))
            
        if filter_params.inventory_number_like:
            query = query.where(Card.inventory_number.ilike(f"%{filter_params.inventory_number_like}%"))
        
        has_pipe_filters = (
            force_pipe_joins or 
            filter_params.pipe_material_ids or 
            filter_params.pipe_diameter_equal or 
            filter_params.pipe_diameter_min or 
            filter_params.pipe_diameter_max or
            filter_params.data_column_types
        )

        if not has_pipe_filters:
            return query

        query = query.join(Card.equipment_list)
        query = query.join(EquipmentItem.data_entries)
        query = query.join(PipeData)
        
        if filter_params.pipe_material_ids:
            query = query.where(PipeData.material_id.in_(filter_params.pipe_material_ids))
        
        if filter_params.groung_level_ids:
            query = query.where(PipeData.groung_level_id.in_(filter_params.groung_level_ids))

        if filter_params.pipe_diameter_equal is not None:
            query = query.where(PipeData.diameter == filter_params.pipe_diameter_equal)

        if filter_params.pipe_diameter_min is not None:
            query = query.where(PipeData.diameter >= filter_params.pipe_diameter_min)
            
        if filter_params.pipe_diameter_max is not None:
            query = query.where(PipeData.diameter <= filter_params.pipe_diameter_max)

        if filter_params.data_column_types:
            query = query.where(EquipmentData.column_type.in_(filter_params.data_column_types))

        return query

    async def list_cards(self, filter_params: CardFilter) -> PaginatedResponse[Card]:
        query = self._build_filtered_query(filter_params)

        query = query.distinct()

        query = query.order_by(Card.id.asc())

        return await self.paginator.paginate(
            query, 
            page=filter_params.page, 
            size=filter_params.size
        )

    async def get_pipes_length_sum(self, filter_params: CardFilter) -> dict:
        query = self._build_filtered_query(filter_params, force_pipe_joins=True)
        
        query = query.with_only_columns(
            func.coalesce(func.sum(PipeData.length), 0),
            func.count(Card.id.distinct())
        )

        result = await self.manager.session.execute(query)
        total_length, count = result.one()
        
        return {
            "total_length": total_length,
            "count_cards": count
        }

    async def update(self, card_id: int, **update_data) -> Optional[Card]:
        card = await self.get_card(card_id)
        
        if not card:
            return None
            
        # update_data contains only non-None data
        for key, value in update_data.items():
            if hasattr(card, key):
                setattr(card, key, value)
        
        return await self.manager.add_record(
            card, 
            err_msg=f"Failed to update card. ID: {card_id}"
        )
    
    async def delete(self, card_id: int) -> bool:
        card = await self.get_card(card_id)
        
        if not card:
            return False
            
        await self.manager.delete_record(card, err_msg=f"Failed to delete card {card_id}")
        return True
