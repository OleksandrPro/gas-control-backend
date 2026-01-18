from typing import List, Annotated
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from inventory_system.models import (
    District, 
    PropertyType, 
    ObjectName, 
    CutType,
    GroundLevel,
    PipeMaterial,
    PressureType
)

from inventory_system.schemas import LookupItemSchema, LookupCreateSchema, LookupUpdateSchema
from utils.db_utils import DatabaseManager
from database import get_session

lookups_router = APIRouter(prefix="/dictionaries", tags=["Lookups"])

def get_manager(session: AsyncSession = Depends(get_session)) -> DatabaseManager:
    return DatabaseManager(session)


# --- GET Endpoints ---

@lookups_router.get("/districts", response_model=List[LookupItemSchema])
async def get_districts(manager: Annotated[DatabaseManager, Depends(get_manager)]):
    return await manager.get_all_lookups(District)

@lookups_router.get("/property-types", response_model=List[LookupItemSchema])
async def get_property_types(manager: Annotated[DatabaseManager, Depends(get_manager)]):
    return await manager.get_all_lookups(PropertyType)

@lookups_router.get("/object-names", response_model=List[LookupItemSchema])
async def get_object_names(manager: Annotated[DatabaseManager, Depends(get_manager)]):
    return await manager.get_all_lookups(ObjectName)

@lookups_router.get("/cut-types", response_model=List[LookupItemSchema])
async def get_cut_types(manager: Annotated[DatabaseManager, Depends(get_manager)]):
    return await manager.get_all_lookups(CutType)

@lookups_router.get("/ground-levels", response_model=List[LookupItemSchema])
async def get_ground_levels(manager: Annotated[DatabaseManager, Depends(get_manager)]):
    return await manager.get_all_lookups(GroundLevel)

@lookups_router.get("/pipe-materials", response_model=List[LookupItemSchema])
async def get_pipe_materials(manager: Annotated[DatabaseManager, Depends(get_manager)]):
    return await manager.get_all_lookups(PipeMaterial)

@lookups_router.get("/pressure-types", response_model=List[LookupItemSchema])
async def get_pressure_types(manager: Annotated[DatabaseManager, Depends(get_manager)]):
    return await manager.get_all_lookups(PressureType)


# --- POST Endpoints ---

@lookups_router.post("/districts", response_model=LookupItemSchema)
async def add_district(
    schema: LookupCreateSchema, 
    manager: Annotated[DatabaseManager, Depends(get_manager)]
):
    return await manager.get_or_create_lookup(District, schema.value, "Failed to add district")

@lookups_router.post("/property-types", response_model=LookupItemSchema)
async def add_property_type(
    schema: LookupCreateSchema, 
    manager: Annotated[DatabaseManager, Depends(get_manager)]
):
    return await manager.get_or_create_lookup(PropertyType, schema.value, "Failed to add property type")

@lookups_router.post("/object-names", response_model=LookupItemSchema)
async def add_object_name(
    schema: LookupCreateSchema, 
    manager: Annotated[DatabaseManager, Depends(get_manager)]
):
    return await manager.get_or_create_lookup(ObjectName, schema.value, "Failed to add object name")

@lookups_router.post("/cut-types", response_model=LookupItemSchema)
async def add_cut_type(
    schema: LookupCreateSchema, 
    manager: Annotated[DatabaseManager, Depends(get_manager)]
):
    return await manager.get_or_create_lookup(CutType, schema.value, "Failed to add cut type")

@lookups_router.post("/ground-levels", response_model=LookupItemSchema)
async def add_ground_level(
    schema: LookupCreateSchema, 
    manager: Annotated[DatabaseManager, Depends(get_manager)]
):
    return await manager.get_or_create_lookup(GroundLevel, schema.value, "Failed to add ground level")

@lookups_router.post("/pipe-materials", response_model=LookupItemSchema)
async def add_pipe_material(
    schema: LookupCreateSchema, 
    manager: Annotated[DatabaseManager, Depends(get_manager)]
):
    return await manager.get_or_create_lookup(PipeMaterial, schema.value, "Failed to add pipe material")

@lookups_router.post("/pressure-types", response_model=LookupItemSchema)
async def add_pressure_type(
    schema: LookupCreateSchema, 
    manager: Annotated[DatabaseManager, Depends(get_manager)]
):
    return await manager.get_or_create_lookup(PressureType, schema.value, "Failed to add pressure type")


# --- PUT Endpoints ---

@lookups_router.put("/districts/{record_id}", response_model=LookupItemSchema)
async def update_district(
    record_id: int,
    schema: LookupUpdateSchema, 
    manager: Annotated[DatabaseManager, Depends(get_manager)]
):
    return await manager.update_lookup_record(District, record_id, schema.value, "Failed to update district")

@lookups_router.put("/property-types/{record_id}", response_model=LookupItemSchema)
async def update_property_type(
    record_id: int,
    schema: LookupUpdateSchema, 
    manager: Annotated[DatabaseManager, Depends(get_manager)]
):
    return await manager.update_lookup_record(PropertyType, record_id, schema.value, "Failed to update property type")

@lookups_router.put("/object-names/{record_id}", response_model=LookupItemSchema)
async def update_object_name(
    record_id: int,
    schema: LookupUpdateSchema, 
    manager: Annotated[DatabaseManager, Depends(get_manager)]
):
    return await manager.update_lookup_record(ObjectName, record_id, schema.value, "Failed to update object name")

@lookups_router.put("/cut-types/{record_id}", response_model=LookupItemSchema)
async def update_cut_type(
    record_id: int,
    schema: LookupUpdateSchema, 
    manager: Annotated[DatabaseManager, Depends(get_manager)]
):
    return await manager.update_lookup_record(CutType, record_id, schema.value, "Failed to update cut type")

@lookups_router.put("/ground-levels/{record_id}", response_model=LookupItemSchema)
async def update_ground_level(
    record_id: int,
    schema: LookupUpdateSchema, 
    manager: Annotated[DatabaseManager, Depends(get_manager)]
):
    return await manager.update_lookup_record(GroundLevel, record_id, schema.value, "Failed to update ground level")

@lookups_router.put("/pipe-materials/{record_id}", response_model=LookupItemSchema)
async def update_pipe_material(
    record_id: int,
    schema: LookupUpdateSchema, 
    manager: Annotated[DatabaseManager, Depends(get_manager)]
):
    return await manager.update_lookup_record(PipeMaterial, record_id, schema.value, "Failed to update pipe material")

@lookups_router.put("/pressure-types/{record_id}", response_model=LookupItemSchema)
async def update_pipe_material(
    record_id: int,
    schema: LookupUpdateSchema, 
    manager: Annotated[DatabaseManager, Depends(get_manager)]
):
    return await manager.update_lookup_record(PressureType, record_id, schema.value, "Failed to update ressure type")

# --- DELETE Endpoints ---

@lookups_router.delete("/districts/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_district(
    record_id: int,
    manager: Annotated[DatabaseManager, Depends(get_manager)]
):
    await manager.delete_record_by_id(District, record_id, "Failed to delete district")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@lookups_router.delete("/property-types/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_property_type(
    record_id: int,
    manager: Annotated[DatabaseManager, Depends(get_manager)]
):
    await manager.delete_record_by_id(PropertyType, record_id, "Failed to delete property type")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@lookups_router.delete("/object-names/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_object_name(
    record_id: int,
    manager: Annotated[DatabaseManager, Depends(get_manager)]
):
    await manager.delete_record_by_id(ObjectName, record_id, "Failed to delete object name")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@lookups_router.delete("/cut-types/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cut_type(
    record_id: int,
    manager: Annotated[DatabaseManager, Depends(get_manager)]
):
    await manager.delete_record_by_id(CutType, record_id, "Failed to delete cut type")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@lookups_router.delete("/ground-levels/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ground_level(
    record_id: int,
    manager: Annotated[DatabaseManager, Depends(get_manager)]
):
    await manager.delete_record_by_id(GroundLevel, record_id, "Failed to delete ground level")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@lookups_router.delete("/pipe-materials/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pipe_material(
    record_id: int,
    manager: Annotated[DatabaseManager, Depends(get_manager)]
):
    await manager.delete_record_by_id(PipeMaterial, record_id, "Failed to delete pipe material")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@lookups_router.delete("/pressure-types/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pressure_type(
    record_id: int,
    manager: Annotated[DatabaseManager, Depends(get_manager)]
):
    await manager.delete_record_by_id(PressureType, record_id, "Failed to delete pressure type")
    return Response(status_code=status.HTTP_204_NO_CONTENT)