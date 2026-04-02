from typing import Type, TypeVar, List
from sqlalchemy import select

from inventory_system.schemas import (
    LookupItemSchema, 
    LookupCreateSchema, 
    LookupUpdateSchema,
    CutTypeCreateSchema
)
from inventory_system.models import CutType
from inventory_system.exceptions.lookups import LookupRecordNotFoundError
from utils.db_utils import DatabaseManager


T = TypeVar("T") 

class LookupRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.manager = db_manager

    async def get_all(self, model_class: Type[T]) -> List[LookupItemSchema]:
        db_records = await self.manager.get_all_lookups(model_class)
        return [LookupItemSchema.model_validate(r) for r in db_records]

    async def create(self, model_class: Type[T], schema: LookupCreateSchema) -> LookupItemSchema:
        db_record = await self.manager.get_or_create_lookup(
            model_class, schema.value, f"Failed to add {model_class.__name__}"
        )
        return LookupItemSchema.model_validate(db_record)

    async def create_cut_type(self, schema: CutTypeCreateSchema) -> LookupItemSchema:
        query = select(CutType).where(
            (CutType.value == schema.value) | (CutType.code == schema.code)
        )
        existing = await self.manager.get_first(query, err_msg="Error checking cut type")
        
        if existing:
            return LookupItemSchema.model_validate(existing)

        new_cut_type = CutType(value=schema.value, code=schema.code)
        db_record = await self.manager.add_record(new_cut_type, err_msg="Failed to add cut type")
        
        return LookupItemSchema.model_validate(db_record)

    async def update(self, model_class: Type[T], record_id: int, schema: LookupUpdateSchema) -> LookupItemSchema:
        db_record = await self.manager.update_lookup_record(
            model_class, record_id, schema.value, f"Failed to update {model_class.__name__}"
        )
        
        if not db_record:
            raise LookupRecordNotFoundError(record_id)
            
        return LookupItemSchema.model_validate(db_record)

    async def delete(self, model_class: Type[T], record_id: int) -> None:
        deleted = await self.manager.delete_record_by_id(
            model_class, record_id, f"Failed to delete {model_class.__name__}"
        )
        if not deleted:
            raise LookupRecordNotFoundError(record_id)