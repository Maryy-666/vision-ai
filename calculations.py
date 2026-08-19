from math import ceil


def calculate_required_resolution(
    minimum_defect_size_mm: float,
    pixels_per_defect: int = 4,
) -> float:
    """
    Calculate the minimum required image resolution.

    Example:
        Defect size = 0.20 mm
        Required representation = 4 pixels

        Resolution = 4 / 0.20
                   = 20 pixels/mm
    """

    if minimum_defect_size_mm <= 0:
        raise ValueError(
            "minimum_defect_size_mm must be greater than 0"
        )

    if pixels_per_defect <= 0:
        raise ValueError(
            "pixels_per_defect must be greater than 0"
        )

    return pixels_per_defect / minimum_defect_size_mm


def calculate_required_pixels(
    fov_mm: float,
    pixels_per_mm: float,
) -> int:
    """
    Calculate the number of sensor pixels required
    to cover a given field of view.
    """

    if fov_mm <= 0:
        raise ValueError("fov_mm must be greater than 0")

    if pixels_per_mm <= 0:
        raise ValueError(
            "pixels_per_mm must be greater than 0"
        )

    return ceil(fov_mm * pixels_per_mm)


def calculate_focal_length(
    working_distance_mm: float,
    sensor_dimension_mm: float,
    field_of_view_mm: float,
) -> float:
    """
    Approximate focal length using the thin-lens
    / similar-triangle relationship.

    f ≈ WD × sensor_dimension / FOV
    """

    if working_distance_mm <= 0:
        raise ValueError(
            "working_distance_mm must be greater than 0"
        )

    if sensor_dimension_mm <= 0:
        raise ValueError(
            "sensor_dimension_mm must be greater than 0"
        )

    if field_of_view_mm <= 0:
        raise ValueError(
            "field_of_view_mm must be greater than 0"
        )

    return (
        working_distance_mm
        * sensor_dimension_mm
        / field_of_view_mm
    )


def calculate_pixel_size_at_object(
    field_of_view_mm: float,
    sensor_pixels: int,
) -> float:
    """
    Calculate object-space pixel size.

    Result:
        mm/pixel
    """

    if field_of_view_mm <= 0:
        raise ValueError(
            "field_of_view_mm must be greater than 0"
        )

    if sensor_pixels <= 0:
        raise ValueError(
            "sensor_pixels must be greater than 0"
        )

    return field_of_view_mm / sensor_pixels