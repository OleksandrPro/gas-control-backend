from typing import List, Optional
from sqlalchemy import String, Integer, Float, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from inventory_system.models.base import Base
from ..constants import ColumnType

# LEVEL 1: CONTAINER (Logical Equipment Unit)
class EquipmentItem(Base):
    __tablename__ = "equipment_items"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id"), nullable=False)
    card: Mapped["Card"] = relationship(back_populates="equipment_list")
    
    item_type: Mapped[str] = mapped_column(String(50), nullable=False)

    # Stores the raw string
    description: Mapped[str] = mapped_column(String(500), nullable=False)

    # Relation to specific data entries (One-to-Many).
    # One item can have multiple data entries (Balance, Fact, Cut)
    data_entries: Mapped[List["EquipmentData"]] = relationship(back_populates="item", cascade="all, delete-orphan")


# LEVEL 2: BASE DATA CLASS (Abstraction)
class EquipmentData(Base):
    """
    Base table for storing data. Contains common fields and the polymorphic discriminator.
    """
    __tablename__ = "equipment_data"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Reference to the logical container
    item_id: Mapped[int] = mapped_column(ForeignKey("equipment_items.id"), nullable=False)
    item: Mapped["EquipmentItem"] = relationship(back_populates="data_entries")
    
    column_type: Mapped[ColumnType] = mapped_column(SQLEnum(ColumnType), nullable=False)
    type: Mapped[str] = mapped_column(String(50)) 

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "base_data",
    }


# LEVEL 3: CONCRETE EQUIPMENT TYPES

class PipeData(EquipmentData):
    __tablename__ = "equipment_data_pipes"
    id: Mapped[int] = mapped_column(ForeignKey("equipment_data.id"), primary_key=True)
    
    diameter: Mapped[float] = mapped_column(Float, nullable=True)
    length: Mapped[float] = mapped_column(Float, nullable=True)

    groung_level_id: Mapped[int] = mapped_column(ForeignKey("groung_levels.id"))
    groung_level: Mapped["GroundLevel"] = relationship()

    material_id: Mapped[int] = mapped_column(ForeignKey("pipe_materials.id"))
    material: Mapped["PipeMaterial"] = relationship()

    __mapper_args__ = {
        "polymorphic_identity": "pipe_data",
    }


class ValveData(EquipmentData):
    __tablename__ = "equipment_data_valves"   
    id: Mapped[int] = mapped_column(ForeignKey("equipment_data.id"), primary_key=True)
    
    diameter: Mapped[float] = mapped_column(Float, nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "valve_data",
    }


class GenericData(EquipmentData):
    """
    Fallback table for equipment types that don't have a specific schema yet.
    Used for GK, regulators, etc., until they are properly modeled.
    """
    __tablename__ = "equipment_data_generic"
    id: Mapped[int] = mapped_column(ForeignKey("equipment_data.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "generic_data",
    }