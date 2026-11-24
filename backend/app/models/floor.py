from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from backend.app.database import Base
class Floor(Base):
    __tablename__ = "floors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    plan_image = Column(String(255), nullable=True)

    building_id = Column(
        Integer,
        back_populates="floors",
        nullable=False,
    )
    building = relationship(
        "Building",
        back_populates="floors"
    )
    devices = relationship(
        "Device",
        back_populates="floor",
        cascade="all, delete-orphan"
    )