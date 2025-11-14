from sqlalchemy import String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from base import Base


class Card(Base):
    __tablename__ = "cards"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    inventory_number: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )
    inventory_number_eskd: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )

    gas_pipeline_section: Mapped[str] = mapped_column(
        String(300), unique=True, nullable=False
    )

    property_type_id: Mapped[int] = mapped_column(ForeignKey("property_types.id"))
    property_type: Mapped["PropertyType"] = relationship()

    # TODO Clarify what does this column in original table even mean
    main_tool: Mapped[str] = mapped_column(String(300), unique=True, nullable=False)

    # TODO Clarify what does 'OZ' mean
    build_date_oz: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    total_length: Mapped[float] = mapped_column(Float, nullable=False)

    district_id: Mapped[int] = mapped_column(ForeignKey("districts.id"))
    district: Mapped["District"] = relationship()

    object_name_id: Mapped[int] = mapped_column(ForeignKey("object_names.id"))
    object_name: Mapped["ObjectName"] = relationship()
