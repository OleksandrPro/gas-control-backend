from sqlalchemy import String, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from inventory_system.models import Base


class EquipmentBase(Base):
    __tablename__ = "equipment"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    value: Mapped[str] = mapped_column(String(50), nullable=False)

    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id"), nullable=False)
    card: Mapped["Card"] = relationship(back_populates="equipment_list")

    diameter: Mapped[float] = mapped_column(Float, nullable=True)
    total_length: Mapped[float] = mapped_column(Float, nullable=True)

    groung_level_id: Mapped[int] = mapped_column(ForeignKey("groung_levels.id"), nullable=True)
    groung_level: Mapped["GroundLevel"] = relationship()

    pipe_material_id: Mapped[int] = mapped_column(ForeignKey("pipe_materials.id"), nullable=True)
    pipe_material: Mapped["PipeMaterial"] = relationship()
    