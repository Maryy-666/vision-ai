from uuid import uuid4
from io import BytesIO

import cv2
import numpy as np

from PIL import Image

from fastapi import (
    APIRouter,
    HTTPException,
    UploadFile,
    File,
)

from pydantic import BaseModel

from app.schemas.inspection import InspectionRequest

from app.services.application_analyzer import (
    analyze_application,
)

from app.services.ai_agent import (
    parse_requirement,
)


router = APIRouter()


# ---------------------------------------------------------
# Temporary in-memory sessions
# ---------------------------------------------------------

SESSIONS: dict[str, dict] = {}


class AgentRequest(BaseModel):
    message: str
    session_id: str | None = None


# ---------------------------------------------------------
# Direct engineering analysis
# ---------------------------------------------------------

@router.post("/analyze")
def analyze(
    request: InspectionRequest,
):

    result = analyze_application(
        request
    )

    return {
        "status": "success",
        "analysis": result,
    }


# ---------------------------------------------------------
# Image analysis
# ---------------------------------------------------------

@router.post("/agent/image")
async def analyze_image(
    file: UploadFile = File(...),
):

    image_bytes = await file.read()

    try:

        # -------------------------------------------------
        # 1. Read image with Pillow
        # -------------------------------------------------

        image = Image.open(
            BytesIO(image_bytes)
        )

        width, height = image.size

        # -------------------------------------------------
        # 2. Decode image with OpenCV
        # -------------------------------------------------

        image_array = np.frombuffer(
            image_bytes,
            dtype=np.uint8,
        )

        cv_image = cv2.imdecode(
            image_array,
            cv2.IMREAD_COLOR,
        )

        if cv_image is None:
            raise ValueError(
                "OpenCV could not decode the image."
            )

        # -------------------------------------------------
        # 3. Convert to grayscale
        # -------------------------------------------------

        gray = cv2.cvtColor(
            cv_image,
            cv2.COLOR_BGR2GRAY,
        )

        # -------------------------------------------------
        # 4. Basic image statistics
        # -------------------------------------------------

        mean_intensity = float(
            np.mean(gray)
        )

        standard_deviation = float(
            np.std(gray)
        )

        # -------------------------------------------------
        # 5. Gaussian blur
        # -------------------------------------------------

        blurred = cv2.GaussianBlur(
            gray,
            (5, 5),
            0,
        )

        # -------------------------------------------------
        # 6. Edge detection
        # -------------------------------------------------

        edges = cv2.Canny(
            blurred,
            50,
            150,
        )

        # -------------------------------------------------
        # 7. Morphological filtering
        # -------------------------------------------------

        kernel = np.ones(
            (3, 3),
            np.uint8,
        )

        morphology = cv2.morphologyEx(
            edges,
            cv2.MORPH_CLOSE,
            kernel,
        )

        # -------------------------------------------------
        # 8. Candidate pixel statistics
        # -------------------------------------------------

        candidate_pixels = int(
            np.count_nonzero(
                morphology
            )
        )

        total_pixels = int(
            morphology.shape[0]
            * morphology.shape[1]
        )

        candidate_ratio = (
            candidate_pixels / total_pixels
            if total_pixels > 0
            else 0
        )

        # -------------------------------------------------
        # 9. Connected Component Analysis
        # -------------------------------------------------

        (
            num_labels,
            labels,
            stats,
            centroids,
        ) = cv2.connectedComponentsWithStats(
            morphology,
            connectivity=8,
        )

        defect_candidates = []

        for label in range(
            1,
            num_labels,
        ):

            x = int(
                stats[
                    label,
                    cv2.CC_STAT_LEFT,
                ]
            )

            y = int(
                stats[
                    label,
                    cv2.CC_STAT_TOP,
                ]
            )

            width_component = int(
                stats[
                    label,
                    cv2.CC_STAT_WIDTH,
                ]
            )

            height_component = int(
                stats[
                    label,
                    cv2.CC_STAT_HEIGHT,
                ]
            )

            area = int(
                stats[
                    label,
                    cv2.CC_STAT_AREA,
                ]
            )

            # ---------------------------------------------
            # Remove very small noise regions
            # ---------------------------------------------

            if area < 10:
                continue

            # ---------------------------------------------
            # Centroid
            # ---------------------------------------------

            centroid_x = float(
                centroids[label][0]
            )

            centroid_y = float(
                centroids[label][1]
            )

            defect_candidates.append(
                {
                    "label": label,
                    "x": x,
                    "y": y,
                    "width": width_component,
                    "height": height_component,
                    "area_pixels": area,
                    "centroid": {
                        "x": round(
                            centroid_x,
                            2,
                        ),
                        "y": round(
                            centroid_y,
                            2,
                        ),
                    },
                }
            )

        # -------------------------------------------------
        # 10. Sort candidates by area
        # -------------------------------------------------

        defect_candidates.sort(
            key=lambda item: item[
                "area_pixels"
            ],
            reverse=True,
        )

        # -------------------------------------------------
        # 11. Limit response to largest candidates
        # -------------------------------------------------

        defect_candidates = (
            defect_candidates[:20]
        )

        # -------------------------------------------------
        # 12. Return image analysis
        # -------------------------------------------------

        return {

            "status": "success",

            "filename": file.filename,

            "content_type": file.content_type,

            "image": {
                "width": width,
                "height": height,
                "mode": image.mode,
                "format": image.format,
            },

            "vision_analysis": {

                "grayscale": True,

                "mean_intensity": round(
                    mean_intensity,
                    2,
                ),

                "standard_deviation": round(
                    standard_deviation,
                    2,
                ),

                "scratch_candidate_detection": {

                    "method": (
                        "canny_edge_morphology"
                    ),

                    "candidate_pixels": (
                        candidate_pixels
                    ),

                    "candidate_ratio": round(
                        candidate_ratio,
                        4,
                    ),

                    "connected_components": {

                        "candidate_count": len(
                            defect_candidates
                        ),

                        "candidates": (
                            defect_candidates
                        ),
                    },
                },
            },

            "message": (
                "Image was successfully "
                "decoded and analyzed."
            ),
        }

    except Exception as exc:

        raise HTTPException(
            status_code=400,
            detail=f"Invalid image: {exc}",
        )


# ---------------------------------------------------------
# AI Agent
# ---------------------------------------------------------

@router.post("/agent")
def run_agent(
    request: AgentRequest,
):

    # -----------------------------------------------------
    # 1. Create or recover session
    # -----------------------------------------------------

    session_id = request.session_id

    if session_id is None:

        session_id = str(
            uuid4()
        )

    session = SESSIONS.get(
        session_id
    )

    # -----------------------------------------------------
    # 2. First message
    # -----------------------------------------------------

    if session is None:

        structured_data = (
            parse_requirement(
                request.message
            )
        )

        session = {
            "structured_request": (
                structured_data
            ),
        }

        SESSIONS[
            session_id
        ] = session

    else:

        # -------------------------------------------------
        # 3. Follow-up message
        # -------------------------------------------------

        structured_data = session[
            "structured_request"
        ]

        message = (
            request.message.strip()
        )

        # ---------------------------------------------
        # required_pixels_per_defect
        # ---------------------------------------------

        if (
            structured_data.get(
                "required_pixels_per_defect"
            )
            is None
        ):

            try:

                pixels_per_defect = float(
                    message
                )

                structured_data[
                    "required_pixels_per_defect"
                ] = pixels_per_defect

            except ValueError:

                return {

                    "status": (
                        "needs_information"
                    ),

                    "session_id": (
                        session_id
                    ),

                    "structured_request": (
                        structured_data
                    ),

                    "missing_information": [

                        {
                            "field": (
                                "required_pixels_per_defect"
                            ),

                            "question": (
                                "Please provide the "
                                "required pixels per "
                                "minimum defect as a "
                                "number. For example: 4"
                            ),

                            "reason": (
                                "This value is required "
                                "to calculate camera "
                                "resolution."
                            ),
                        }

                    ],
                }

        session[
            "structured_request"
        ] = structured_data

        SESSIONS[
            session_id
        ] = session

    # -----------------------------------------------------
    # 4. Check remaining required information
    # -----------------------------------------------------

    missing_information = []

    if (
        structured_data.get(
            "required_pixels_per_defect"
        )
        is None
    ):

        missing_information.append({

            "field": (
                "required_pixels_per_defect"
            ),

            "question": (
                "How many pixels per minimum "
                "defect would you like to use?"
            ),

            "reason": (
                "This value is required to "
                "calculate the required camera "
                "resolution."
            ),
        })

    if (
        structured_data.get(
            "field_of_view_width_mm"
        )
        is None
    ):

        missing_information.append({

            "field": (
                "field_of_view_width_mm"
            ),

            "question": (
                "What is the required field of "
                "view width in mm?"
            ),

            "reason": (
                "This value is required for "
                "camera resolution calculation."
            ),
        })

    if (
        structured_data.get(
            "working_distance_mm"
        )
        is None
    ):

        missing_information.append({

            "field": (
                "working_distance_mm"
            ),

            "question": (
                "What is the approximate camera "
                "working distance in mm?"
            ),

            "reason": (
                "This value is required for "
                "lens selection."
            ),
        })

    # -----------------------------------------------------
    # 5. Ask for missing information
    # -----------------------------------------------------

    if missing_information:

        return {

            "status": (
                "needs_information"
            ),

            "session_id": (
                session_id
            ),

            "structured_request": (
                structured_data
            ),

            "missing_information": (
                missing_information
            ),
        }

    # -----------------------------------------------------
    # 6. Validate structured request
    # -----------------------------------------------------

    try:

        inspection_request = (
            InspectionRequest(
                **structured_data
            )
        )

    except Exception as exc:

        raise HTTPException(
            status_code=422,
            detail=str(exc),
        )

    # -----------------------------------------------------
    # 7. Run engineering engine
    # -----------------------------------------------------

    analysis = (
        analyze_application(
            inspection_request
        )
    )

    # -----------------------------------------------------
    # 8. Final response
    # -----------------------------------------------------

    return {

        "status": "success",

        "session_id": (
            session_id
        ),

        "structured_request": (
            structured_data
        ),

        "analysis": analysis,
    }