from pydantic import BaseModel
from typing import Optional


class TrainingRequest(BaseModel):
    """Request model for training neural network"""

    steps: int = 10000
    batch_size: int = 64
    mode: bool = True


class TrainingResponse(BaseModel):
    """Response model for training requests"""

    success: bool
    message: str
    steps_completed: Optional[int] = None
