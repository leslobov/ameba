import sys
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
from typing import Dict, Any

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from .models import (
    ConfigSection,
    ApiResponse,
    ConfigSectionResponse,
)
from core.config_classes.game_config import GameConfig
from core.out.config_handler import ConfigHandler

# Initialize router
router = APIRouter(prefix="/api/config", tags=["Configuration"])

# Initialize config handler
config_handler = ConfigHandler(project_root)


@router.get("", response_model=ApiResponse, summary="Get complete game configuration")
async def get_config():
    """
    Get the complete game configuration from config.json

    Returns:
        Complete game configuration with all sections
    """
    try:
        result = config_handler.get_config()
        if result.success:
            return JSONResponse(
                content={
                    "success": True,
                    "data": result.data,
                    "message": result.message,
                }
            )
        else:
            raise HTTPException(status_code=500, detail=result.error_details)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.put(
    "", response_model=ApiResponse, summary="Update complete game configuration"
)
async def update_config(config: GameConfig):
    """
    Update the complete game configuration

    Args:
        config: Complete game configuration object

    Returns:
        Updated configuration data
    """
    try:
        result = config_handler.update_config(config)
        if result.success:
            return JSONResponse(
                content={
                    "success": True,
                    "message": result.message,
                    "data": result.data,
                }
            )
        else:
            raise HTTPException(status_code=500, detail=result.error_details)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error updating configuration: {str(e)}"
        )


@router.get(
    "/{section}",
    response_model=ConfigSectionResponse,
    summary="Get specific configuration section",
)
async def get_config_section(
    section: ConfigSection, service: ConfigService = Depends(get_config_service)
):
    """
    Get a specific configuration section

    Args:
        section: Section name (play_desk, ameba, or neural_network)

    Returns:
        Configuration data for the specified section
    """
    try:
        section_data = service.get_config_section(section)
        return JSONResponse(
            content={
                "success": True,
                "section": section,
                "data": section_data,
                "message": f"Configuration section '{section}' loaded successfully",
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.put(
    "/{section}",
    response_model=ConfigSectionResponse,
    summary="Update specific configuration section",
)
async def update_config_section(
    section: ConfigSection,
    section_data: Dict[str, Any],
    service: ConfigService = Depends(get_config_service),
):
    """
    Update a specific configuration section

    Args:
        section: Section name (play_desk, ameba, or neural_network)
        section_data: New data for the section

    Returns:
        Updated section data
    """
    try:
        updated_section = service.update_config_section(section, section_data)
        return JSONResponse(
            content={
                "success": True,
                "section": section,
                "message": f"Configuration section '{section}' updated successfully",
                "data": updated_section,
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error updating configuration section: {str(e)}"
        )


@router.post(
    "/reset", response_model=ApiResponse, summary="Reset configuration to defaults"
)
async def reset_config_to_defaults(
    service: ConfigService = Depends(get_config_service),
):
    """
    Reset the complete configuration to default values

    Returns:
        Default configuration data
    """
    try:
        default_config = service.reset_to_defaults()
        return JSONResponse(
            content={
                "success": True,
                "message": "Configuration reset to defaults successfully",
                "data": default_config.model_dump(),
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error resetting configuration: {str(e)}"
        )


@router.get(
    "/info/status",
    response_model=ApiResponse,
    summary="Get configuration file information",
)
async def get_config_info(service: ConfigService = Depends(get_config_service)):
    """
    Get information about the configuration file

    Returns:
        Configuration file status and metadata
    """
    try:
        info = service.get_config_info()
        return JSONResponse(
            content={
                "success": True,
                "message": "Configuration info retrieved successfully",
                "data": info,
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting configuration info: {str(e)}"
        )


@router.get(
    "/validate", response_model=ApiResponse, summary="Validate current configuration"
)
async def validate_config(service: ConfigService = Depends(get_config_service)):
    """
    Validate the current configuration structure

    Returns:
        Validation status and any issues found
    """
    try:
        config_data = service.load_config()
        service.validate_config_structure(config_data)

        # Try to parse as Pydantic model for full validation
        config = GameConfig(**config_data)

        return JSONResponse(
            content={
                "success": True,
                "message": "Configuration is valid",
                "data": {
                    "valid": True,
                    "sections": list(config_data.keys()),
                    "validated_at": "now",
                },
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "Configuration validation failed",
                "data": {"valid": False, "error": str(e)},
            },
        )
