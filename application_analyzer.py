from app.schemas.inspection import InspectionRequest

from app.services.final_design import (
    build_final_design,
)

from app.services.vision_strategy import (
    determine_vision_strategy,
)

from app.services.lighting_selector import (
    determine_lighting_strategy,
    select_lighting_candidates,
)

from app.utils.calculations import (
    calculate_required_resolution,
    calculate_required_pixels,
)

from app.services.camera_selector import (
    determine_camera_architecture,
    select_cameras,
    calculate_required_fps,
    rank_cameras,
)

from app.services.lens_calculator import (
    calculate_focal_length,
    calculate_magnification,
)

from app.services.lens_selector import (
    select_lenses,
    calculate_fov_for_lens,
)


def analyze_application(request: InspectionRequest) -> dict:
    """
    Analyze an industrial machine vision inspection
    and generate initial engineering requirements.
    """

    engineering = {}
    camera_candidates = []

    # ---------------------------------------------------------
    # 1. Motion information
    # ---------------------------------------------------------

    motion_type = None
    speed_m_s = None

    if request.motion:
        motion_type = request.motion.motion_type
        speed_m_s = request.motion.speed_m_s

    # ---------------------------------------------------------
    # 2. Camera architecture
    # ---------------------------------------------------------

    camera_architecture = determine_camera_architecture(
        motion_type=motion_type,
        speed_m_s=speed_m_s,
        inspection_description=request.inspection_description,
    )

    recommended_camera_type = (
        camera_architecture["recommended_architecture"]
    )

    # ---------------------------------------------------------
    # 3. Required FPS
    # ---------------------------------------------------------

    required_fps = None

    if (
        speed_m_s is not None
        and request.object_length_mm is not None
    ):
        required_fps = calculate_required_fps(
            conveyor_speed_m_s=speed_m_s,
            object_length_mm=request.object_length_mm,
        )

        engineering["required_fps"] = required_fps

    # ---------------------------------------------------------
    # 4. Required image resolution
    # ---------------------------------------------------------

    required_pixels = None

    if (
        request.minimum_defect_size_mm is not None
        and request.required_pixels_per_defect is not None
    ):
        pixels_per_mm = calculate_required_resolution(
            request.minimum_defect_size_mm,
            request.required_pixels_per_defect,
        )

        engineering["required_pixels_per_mm"] = pixels_per_mm

        if request.field_of_view_width_mm is not None:

            required_pixels = calculate_required_pixels(
                request.field_of_view_width_mm,
                pixels_per_mm,
            )

            engineering["required_horizontal_pixels"] = (
                required_pixels
            )

    # ---------------------------------------------------------
    # 5. Camera selection
    # ---------------------------------------------------------

    if required_pixels is not None:

        camera_candidates = select_cameras(
            required_horizontal_pixels=required_pixels,
            camera_type=recommended_camera_type,
            require_global_shutter=True,
            require_monochrome=True,
        )

        camera_candidates = rank_cameras(
            camera_candidates,
            required_fps=required_fps,
        )

    # ---------------------------------------------------------
    # 6. Primary camera
    # ---------------------------------------------------------

    primary_camera = None

    if camera_candidates:
        primary_camera = camera_candidates[0]

    # ---------------------------------------------------------
    # 7. Optical calculation
    # ---------------------------------------------------------

    lens_design = {
        "status": "not_calculated",
        "reason": "Insufficient optical information.",
    }
    # ---------------------------------------------------------
    # 8. Lighting design
    # ---------------------------------------------------------

    geometry = None

    if request.dimensions:
        geometry = "unknown"

    lighting_strategy = determine_lighting_strategy(
        defect_description=request.defect_description,
        surface_type=request.surface_type,
        material=request.material,
        geometry=geometry,
    )

    lighting_candidates = select_lighting_candidates(
        recommended_type=lighting_strategy["recommended_type"],
        working_distance_mm=request.working_distance_mm,
    )

    lighting_design = {
        "strategy": lighting_strategy,
        "candidates": [
            lighting.model_dump()
            for lighting in lighting_candidates
        ],
    }

        # ---------------------------------------------------------
    # 9. Vision / AI strategy
    # ---------------------------------------------------------

    vision_strategy = determine_vision_strategy(
        inspection_description=request.inspection_description,
        defect_description=request.defect_description,
        surface_type=request.surface_type,
    )

        # ---------------------------------------------------------
    # 10. Final engineering design
    # ---------------------------------------------------------

    final_design = build_final_design(
    camera_architecture=camera_architecture,
    primary_camera=(
        primary_camera.model_dump()
        if primary_camera
        else None
    ),
    engineering=engineering,
    lens_design=engineering.get(
        "lens",
        lens_design,
    ),
    lighting_design=lighting_design,
    vision_strategy=vision_strategy,
    request=request,
)
    lens_candidates = []

    if (
        primary_camera is not None
        and request.field_of_view_width_mm is not None
        and request.working_distance_mm is not None
        and primary_camera.sensor_width_mm is not None
    ):

        # -----------------------------------------------------
        # 7A. Calculate focal length
        # -----------------------------------------------------

        focal_length = calculate_focal_length(
            working_distance_mm=request.working_distance_mm,
            sensor_width_mm=primary_camera.sensor_width_mm,
            field_of_view_width_mm=(
                request.field_of_view_width_mm
            ),
        )

        # -----------------------------------------------------
        # 7B. Calculate magnification
        # -----------------------------------------------------

        magnification = calculate_magnification(
            sensor_width_mm=primary_camera.sensor_width_mm,
            field_of_view_width_mm=(
                request.field_of_view_width_mm
            ),
        )

        # -----------------------------------------------------
        # 7C. Find suitable lens candidates
        # -----------------------------------------------------

        lens_candidates = select_lenses(
            required_focal_length_mm=focal_length,
            sensor_width_mm=primary_camera.sensor_width_mm,
        )

        # -----------------------------------------------------
        # 7D. Calculate actual FOV for each candidate
        # -----------------------------------------------------

        lens_results = []

        for lens in lens_candidates:

            actual_fov = calculate_fov_for_lens(
                focal_length_mm=lens.focal_length_mm,
                working_distance_mm=(
                    request.working_distance_mm
                ),
                sensor_width_mm=(
                    primary_camera.sensor_width_mm
                ),
            )

            fov_error_percent = (
                abs(
                    actual_fov
                    - request.field_of_view_width_mm
                )
                / request.field_of_view_width_mm
                * 100
            )

            lens_results.append(
                {
                    **lens.model_dump(),
                    "calculated_fov_mm": round(
                        actual_fov,
                        2,
                    ),
                    "fov_error_percent": round(
                        fov_error_percent,
                        2,
                    ),
                }
            )

        # -----------------------------------------------------
        # 7E. Lens design result
        # -----------------------------------------------------

        lens_design = {
            "status": "calculated",
            "required_focal_length_mm": round(
                focal_length,
                2,
            ),
            "magnification": round(
                magnification,
                5,
            ),
            "working_distance_mm": (
                request.working_distance_mm
            ),
            "sensor_width_mm": (
                primary_camera.sensor_width_mm
            ),
            "target_fov_width_mm": (
                request.field_of_view_width_mm
            ),
            "lens_candidates": lens_results,
        }

        engineering["lens"] = lens_design

    # ---------------------------------------------------------
    # 9. Final structured analysis
    # ---------------------------------------------------------

    return {
        "part": {
            "description": request.part_description,
            "material": request.material,
            "surface_type": request.surface_type,
            "dimensions": (
                request.dimensions.model_dump()
                if request.dimensions
                else None
            ),
        },

        "inspection": {
            "description": request.inspection_description,
            "defect": request.defect_description,
            "roi": request.roi_description,
            "minimum_defect_size_mm": (
                request.minimum_defect_size_mm
            ),
        },

        "motion": (
            request.motion.model_dump()
            if request.motion
            else None
        ),

        "camera_architecture": camera_architecture,

        "primary_camera": (
            primary_camera.model_dump()
            if primary_camera
            else None
        ),

        "engineering": engineering,

        "lens_design": lens_design,
        "lighting_design": lighting_design,

        "vision_strategy": vision_strategy,

        "final_design": final_design,

        "camera_candidates": [
            camera.model_dump()
            for camera in camera_candidates
        ],
    }