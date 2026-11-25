
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.device import Device
from app.models.floor import Floor

router = APIRouter(prefix="/api", tags=["Devices"])

ALLOWED_TYPES = ["router", "switch", "computer", "phone"]


@router.get("/floors/{floor_id}/devices")
def get_devices(floor_id: int, db: Session = Depends(get_db)):
    floor = db.query(Floor).filter(Floor.id == floor_id).first()

    if not floor:
        raise HTTPException(status_code=404, detail="Floor not found")

    return db.query(Device).filter(Device.floor_id == floor_id).all()


@router.post("/floors/{floor_id}/devices")
def create_device(
    floor_id: int,
    name: str,
    device_type: str,
    ip_address: str | None = None,
    x: float = 0.5,
    y: float = 0.5,
    db: Session = Depends(get_db)
):
    floor = db.query(Floor).filter(Floor.id == floor_id).first()

    if not floor:
        raise HTTPException(status_code=404, detail="Floor not found")

    if device_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid device type")

    if not (0 <= x <= 1 and 0 <= y <= 1):
        raise HTTPException(status_code=400, detail="Coordinates must be between 0 and 1")

    device = Device(
        name=name,
        device_type=device_type,
        ip_address=ip_address,
        x=x,
        y=y,
        floor_id=floor_id
    )

    db.add(device)
    db.commit()
    db.refresh(device)

    return device


@router.delete("/devices/{device_id}")
def delete_device(device_id: int, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.id == device_id).first()

    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    db.delete(device)
    db.commit()

    return {"message": "Device deleted"}
