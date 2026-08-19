from typing import List

from pydantic import BaseModel


class Lens(BaseModel):
    manufacturer: str
    model: str

    focal_length_mm: float

    format_type: str

    max_sensor_size_mm: float

    notes: str | None = None


# ---------------------------------------------------------
# Temporary lens catalog
# ---------------------------------------------------------
# Bu katalog şu anda MVP/demo amaçlıdır.
# Daha sonra gerçek üretici katalog/API verileri ile
# değiştirilecektir.
# ---------------------------------------------------------

LENS_CATALOG: List[Lens] = [

    Lens(
        manufacturer="DemoOptics",
        model="FA-16",
        focal_length_mm=16,
        format_type="1.1 inch",
        max_sensor_size_mm=17.6,
        notes="Wide-angle lens candidate.",
    ),

    Lens(
        manufacturer="DemoOptics",
        model="FA-20",
        focal_length_mm=20,
        format_type="1.1 inch",
        max_sensor_size_mm=17.6,
        notes="Standard focal-length candidate.",
    ),

    Lens(
        manufacturer="DemoOptics",
        model="FA-25",
        focal_length_mm=25,
        format_type="1.1 inch",
        max_sensor_size_mm=17.6,
        notes="Moderate telephoto candidate.",
    ),

    Lens(
        manufacturer="DemoOptics",
        model="FA-35",
        focal_length_mm=35,
        format_type="1.1 inch",
        max_sensor_size_mm=17.6,
        notes="Longer focal-length candidate.",
    ),

    Lens(
        manufacturer="DemoOptics",
        model="FA-50",
        focal_length_mm=50,
        format_type="1.1 inch",
        max_sensor_size_mm=17.6,
        notes="Long focal-length candidate.",
    ),
]


def select_lenses(
    required_focal_length_mm: float,
    sensor_width_mm: float,
    tolerance_ratio: float = 0.30,
) -> List[Lens]:
    """
    Select and rank lenses according to the calculated
    focal length and camera sensor size.

    Example:

        Required focal length = 21.2 mm

        Candidate lenses:
            20 mm
            25 mm
            35 mm

        The closest suitable lens is ranked first.
    """

    if required_focal_length_mm <= 0:
        raise ValueError(
            "required_focal_length_mm must be greater than 0"
        )

    if sensor_width_mm <= 0:
        raise ValueError(
            "sensor_width_mm must be greater than 0"
        )

    if tolerance_ratio <= 0:
        raise ValueError(
            "tolerance_ratio must be greater than 0"
        )

    candidates = []

    for lens in LENS_CATALOG:

        # -------------------------------------------------
        # Sensor compatibility
        # -------------------------------------------------

        if lens.max_sensor_size_mm < sensor_width_mm:
            continue

        # -------------------------------------------------
        # Focal length difference
        # -------------------------------------------------

        difference = abs(
            lens.focal_length_mm
            - required_focal_length_mm
        )

        relative_difference = (
            difference
            / required_focal_length_mm
        )

        # -------------------------------------------------
        # Keep reasonable candidates
        # -------------------------------------------------

        if relative_difference <= tolerance_ratio:

            candidates.append(
                (
                    lens,
                    relative_difference,
                )
            )

    # -----------------------------------------------------
    # Rank by focal-length difference
    # -----------------------------------------------------

    candidates.sort(
        key=lambda item: item[1]
    )

    return [
        lens
        for lens, _ in candidates
    ]


def calculate_fov_for_lens(
    focal_length_mm: float,
    working_distance_mm: float,
    sensor_width_mm: float,
) -> float:
    """
    Estimate the actual horizontal FOV produced by a lens.

    FOV ≈ WD × sensor_width / focal_length
    """

    if focal_length_mm <= 0:
        raise ValueError(
            "focal_length_mm must be greater than 0"
        )

    if working_distance_mm <= 0:
        raise ValueError(
            "working_distance_mm must be greater than 0"
        )

    if sensor_width_mm <= 0:
        raise ValueError(
            "sensor_width_mm must be greater than 0"
        )

    return (
        working_distance_mm
        * sensor_width_mm
        / focal_length_mm
    )