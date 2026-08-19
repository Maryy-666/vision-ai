from typing import List

from app.models.components import Camera


# ---------------------------------------------------------
# Temporary camera catalog
# ---------------------------------------------------------

CAMERA_CATALOG: List[Camera] = [

    Camera(
        manufacturer="DemoVision",
        model="AV-5000M",
        camera_type="area_scan",
        resolution_width=5472,
        resolution_height=3648,
        pixel_size_um=2.74,
        monochrome=True,
        shutter_type="global",
        interface="GigE",
        max_fps=20,
        sensor_width_mm=14.99,
        sensor_height_mm=9.99,
    ),

    Camera(
        manufacturer="DemoVision",
        model="AV-12000M",
        camera_type="area_scan",
        resolution_width=4096,
        resolution_height=3000,
        pixel_size_um=3.45,
        monochrome=True,
        shutter_type="global",
        interface="USB3",
        max_fps=30,
        sensor_width_mm=14.13,
        sensor_height_mm=10.35,
    ),

    Camera(
        manufacturer="DemoVision",
        model="AV-2000M",
        camera_type="area_scan",
        resolution_width=1920,
        resolution_height=1080,
        pixel_size_um=5.86,
        monochrome=True,
        shutter_type="global",
        interface="GigE",
        max_fps=60,
        sensor_width_mm=11.26,
        sensor_height_mm=6.34,
    ),

    Camera(
        manufacturer="DemoVision",
        model="LS-4096M",
        camera_type="line_scan",
        resolution_width=4096,
        resolution_height=1,
        pixel_size_um=7.0,
        monochrome=True,
        shutter_type=None,
        interface="CoaXPress",
        max_fps=None,
        sensor_width_mm=28.67,
        sensor_height_mm=None,
    ),
]


def determine_camera_architecture(
    motion_type: str | None,
    speed_m_s: float | None,
    inspection_description: str,
) -> dict:
    """
    Determine whether the application is better suited
    for area-scan or line-scan architecture.

    This is an initial engineering rule set.
    """

    description = inspection_description.lower()

    # Continuous web/conveyor applications are candidates
    # for line-scan architecture.
    continuous_keywords = [
        "continuous",
        "web",
        "film",
        "sheet",
        "textile",
        "roll",
        "continuous surface",
    ]

    continuous_application = any(
        keyword in description
        for keyword in continuous_keywords
    )

    if motion_type == "continuous" or continuous_application:

        return {
            "recommended_architecture": "line_scan",
            "reason": (
                "The application appears to involve "
                "continuous material or continuous motion."
            ),
            "confidence": 0.80,
        }

    # Fast conveyor applications may also benefit from
    # line-scan depending on geometry and inspection area.
    if (
        motion_type == "conveyor"
        and speed_m_s is not None
        and speed_m_s >= 1.0
    ):

        return {
            "recommended_architecture": "line_scan",
            "reason": (
                "High conveyor speed may make line-scan "
                "architecture advantageous."
            ),
            "confidence": 0.70,
        }

    # Default for discrete parts.
    return {
        "recommended_architecture": "area_scan",
        "reason": (
            "The application appears suitable for "
            "discrete-part area-scan inspection."
        ),
        "confidence": 0.85,
    }


def select_cameras(
    required_horizontal_pixels: int,
    camera_type: str = "area_scan",
    require_global_shutter: bool = True,
    require_monochrome: bool = True,
) -> List[Camera]:
    """
    Filter camera candidates according to engineering requirements.
    """

    candidates = []

    for camera in CAMERA_CATALOG:

        # Architecture
        if camera.camera_type != camera_type:
            continue

        # Resolution
        if camera.resolution_width < required_horizontal_pixels:
            continue

        # Shutter
        if require_global_shutter:
            if camera.shutter_type != "global":
                continue

        # Monochrome
        if require_monochrome:
            if not camera.monochrome:
                continue

        candidates.append(camera)

    # Rank by the smallest resolution that still satisfies
    # the requirement.
    candidates.sort(
        key=lambda camera: camera.resolution_width
    )

    return candidates


def calculate_required_fps(
    conveyor_speed_m_s: float,
    object_length_mm: float,
    overlap_factor: float = 1.2,
) -> float:
    """
    Estimate the minimum frame rate required for
    area-scan inspection of moving parts.

    FPS ≈ object_speed / object_length × overlap_factor
    """

    if conveyor_speed_m_s <= 0:
        raise ValueError(
            "conveyor_speed_m_s must be greater than 0"
        )

    if object_length_mm <= 0:
        raise ValueError(
            "object_length_mm must be greater than 0"
        )

    object_length_m = object_length_mm / 1000.0

    return (
        conveyor_speed_m_s
        / object_length_m
        * overlap_factor
    )


def rank_cameras(
    cameras: List[Camera],
    required_fps: float | None = None,
) -> List[Camera]:
    """
    Rank cameras according to whether they satisfy
    the required frame rate and resolution.
    """

    def score(camera: Camera) -> tuple:

        fps_ok = True

        if required_fps is not None:
            fps_ok = (
                camera.max_fps is not None
                and camera.max_fps >= required_fps
            )

        # Cameras satisfying FPS requirements come first.
        # Among those, prefer the lowest sufficient resolution.
        return (
            not fps_ok,
            camera.resolution_width,
        )

    return sorted(cameras, key=score)