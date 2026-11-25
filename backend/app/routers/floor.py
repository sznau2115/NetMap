# backend/app/routers/floor.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pathlib import Path
import uuid

from app.database import get_db
from app.models.floor import Floor
from app.models.building import Building

router = APIRouter(prefix="/api", tags=["Floors"])


@router.get("/buildings/{building_id}/floors")
def get_floors(building_id: int, db: Session = Depends(get_db)):
    building = db.query(Building).filter(
        Building.id == building_id
    ).first()

    if not building:
        raise HTTPException(status_code=404, detail="Building not found")

    return db.query(Floor).filter(
        Floor.building_id == building_id
    ).all()


@router.post("/buildings/{building_id}/floors")
def create_floor(
    building_id: int,
    name: str,
    db: Session = Depends(get_db)
):
    building = db.query(Building).filter(
        Building.id == building_id
    ).first()

    if not building:
        raise HTTPException(status_code=404, detail="Building not found")

    floor = Floor(name=name, building_id=building_id)

    db.add(floor)
    db.commit()
    db.refresh(floor)

    return floor

UPLOAD_DIR = Path(__file__).resolve().parents[2] / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/floors/{floor_id}/plan")
async def upload_floor_plan(
    floor_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    floor = db.query(Floor).filter(
        Floor.id == floor_id
    ).first()

    if not floor:
        raise HTTPException(
            status_code=404,
            detail="Floor not found"
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in [".png", ".jpg", ".jpeg"]:
        raise HTTPException(
            status_code=400,
            detail="Only PNG and JPG files are allowed"
        )

    filename = f"{uuid.uuid4().hex}{extension}"
    file_path = UPLOAD_DIR / filename

    content = await file.read()

    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File is too large (maximum 10 MB)"
        )

    file_path.write_bytes(content)

    floor.plan_image = f"/uploads/{filename}"

    db.commit()
    db.refresh(floor)

    return {
        "message": "Floor plan uploaded",
        "plan_image": floor.plan_image
    }