from pydantic import BaseModel

class PipeLengthStats(BaseModel):
    total_length: float
    count_cards: int