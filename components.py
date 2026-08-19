from typing import Optional

from pydantic import BaseModel


class Camera(BaseModel):
    manufacturer: str
    model: str

    camera_type: str  # area_scan / line_scan

    resolution_width: int
    resolution_height: int

    pixel_size_um: Optional[float] = None

    monochrome: bool = True

    shutter_type: Optional[str] = None

    interface: Optional[str] = None

    max_fps: Optional[float] = None

    sensor_width_mm: Optional[float] = None
    sensor_height_mm: Optional[float] = None

    notes: Optional[str] = None