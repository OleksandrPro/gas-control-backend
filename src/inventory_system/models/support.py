from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column
from inventory_system.models import Base


class PropertyType(Base):
    __tablename__ = "property_types"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    value: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)


class District(Base):
    __tablename__ = "districts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    value: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)


class ObjectName(Base):
    __tablename__ = "object_names"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    value: Mapped[str] = mapped_column(String(70), unique=True, nullable=False)


class CutType(Base):
    __tablename__ = "cut_types"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    value: Mapped[str] = mapped_column(String(70), unique=True, nullable=False)

    # Technical code for business logic ("full", "partial", "none")
    # nullable=True is set temporarily to avoid migration errors on existing data,
    # but logically it should be unique and required.
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=True)


class GroundLevel(Base):
    __tablename__ = "groung_levels"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    value: Mapped[str] = mapped_column(String(70), unique=True, nullable=False)

class PipeMaterial(Base):
    __tablename__ = "pipe_materials"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    value: Mapped[str] = mapped_column(String(70), unique=True, nullable=False)

class PressureType(Base):
    __tablename__ = "pressure_types"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    value: Mapped[str] = mapped_column(String(70), unique=True, nullable=False)