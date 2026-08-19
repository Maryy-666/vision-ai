from typing import List

from pydantic import BaseModel


class Lighting(BaseModel):
    manufacturer: str
    model: str

    lighting_type: str

    working_distance_mm: float | None = None

    recommended_angle_deg: float | None = None

    wavelength_nm: int | None = None

    size_mm: float | None = None

    notes: str | None = None


# ---------------------------------------------------------
# Temporary lighting catalog
# ---------------------------------------------------------

LIGHTING_CATALOG: List[Lighting] = [

    Lighting(
        manufacturer="DemoLight",
        model="DF-BAR-100",
        lighting_type="dark_field_bar",
        working_distance_mm=100,
        recommended_angle_deg=30,
        wavelength_nm=630,
        size_mm=100,
        notes="Low-angle illumination for scratches and edges.",
    ),

    Lighting(
        manufacturer="DemoLight",
        model="DF-BAR-300",
        lighting_type="dark_field_bar",
        working_distance_mm=300,
        recommended_angle_deg=30,
        wavelength_nm=630,
        size_mm=300,
        notes="Large dark-field bar for long working-distance surface inspection.",
    ),

    Lighting(
        manufacturer="DemoLight",
        model="DOME-150",
        lighting_type="dome",
        working_distance_mm=150,
        recommended_angle_deg=90,
        wavelength_nm=550,
        size_mm=150,
        notes="Diffuse illumination for reflective and curved surfaces.",
    ),

    Lighting(
        manufacturer="DemoLight",
        model="RING-100",
        lighting_type="ring",
        working_distance_mm=100,
        recommended_angle_deg=45,
        wavelength_nm=630,
        size_mm=100,
        notes="General-purpose ring illumination.",
    ),

    Lighting(
        manufacturer="DemoLight",
        model="COAX-100",
        lighting_type="coaxial",
        working_distance_mm=50,
        recommended_angle_deg=0,
        wavelength_nm=550,
        size_mm=100,
        notes="Coaxial illumination for flat reflective surfaces.",
    ),

    Lighting(
        manufacturer="DemoLight",
        model="BACKLIGHT-150",
        lighting_type="backlight",
        working_distance_mm=150,
        recommended_angle_deg=0,
        wavelength_nm=630,
        size_mm=150,
        notes="Backlight for silhouette and dimensional inspection.",
    ),

    Lighting(
        manufacturer="DemoLight",
        model="BAR-DIFFUSE-200",
        lighting_type="diffuse_bar",
        working_distance_mm=200,
        recommended_angle_deg=45,
        wavelength_nm=550,
        size_mm=200,
        notes="Diffuse bar illumination for larger inspection areas.",
    ),
]


def determine_lighting_strategy(
    defect_description: str | None,
    surface_type: str | None,
    material: str | None,
    geometry: str | None = None,
) -> dict:
    """
    Determine the most suitable illumination strategy.
    """

    defect = (
        defect_description.lower()
        if defect_description
        else ""
    )

    surface = (
        surface_type.lower()
        if surface_type
        else ""
    )

    material_name = (
        material.lower()
        if material
        else ""
    )

    geometry_name = (
        geometry.lower()
        if geometry
        else ""
    )

    # ---------------------------------------------------------
    # Scratch / edge inspection
    # ---------------------------------------------------------

    scratch_keywords = [
        "scratch",
        "çizik",
        "edge",
        "kenar",
        "crack",
        "çatlak",
    ]

    if any(
        keyword in defect
        for keyword in scratch_keywords
    ):

        if (
            "reflective" in surface
            or "metal" in material_name
            or "steel" in material_name
        ):

            return {
                "recommended_type": "dark_field_bar",
                "reason": (
                    "Low-angle dark-field illumination is "
                    "recommended to enhance scratches, "
                    "edges and surface discontinuities "
                    "on reflective materials."
                ),
                "recommended_angle_deg": 30,
                "confidence": 0.90,
            }

        return {
            "recommended_type": "dark_field_bar",
            "reason": (
                "Dark-field illumination is suitable "
                "for emphasizing scratches and edges."
            ),
            "recommended_angle_deg": 30,
            "confidence": 0.82,
        }

    # ---------------------------------------------------------
    # Dimensional / silhouette inspection
    # ---------------------------------------------------------

    dimensional_keywords = [
        "dimension",
        "dimensional",
        "measurement",
        "diameter",
        "height",
        "width",
        "silhouette",
        "ölçüm",
        "çap",
        "boy",
        "genişlik",
    ]

    if any(
        keyword in defect
        for keyword in dimensional_keywords
    ):

        return {
            "recommended_type": "backlight",
            "reason": (
                "Backlight is recommended for silhouette "
                "and dimensional measurements."
            ),
            "recommended_angle_deg": 0,
            "confidence": 0.92,
        }

    # ---------------------------------------------------------
    # Reflective surface
    # ---------------------------------------------------------

    if "reflective" in surface:

        if (
            "cylindrical" in geometry_name
            or "curved" in geometry_name
            or "cylinder" in geometry_name
        ):

            return {
                "recommended_type": "dome",
                "reason": (
                    "A dome light is recommended to provide "
                    "more uniform diffuse illumination over "
                    "a curved reflective surface."
                ),
                "recommended_angle_deg": 90,
                "confidence": 0.78,
            }

        return {
            "recommended_type": "coaxial",
            "reason": (
                "Coaxial illumination is a strong candidate "
                "for flat reflective surfaces."
            ),
            "recommended_angle_deg": 0,
            "confidence": 0.75,
        }

    # ---------------------------------------------------------
    # Matte surface
    # ---------------------------------------------------------

    if "matte" in surface:

        return {
            "recommended_type": "ring",
            "reason": (
                "Ring illumination provides general-purpose "
                "uniform illumination for matte surfaces."
            ),
            "recommended_angle_deg": 45,
            "confidence": 0.72,
        }

    # ---------------------------------------------------------
    # Default strategy
    # ---------------------------------------------------------

    return {
        "recommended_type": "ring",
        "reason": (
            "Ring illumination is selected as a general-purpose "
            "starting point because insufficient surface "
            "information is available."
        ),
        "recommended_angle_deg": 45,
        "confidence": 0.55,
    }


def select_lighting_candidates(
    recommended_type: str,
    working_distance_mm: float | None = None,
) -> List[Lighting]:
    """
    Filter lighting candidates based on the recommended
    illumination strategy and approximate working distance.
    """

    candidates = []

    for lighting in LIGHTING_CATALOG:

        if lighting.lighting_type != recommended_type:
            continue

        if (
            working_distance_mm is not None
            and lighting.working_distance_mm is not None
        ):

            distance_error = abs(
                lighting.working_distance_mm
                - working_distance_mm
            )

            if distance_error > 150:
                continue

        candidates.append(lighting)

    return candidates