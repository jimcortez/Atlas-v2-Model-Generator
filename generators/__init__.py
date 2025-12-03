"""
LED Sphere Model Generators Package

This package contains generators for various LED animation software formats.
"""

from typing import Dict, List, Type
from .base_generator import BaseGenerator
from .xlights_generator import XLightsGenerator
from .madmapper_generator import MadMapperGenerator
from .xlights3d_generator import XLights3DGenerator
from .chromatik_generator import ChromatikGenerator


class GeneratorFactory:
    """Factory class for creating model generators"""
    
    _generators: Dict[str, Type[BaseGenerator]] = {
        'xlights': XLightsGenerator,
        'madmapper': MadMapperGenerator,
        'xlights3d': XLights3DGenerator,
        'chromatik': ChromatikGenerator,
    }
    
    @classmethod
    def get_available_formats(cls) -> List[str]:
        """Get list of available format names"""
        return list(cls._generators.keys())
    
    @classmethod
    def create_generator(cls, format_name: str, config: Dict) -> BaseGenerator:
        """Create a generator instance for the given format"""
        format_name = format_name.lower()
        if format_name not in cls._generators:
            raise ValueError(f"Unknown format: {format_name}")
        return cls._generators[format_name](config)


# Convenience functions for backward compatibility
def get_available_formats() -> List[str]:
    """Get list of available format names"""
    return GeneratorFactory.get_available_formats()


def create_generator(format_name: str, config: Dict) -> BaseGenerator:
    """Create a generator instance for the specified format"""
    return GeneratorFactory.create_generator(format_name, config) 