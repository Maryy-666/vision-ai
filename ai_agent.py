import json
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


SYSTEM_PROMPT = """
You are an industrial machine vision engineering assistant.

Your job is to convert a user's natural-language inspection
requirement into structured engineering information.

You must NOT invent missing engineering measurements.

Extract only information that is explicitly provided.

Return valid JSON with these fields:

{
    "part_description": string,
    "inspection_description": string,
    "defect_description": string | null,
    "surface_type": string | null,
    "material": string | null,
    "roi_description": string | null,
    "minimum_defect_size_mm": number | null,
    "field_of_view_width_mm": number | null,
    "required_pixels_per_defect": number | null,
    "object_length_mm": number | null,
    "working_distance_mm": number | null,
    "motion": {
        "motion_type": string | null,
        "speed_m_s": number | null,
        "direction": string | null
    }
}

If information is missing, return null.

Do not guess.
"""


def parse_requirement(user_text: str) -> dict:
    """
    Convert natural-language inspection requirements
    into structured JSON.
    """

    response = client.responses.create(
        model="gpt-5.5",
        instructions=SYSTEM_PROMPT,
        input=user_text,
    )

    text = response.output_text

    return json.loads(text)