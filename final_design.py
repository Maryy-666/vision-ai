def build_final_design(
    camera_architecture: dict,
    primary_camera: dict | None,
    engineering: dict,
    lens_design: dict,
    lighting_design: dict,
    vision_strategy: dict,
    request,
) -> dict:
    """
    Build the final structured engineering recommendation.
    """

    assumptions = []
    validation_items = []

    # ---------------------------------------------------------
    # Assumptions
    # ---------------------------------------------------------

    if request.working_distance_mm is not None:
        assumptions.append({
            "parameter": "working_distance_mm",
            "value": request.working_distance_mm,
            "status": "provided",
        })
    else:
        assumptions.append({
            "parameter": "working_distance_mm",
            "value": None,
            "status": "missing",
            "impact": "Lens selection cannot be finalized.",
        })

    if request.minimum_defect_size_mm is not None:
        assumptions.append({
            "parameter": "minimum_defect_size_mm",
            "value": request.minimum_defect_size_mm,
            "status": "provided",
        })
    else:
        assumptions.append({
            "parameter": "minimum_defect_size_mm",
            "value": None,
            "status": "missing",
            "impact": "Camera resolution cannot be finalized.",
        })

    if request.field_of_view_width_mm is not None:
        assumptions.append({
            "parameter": "field_of_view_width_mm",
            "value": request.field_of_view_width_mm,
            "status": "provided",
        })
    else:
        assumptions.append({
            "parameter": "field_of_view_width_mm",
            "value": None,
            "status": "missing",
            "impact": "Camera and lens sizing are incomplete.",
        })

    if request.object_length_mm is not None:
        assumptions.append({
            "parameter": "object_length_mm",
            "value": request.object_length_mm,
            "status": "provided",
        })

    # ---------------------------------------------------------
    # Validation requirements
    # ---------------------------------------------------------

    validation_items.append(
        "Validate illumination experimentally on the actual surface."
    )

    validation_items.append(
        "Verify final lens FOV and mechanical working distance."
    )

    validation_items.append(
        "Verify exposure time and motion blur at production speed."
    )

    if vision_strategy.get("ai_alternative"):
        validation_items.append(
            "Evaluate AI anomaly detection if classical CV "
            "does not provide sufficient robustness."
        )

    # ---------------------------------------------------------
    # Confidence calculation
    # ---------------------------------------------------------

    confidence_scores = []

    architecture_confidence = camera_architecture.get(
        "confidence"
    )

    if architecture_confidence is not None:
        confidence_scores.append(
            architecture_confidence
        )

    lighting_confidence = (
        lighting_design
        .get("strategy", {})
        .get("confidence")
    )

    if lighting_confidence is not None:
        confidence_scores.append(
            lighting_confidence
        )

    vision_confidence = vision_strategy.get(
        "confidence"
    )

    if vision_confidence is not None:
        confidence_scores.append(
            vision_confidence
        )

    if primary_camera:
        confidence_scores.append(0.85)

    if engineering:
        confidence_scores.append(0.85)

    if confidence_scores:
        overall_confidence = (
            sum(confidence_scores)
            / len(confidence_scores)
        )
    else:
        overall_confidence = 0.0

    # ---------------------------------------------------------
    # Final recommendation
    # ---------------------------------------------------------

    recommendation = {
        "camera_architecture": camera_architecture,
        "primary_camera": primary_camera,
        "lens_design": lens_design,
        "lighting_design": lighting_design,
        "vision_strategy": vision_strategy,
    }

    return {
        "recommendation": recommendation,

        "confidence": {
            "score": round(
                overall_confidence,
                2,
            ),
            "percentage": round(
                overall_confidence * 100
            ),
        },

        "assumptions": assumptions,

        "validation_required": validation_items,
    }