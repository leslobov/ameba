import sys
from fastapi import APIRouter, HTTPException
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from training.models import TrainingRequest, TrainingResponse
from core.out.training_handler import TrainingHandler

router = APIRouter(prefix="/api/training", tags=["training"])

# Initialize training handler
training_handler = TrainingHandler(project_root)


@router.post("/train", response_model=TrainingResponse)
async def train_neural_network(request: TrainingRequest):
    """
    Train the neural network with specified parameters

    - **steps**: Number of training steps (default: 1000)
    - **batch_size**: Batch size for training (default: 32)
    - **mode**: Training mode (default: True)
    """
    try:
        # Use the training handler from core/out
        result = training_handler.train_neural_network(
            steps=request.steps, batch_size=request.batch_size, mode=request.mode
        )

        if result.success:
            return TrainingResponse(
                success=result.success,
                message=result.message,
                steps_completed=result.steps_completed,
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Training failed: {result.error_details}"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")


@router.get("/status")
async def get_training_status():
    """Get the current training status and model information"""
    try:
        # Use the training handler from core/out
        status = training_handler.get_training_status()

        return {
            "model_exists": status.model_exists,
            "model_path": status.model_path,
            "last_modified": status.last_modified,
            "config_exists": status.config_exists,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get training status: {str(e)}"
        )
