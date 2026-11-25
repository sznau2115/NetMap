from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Connection(Base):
    __tablename__ = "connections"

    id = Column(Integer, primary_key=True, index=True)

    source_device_id = Column(
        Integer,
        ForeignKey("devices.id"),
        nullable=False
    )

    target_device_id = Column(
        Integer,
        ForeignKey("devices.id"),
        nullable=False
    )

    connection_type = Column(String(30), default="ethernet")
    discovery_source = Column(String(20), default="manual")

    source_port = Column(String(50), nullable=True)
    target_port = Column(String(50), nullable=True)

    source_device = relationship(
        "Device",
        foreign_keys=[source_device_id],
        back_populates="outgoing_connections"
    )

    target_device = relationship(
        "Device",
        foreign_keys=[target_device_id],
        back_populates="incoming_connections"
    )