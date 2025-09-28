import json
from pathlib import Path
from typing import Dict, Any
from fastapi import HTTPException

from .models import GameConfig, PlayDeskConfig, AmebaConfig, NeuralNetworkConfig


class ConfigService:
    """Service for handling game configuration operations"""

    def __init__(self, config_file_path: Path):
        self.config_file_path = config_file_path

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from config.json file"""
        try:
            if not self.config_file_path.exists():
                raise FileNotFoundError(
                    f"Config file not found: {self.config_file_path}"
                )

            with open(self.config_file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Configuration file not found")
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=500, detail=f"Invalid JSON in config file: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error loading configuration: {str(e)}"
            )

    def save_config(self, config_data: Dict[str, Any]) -> bool:
        """Save configuration to config.json file"""
        try:
            with open(self.config_file_path, "w", encoding="utf-8") as file:
                json.dump(config_data, file, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error saving configuration: {str(e)}"
            )

    def get_config(self) -> GameConfig:
        """Get current game configuration as Pydantic model"""
        config_data = self.load_config()
        try:
            return GameConfig(**config_data)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Invalid configuration format: {str(e)}"
            )

    def update_config(self, config: GameConfig) -> GameConfig:
        """Update complete game configuration"""
        config_dict = config.model_dump()
        self.save_config(config_dict)
        return config

    def get_config_section(self, section: str) -> Dict[str, Any]:
        """Get specific configuration section"""
        config = self.load_config()
        if section not in config:
            raise HTTPException(
                status_code=404, detail=f"Configuration section '{section}' not found"
            )
        return config[section]

    def update_config_section(
        self, section: str, section_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update specific configuration section"""
        config = self.load_config()

        if section not in config:
            raise HTTPException(
                status_code=404, detail=f"Configuration section '{section}' not found"
            )

        # Validate section data based on section type
        try:
            if section == "play_desk":
                validated_data = PlayDeskConfig(**section_data)
            elif section == "ameba":
                validated_data = AmebaConfig(**section_data)
            elif section == "neural_network":
                validated_data = NeuralNetworkConfig(**section_data)
            else:
                raise HTTPException(
                    status_code=400, detail=f"Unknown configuration section: {section}"
                )

            # Update the specific section
            config[section] = validated_data.model_dump()
            self.save_config(config)
            return config[section]
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid data for section '{section}': {str(e)}",
            )

    def reset_to_defaults(self) -> GameConfig:
        """Reset configuration to default values"""
        default_config = GameConfig(
            play_desk=PlayDeskConfig(),
            ameba=AmebaConfig(),
            neural_network=NeuralNetworkConfig(),
        )

        config_dict = default_config.model_dump()
        self.save_config(config_dict)
        return default_config

    def validate_config_structure(self, config_data: Dict[str, Any]) -> bool:
        """Validate that config has required sections"""
        required_sections = ["play_desk", "ameba", "neural_network"]
        for section in required_sections:
            if section not in config_data:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing required configuration section: {section}",
                )
        return True

    def get_config_info(self) -> Dict[str, Any]:
        """Get configuration file information"""
        return {
            "file_path": str(self.config_file_path),
            "file_exists": self.config_file_path.exists(),
            "file_size": (
                self.config_file_path.stat().st_size
                if self.config_file_path.exists()
                else 0
            ),
            "sections": ["play_desk", "ameba", "neural_network"],
        }
