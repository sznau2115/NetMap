from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)

    # router, switch, computer, phone
    device_type = Column(String(30), nullable=False)

    ip_address = Column(String(45), nullable=True)

    # Pozycja na planie piętra, wartości od 0 do 1
    x = Column(Float, default=0.5, nullable=False)
    y = Column(Float, default=0.5, nullable=False)

    floor_id = Column(
        Integer,
        ForeignKey("floors.id"),
        nullable=False
    )

    floor = relationship("Floor", back_populates="devices")

    outgoing_connections = relationship(
        "Connection",
        foreign_keys="Connection.source_device_id",
        back_populates="source_device",
        cascade="all, delete-orphan"
    )

    incoming_connections = relationship(
        "Connection",
        foreign_keys="Connection.target_device_id",
        back_populates="target_device",
        cascade="all, delete-orphan"
    )