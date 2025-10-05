"""
Configuration handler for API requests - interfaces with core configuration functionality
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

from core.config_classes.game_config import GameConfig


@dataclass
class ConfigResult:
    """Result of configuration operation"""

    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error_details: Optional[str] = None


@dataclass
class ConfigInfo:
    """Information about configuration file"""

    exists: bool
    path: str
    size: Optional[int] = None
    last_modified: Optional[str] = None
    is_valid: bool = True


class ConfigHandler:
    """Handler for configuration operations"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.config_file_path = project_root / "config.json"

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from config.json"""
        if not self.config_file_path.exists():
            raise FileNotFoundError("Configuration file not found")

        try:
            with open(self.config_file_path, "r") as file:
                return json.load(file)
        except Exception as e:
            raise Exception(f"Failed to load configuration: {str(e)}")

    def save_config(self, config_data: Dict[str, Any]) -> None:
        """Save configuration to config.json"""
        try:
            self.config_file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file_path, "w") as file:
                json.dump(config_data, file, indent=2)
        except Exception as e:
            raise Exception(f"Failed to save configuration: {str(e)}")

    def get_config(self) -> ConfigResult:
        """Get the complete game configuration"""
        try:
            config_data = self.load_config()
            # Validate by creating GameConfig instance
            game_config = GameConfig.from_dict(config_data)

            return ConfigResult(
                success=True,
                message="Configuration loaded successfully",
                data=game_config.to_dict(),
            )
        except Exception as e:
            return ConfigResult(
                success=False,
                message="Failed to load configuration",
                error_details=str(e),
            )

    def update_config(self, new_config: GameConfig) -> ConfigResult:
        """Update the complete game configuration"""
        try:
            config_data = new_config.to_dict()
            self.save_config(config_data)

            return ConfigResult(
                success=True,
                message="Configuration updated successfully",
                data=config_data,
            )
        except Exception as e:
            return ConfigResult(
                success=False,
                message="Failed to update configuration",
                error_details=str(e),
            )

    def get_config_section(self, section: str) -> ConfigResult:
        """Get a specific configuration section"""
        try:
            config_data = self.load_config()

            if section not in config_data:
                return ConfigResult(
                    success=False,
                    message=f"Configuration section '{section}' not found",
                    error_details=f"Available sections: {list(config_data.keys())}",
                )

            return ConfigResult(
                success=True,
                message=f"Configuration section '{section}' loaded successfully",
                data=config_data[section],
            )
        except Exception as e:
            return ConfigResult(
                success=False,
                message=f"Failed to load configuration section '{section}'",
                error_details=str(e),
            )

    def update_config_section(
        self, section: str, section_data: Dict[str, Any]
    ) -> ConfigResult:
        """Update a specific configuration section"""
        try:
            # Load current config
            config_data = self.load_config()

            # Update the section
            config_data[section] = section_data

            # Validate the updated config
            game_config = GameConfig.from_dict(config_data)

            # Save if valid
            self.save_config(config_data)

            return ConfigResult(
                success=True,
                message=f"Configuration section '{section}' updated successfully",
                data=section_data,
            )
        except Exception as e:
            return ConfigResult(
                success=False,
                message=f"Failed to update configuration section '{section}'",
                error_details=str(e),
            )

    def reset_to_defaults(self) -> ConfigResult:
        """Reset configuration to default values"""
        try:
            # Create default config
            default_config = GameConfig.create_default()
            config_data = default_config.to_dict()

            # Save default config
            self.save_config(config_data)

            return ConfigResult(
                success=True,
                message="Configuration reset to defaults successfully",
                data=config_data,
            )
        except Exception as e:
            return ConfigResult(
                success=False,
                message="Failed to reset configuration to defaults",
                error_details=str(e),
            )

    def get_config_info(self) -> ConfigInfo:
        """Get information about the configuration file"""
        try:
            exists = self.config_file_path.exists()
            size = None
            last_modified = None
            is_valid = True

            if exists:
                stat = self.config_file_path.stat()
                size = stat.st_size
                last_modified = datetime.fromtimestamp(stat.st_mtime).isoformat()

                # Check if config is valid
                try:
                    config_data = self.load_config()
                    GameConfig.from_dict(config_data)
                except:
                    is_valid = False

            return ConfigInfo(
                exists=exists,
                path=str(self.config_file_path),
                size=size,
                last_modified=last_modified,
                is_valid=is_valid,
            )
        except Exception as e:
            return ConfigInfo(
                exists=False, path=str(self.config_file_path), is_valid=False
            )

    def validate_config(self) -> ConfigResult:
        """Validate current configuration"""
        try:
            config_data = self.load_config()
            game_config = GameConfig.from_dict(config_data)

            return ConfigResult(
                success=True,
                message="Configuration is valid",
                data={
                    "valid": True,
                    "sections": list(config_data.keys()),
                    "validated_at": datetime.now().isoformat(),
                },
            )
        except Exception as e:
            return ConfigResult(
                success=False,
                message="Configuration validation failed",
                data={"valid": False},
                error_details=str(e),
            )
