from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.connection import Connection
from app.models.device import Device

router = APIRouter(prefix="/api", tags=["Connections"])

@router.get("/devices/{device_id}/connections")
def get_connections(device_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Connection)
        .join(Device, Connection.source_device_id == Device.id)
        .filter(Device.floor_id == device_id)
        .all()
    )

@router.post("/connections")
def create_connection(
     source_device_id: int,
     target_device_id: int,
     connection_type: str = "ethernet",
     source_port: str | None = None,
     target_port: str | None = None,
     db: Session = Depends(get_db)
):
    if source_device_id == target_device_id:
        raise HTTPException(status_code=400, detail="Source and target devices cannot be the same")
    source = db.query(Device).filter(Device.id == source_device_id).first()

    target = db.query(Device).filter(Device.id == target_device_id).first()

    if not source or not target:
        raise HTTPException(status_code=404, detail="One or both devices not found")
    if source.floor_id != target.floor_id:
        raise HTTPException(status_code=400, detail="Devices must be on the same floor")

    connection = Connection(
        source_device_id=source_device_id,
        target_device_id=target_device_id,
        connection_type=connection_type,
        discovery_source="manual",
        source_port=source_port,
        target_port=target_port
    )
    db.add(connection)
    db.commit()
    db.refresh(connection)
    return connection

@router.delete("/connections/{connection_id}")
def delete_connection(connection_id: int, db: Session = Depends(get_db)):
    connection = db.query(Connection).filter(Connection.id == connection_id).first()
    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")
    db.delete(connection)
    db.commit()
    return {"detail": "Connection deleted"}
    