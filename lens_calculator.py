def calculate_focal_length(
    working_distance_mm: float,
    sensor_width_mm: float,
    field_of_view_width_mm: float,
) -> float:
    """
    Calculate approximate focal length.

    Formula:
        f = WD × sensor_width / FOV

    All dimensions are in millimeters.
    """

    if working_distance_mm <= 0:
        raise ValueError(
            "working_distance_mm must be greater than 0"
        )

    if sensor_width_mm <= 0:
        raise ValueError(
            "sensor_width_mm must be greater than 0"
        )

    if field_of_view_width_mm <= 0:
        raise ValueError(
            "field_of_view_width_mm must be greater than 0"
        )

    focal_length_mm = (
        working_distance_mm
        * sensor_width_mm
        / field_of_view_width_mm
    )

    return focal_length_mm


def calculate_magnification(
    sensor_width_mm: float,
    field_of_view_width_mm: float,
) -> float:
    """
    Calculate approximate optical magnification.

    Magnification = sensor size / object FOV
    """

    if sensor_width_mm <= 0:
        raise ValueError(
            "sensor_width_mm must be greater than 0"
        )

    if field_of_view_width_mm <= 0:
        raise ValueError(
            "field_of_view_width_mm must be greater than 0"
        )

    return sensor_width_mm / field_of_view_width_mm