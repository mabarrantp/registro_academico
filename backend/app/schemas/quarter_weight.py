from pydantic import BaseModel
from typing import Dict


class QuarterWeightsPayload(BaseModel):
    weights: Dict[str, int]