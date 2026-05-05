# src/schemas/metrics

from pydantic import BaseModel
from typing import List, Optional

class MetricsInput(BaseModel):
    tp: int
    tn: int
    fp: int
    fn: int
    first_relevant_rank: int = 1
    ranks: Optional[List[int]] = None