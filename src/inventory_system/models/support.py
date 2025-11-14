from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from base import Base


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
