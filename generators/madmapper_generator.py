"""
MadMapper model generator for LED sphere models.
"""

import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import math
from typing import Dict, List, Tuple
from .base_generator import BaseGenerator


class MadMapperGenerator(BaseGenerator):
    """Generator for MadMapper fixture files"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.model_name = config['model']['name']
        self.model_version = config['model']['version']
        
        # MadMapper specific configuration
        self.grid_resolution = config.get('madmapper', {}).get('grid_resolution', 100)
        self.dmx_start_channel = config.get('madmapper', {}).get('dmx_start_channel', 1)
    
    def get_format_name(self) -> str:
        return "MadMapper"
    
    def get_file_extension(self) -> str:
        return ".mmfl"
    
    def create_sphere_mapping(self) -> List[List[int]]:
        """
        Create a 2D mapping array for the sphere that MadMapper can understand.
        Uses a proper spherical projection that centers rings and leaves appropriate spacing.
        """
        # Generate LED positions first
        self.generate_led_positions()
        
        # Get the maximum number of LEDs in any ring
        max_leds_in_ring = max(self.rings.values())
        num_rings = len(self.rings)
        
        # Create a 2D mapping array initialized with -1 (no LED)
        # Use a larger grid to allow for proper spacing and centering
        grid_width = max_leds_in_ring * 2  # Double width to allow centering
        mapping = [[-1 for _ in range(grid_width)] for _ in range(num_rings)]
        
        # Sort LEDs by LED number to ensure proper ordering
        sorted_leds = sorted(self.led_positions, key=lambda led: led.led_number)
        
        # Fill the mapping with DMX channel numbers using proper spherical projection
        for led in sorted_leds:
            ring_idx = led.ring_number - 1  # Convert to 0-based index
            leds_in_ring = self.rings[led.ring_number]
            
            # Calculate position within the ring (0 to leds_in_ring - 1)
            pos_in_ring = led.position_in_ring
            
            # Use a simpler linear mapping to ensure first LED starts at beginning
            # This ensures LED #1 is visible at the start of the grid
            if leds_in_ring > 1:
                # Map position to grid coordinates with proper spacing
                grid_x = int((pos_in_ring * (grid_width - 1)) / (leds_in_ring - 1))
            else:
                grid_x = grid_width // 2  # Center single LED
            
            # Ensure the position is within bounds
            grid_x = max(0, min(grid_width - 1, grid_x))
            
            # Calculate DMX channel number (each pixel uses 3 channels: RGB)
            dmx_channel = self.dmx_start_channel + (led.led_number - 1) * 3
            
            # Place LED in grid
            mapping[ring_idx][grid_x] = dmx_channel
        
        return mapping
    
    def create_sphere_fixture(self, mapping: List[List[int]], fixture_name: str) -> ET.Element:
        """
        Create a MadMapper LED fixture element for the sphere.
        
        Args:
            mapping: 2D mapping array of DMX channel numbers
            fixture_name: Name for the fixture
            
        Returns:
            LEDFixture XML element
        """
        height = len(mapping)
        width = len(mapping[0]) if mapping else 0
        
        # Create the LEDFixture element
        fixture = ET.Element("LEDFixture", {
            "product": fixture_name,
            "group": "AtlasV2Sphere",
            "favorite": "0"
        })
        
        # Create the PixelMapping element
        pixel_mapping = ET.SubElement(fixture, "PixelMapping", {
            "width": str(width),
            "height": str(height),
            "type": "RGB",
            "avoidCrossUniversePixels": "0"
        })
        
        # Flatten the mapping array and convert to space-separated string
        # MadMapper expects the mapping as a single string with space-separated values
        flat_mapping = []
        for row in mapping:
            flat_mapping.extend(str(channel) for channel in row)
        
        pixel_mapping.text = " ".join(flat_mapping)
        
        return fixture
    
    def write_madmapper_file(self, filename: str, fixtures: List[ET.Element]):
        """
        Write the MadMapper fixture library file.
        
        Args:
            filename: Output filename
            fixtures: List of LEDFixture elements
        """
        # Create the root LEDFixtureLibrary element
        library = ET.Element("LEDFixtureLibrary")
        
        # Add all fixtures
        for fixture in fixtures:
            library.append(fixture)
        
        # Convert to string and pretty print
        xml_str = ET.tostring(library, encoding="unicode")
        
        # Parse with minidom for pretty printing
        reparsed = minidom.parseString(xml_str)
        pretty_xml = reparsed.toprettyxml(indent="  ")
        
        # Write to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)
    
    def generate(self, output_path: str) -> bool:
        """
        Generate MadMapper fixture files.
        
        Args:
            output_path: Base path for output files (without extension)
            
        Returns:
            True if generation was successful, False otherwise
        """
        try:
            # Create sphere mapping
            mapping = self.create_sphere_mapping()
            
            # Create fixtures for different parts of the sphere
            # We'll create one fixture for the entire sphere
            sphere_fixture = self.create_sphere_fixture(
                mapping, 
                f"{self.model_name}Sphere"
            )
            
            # Write the MadMapper file
            mmfl_path = f"{output_path}.mmfl"
            self.write_madmapper_file(mmfl_path, [sphere_fixture])
            
            return True
            
        except Exception as e:
            print(f"Error generating MadMapper fixture file (.mmfl): {e}")
            return False 