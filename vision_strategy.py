from typing import Dict


def determine_vision_strategy(
    inspection_description: str,
    defect_description: str | None,
    surface_type: str | None,
) -> Dict:

    inspection = inspection_description.lower()

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

    # ---------------------------------------------------------
    # Surface scratch / defect inspection
    # ---------------------------------------------------------

    scratch_keywords = [
        "scratch",
        "çizik",
        "surface defect",
        "surface anomaly",
        "crack",
        "çatlak",
    ]

    if any(
        keyword in defect
        for keyword in scratch_keywords
    ):

        return {
            "primary_method": "classical_cv",
            "secondary_method": "segmentation",
            "recommended_pipeline": [
                "image_acquisition",
                "grayscale_conversion",
                "illumination_normalization",
                "noise_reduction",
                "contrast_enhancement",
                "defect_segmentation",
                "morphological_filtering",
                "connected_component_analysis",
                "defect_measurement",
                "pass_fail_decision",
            ],
            "ai_required": False,
            "ai_alternative": "anomaly_detection",
            "reason": (
                "Surface scratches can initially be addressed "
                "using controlled illumination and classical "
                "image processing. AI anomaly detection can "
                "be evaluated if defect appearance varies "
                "significantly."
            ),
            "confidence": 0.78,
        }

    # ---------------------------------------------------------
    # Measurement
    # ---------------------------------------------------------

    measurement_keywords = [
        "measurement",
        "dimension",
        "diameter",
        "width",
        "height",
        "ölçüm",
        "çap",
    ]

    if any(
        keyword in inspection
        for keyword in measurement_keywords
    ):

        return {
            "primary_method": "classical_cv",
            "secondary_method": "calibrated_measurement",
            "recommended_pipeline": [
                "image_acquisition",
                "calibration",
                "grayscale_conversion",
                "edge_detection",
                "subpixel_edge_detection",
                "geometric_measurement",
                "tolerance_check",
                "pass_fail_decision",
            ],
            "ai_required": False,
            "ai_alternative": None,
            "reason": (
                "Dimensional inspection is preferably solved "
                "using calibrated classical vision rather than AI."
            ),
            "confidence": 0.90,
        }

    # ---------------------------------------------------------
    # Default
    # ---------------------------------------------------------

    return {
        "primary_method": "ai_vision",
        "secondary_method": "classification",
        "recommended_pipeline": [
            "image_acquisition",
            "preprocessing",
            "ai_inference",
            "postprocessing",
            "pass_fail_decision",
        ],
        "ai_required": True,
        "ai_alternative": None,
        "reason": (
            "The inspection description does not provide "
            "enough information for a specialized classical "
            "vision strategy."
        ),
        "confidence": 0.55,
    }