from typing import List, Annotated
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from inventory_system.models import (
    District, 
    PropertyType, 
    ObjectName, 
    CutType,
    GroundLevel,
    PipeMaterial,
    PressureType
)

from inventory_system.schemas import (
    LookupItemSchema, 
    LookupCreateSchema, 
    LookupUpdateSchema,
    CutTypeCreateSchema
)
from utils.db_utils import DatabaseManager
from inventory_system.repositories.lookups import LookupRepository
from database import get_session

lookups_router = APIRouter(prefix="/dictionaries", tags=["Lookups"])

def get_lookup_repo(session: AsyncSession = Depends(get_session)) -> LookupRepository:
    return LookupRepository(DatabaseManager(session))


# --- GET Endpoints ---

@lookups_router.get("/districts", response_model=List[LookupItemSchema])
async def get_districts(repo: Annotated[LookupRepository, Depends(get_lookup_repo)]):
    return await repo.get_all(District)

@lookups_router.get("/property-types", response_model=List[LookupItemSchema])
async def get_property_types(repo: Annotated[LookupRepository, Depends(get_lookup_repo)]):
    return await repo.get_all(PropertyType)

@lookups_router.get("/object-names", response_model=List[LookupItemSchema])
async def get_object_names(repo: Annotated[LookupRepository, Depends(get_lookup_repo)]):
    return await repo.get_all(ObjectName)

@lookups_router.get("/cut-types", response_model=List[LookupItemSchema])
async def get_cut_types(repo: Annotated[LookupRepository, Depends(get_lookup_repo)]):
    return await repo.get_all(CutType)

@lookups_router.get("/ground-levels", response_model=List[LookupItemSchema])
async def get_ground_levels(repo: Annotated[LookupRepository, Depends(get_lookup_repo)]):
    return await repo.get_all(GroundLevel)

@lookups_router.get("/pipe-materials", response_model=List[LookupItemSchema])
async def get_pipe_materials(repo: Annotated[LookupRepository, Depends(get_lookup_repo)]):
    return await repo.get_all(PipeMaterial)

@lookups_router.get("/pressure-types", response_model=List[LookupItemSchema])
async def get_pressure_types(repo: Annotated[LookupRepository, Depends(get_lookup_repo)]):
    return await repo.get_all(PressureType)


# --- POST Endpoints ---

@lookups_router.post("/districts", response_model=LookupItemSchema)
async def add_district(
    schema: LookupCreateSchema, 
    repo: Annotated[LookupRepository, Depends(get_lookup_repo)]
):
    return await repo.create(District, schema.value, "Failed to add district")

@lookups_router.post("/property-types", response_model=LookupItemSchema)
async def add_property_type(
    schema: LookupCreateSchema, 
    repo: Annotated[LookupRepository, Depends(get_lookup_repo)]
):
    return await repo.create(PropertyType, schema.value, "Failed to add property type")

@lookups_router.post("/object-names", response_model=LookupItemSchema)
async def add_object_name(
    schema: LookupCreateSchema, 
    repo: Annotated[LookupRepository, Depends(get_lookup_repo)]
):
    return await repo.create(ObjectName, schema.value, "Failed to add object name")

@lookups_router.post("/cut-types", response_model=LookupItemSchema)
async def add_cut_type(
    schema: CutTypeCreateSchema,
    repo: Annotated[LookupRepository, Depends(get_lookup_repo)]
):
    return await repo.create_cut_type(schema)

@lookups_router.post("/ground-levels", response_model=LookupItemSchema)
async def add_ground_level(
    schema: LookupCreateSchema, 
    repo: Annotated[LookupRepository, Depends(get_lookup_repo)]
):
    return await repo.create(GroundLevel, schema.value, "Failed to add ground level")

@lookups_router.post("/pipe-materials", response_model=LookupItemSchema)
async def add_pipe_material(
    schema: LookupCreateSchema, 
    repo: Annotated[LookupRepository, Depends(get_lookup_repo)]
):
    return await repo.create(PipeMaterial, schema.value, "Failed to add pipe material")

@lookups_router.post("/pressure-types", response_model=LookupItemSchema)
async def add_pressure_type(
    schema: LookupCreateSchema, 
    repo: Annotated[LookupRepository, Depends(get_lookup_repo)]
):
    return await repo.create(PressureType, schema.value, "Failed to add pressure type")


# --- PUT Endpoints ---

@lookups_router.put("/districts/{record_id}", response_model=LookupItemSchema)
async def update_district(
    record_id: int,
    schema: LookupUpdateSchema, 
    repo: Annotated[LookupRepository, Depends(get_lookup_repo)]
):
    return await repo.update(District, record_id, schema.value, "Failed to update district")

@lookups_router.put("/property-types/{record_id}", response_model=LookupItemSchema)
async def update_property_type(
    record_id: int,
    schema: LookupUpdateSchema, 
    repo: Annotated[LookupRepository, Depends(get_lookup_repo)]
):
    return await repo.update(PropertyType, record_id, schema.value, "Failed to update property type")

@lookups_router.put("/object-names/{record_id}", response_model=LookupItemSchema)
async def update_object_name(
    record_id: int,
    schema: LookupUpdateSchema, 
    repo: Annotated[LookupRepository, Depends(get_lookup_repo)]
):
    return await repo.update(ObjectName, record_id, schema.value, "Failed to update object name")

@lookups_router.put("/cut-types/{record_id}", response_model=LookupItemSchema)
async def update_cut_type(
    record_id: int,
    schema: LookupUpdateSchema, 
    repo: Annotated[LookupRepository, Depends(get_lookup_repo)]
):
    return await repo.update(CutType, record_id, schema.value, "Failed to update cut type")

@lookups_router.put("/ground-levels/{record_id}", response_model=LookupItemSchema)
async def update_ground_level(
    record_id: int,
    schema: LookupUpdateSchema, 
    repo: Annotated[LookupRepository, Depends(get_lookup_repo)]
):
    return await repo.update(GroundLevel, record_id, schema.value, "Failed to update ground level")

@lookups_router.put("/pipe-materials/{record_id}", response_model=LookupItemSchema)
async def update_pipe_material(
    record_id: int,
    schema: LookupUpdateSchema, 
    repo: Annotated[LookupRepository, Depends(get_lookup_repo)]
):
    return await repo.update(PipeMaterial, record_id, schema.value, "Failed to update pipe material")

@lookups_router.put("/pressure-types/{record_id}", response_model=LookupItemSchema)
async def update_pipe_material(
    record_id: int,
    schema: LookupUpdateSchema, 
    repo: Annotated[LookupRepository, Depends(get_lookup_repo)]
):
    return await repo.update(PressureType, record_id, schema.value, "Failed to update ressure type")

# --- DELETE Endpoints ---

@lookups_router.delete("/districts/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_district(
    record_id: int,
    repo: Annotated[LookupRepository, Depends(get_lookup_repo)]
):
    await repo.delete(District, record_id, "Failed to delete district")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@lookups_router.delete("/property-types/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_property_type(
    record_id: int,
    repo: Annotated[LookupRepository, Depends(get_lookup_repo)]
):
    await repo.delete(PropertyType, record_id, "Failed to delete property type")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@lookups_router.delete("/object-names/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_object_name(
    record_id: int,
    repo: Annotated[LookupRepository, Depends(get_lookup_repo)]
):
    await repo.delete(ObjectName, record_id, "Failed to delete object name")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@lookups_router.delete("/cut-types/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cut_type(
    record_id: int,
    repo: Annotated[LookupRepository, Depends(get_lookup_repo)]
):
    await repo.delete(CutType, record_id, "Failed to delete cut type")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@lookups_router.delete("/ground-levels/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ground_level(
    record_id: int,
    repo: Annotated[LookupRepository, Depends(get_lookup_repo)]
):
    await repo.delete(GroundLevel, record_id, "Failed to delete ground level")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@lookups_router.delete("/pipe-materials/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pipe_material(
    record_id: int,
    repo: Annotated[LookupRepository, Depends(get_lookup_repo)]
):
    await repo.delete(PipeMaterial, record_id, "Failed to delete pipe material")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@lookups_router.delete("/pressure-types/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pressure_type(
    record_id: int,
    repo: Annotated[LookupRepository, Depends(get_lookup_repo)]
):
    await repo.delete(PressureType, record_id, "Failed to delete pressure type")
    return Response(status_code=status.HTTP_204_NO_CONTENT)