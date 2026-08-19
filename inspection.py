from typing import Optional

from pydantic import BaseModel, Field


class PartDimensions(BaseModel):
    width_mm: Optional[float] = None
    height_mm: Optional[float] = None
    depth_mm: Optional[float] = None


class MotionInfo(BaseModel):
    motion_type: Optional[str] = None
    speed_m_s: Optional[float] = None
    direction: Optional[str] = None


class InspectionRequest(BaseModel):
    part_description: str = Field(
        ...,
        description="Description of the part being inspected",
    )

    inspection_description: str = Field(
        ...,
        description="Description of the quality inspection task",
    )

    defect_description: Optional[str] = None

    dimensions: Optional[PartDimensions] = None

    surface_type: Optional[str] = None

    material: Optional[str] = None

    motion: Optional[MotionInfo] = None

    roi_description: Optional[str] = None

    minimum_defect_size_mm: Optional[float] = None

    field_of_view_width_mm: Optional[float] = None

    required_pixels_per_defect: Optional[int] = 4

    object_length_mm: Optional[float] = None

    working_distance_mm: Optional[float] = None