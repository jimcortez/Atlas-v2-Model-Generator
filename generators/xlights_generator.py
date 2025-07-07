"""
xLights model generator for LED sphere models.
"""

import xml.etree.ElementTree as ET
import csv
from typing import Dict, List
from .base_generator import BaseGenerator
from .xlights_common import XLightsCommon


class XLightsGenerator(BaseGenerator):
    """Generator for xLights model files"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.model_name = config['model']['name']
        self.model_version = config['model']['version']
        
        # Enforce xLights 2D grid size limit of 1000
        self.max_grid_size = 1000
        self.validated_total_size = self._validate_total_size()
    
    def _validate_total_size(self) -> int:
        """
        Validate and enforce the 1000 limit for xLights 2D grid dimensions.
        
        Returns:
            Validated total_size (clamped to 1000 if necessary)
        """
        if self.total_size > self.max_grid_size:
            print(f"Warning: total_size ({self.total_size}) exceeds xLights 2D limit of {self.max_grid_size}. Clamping to {self.max_grid_size}.")
            return self.max_grid_size
        return self.total_size
    
    def get_format_name(self) -> str:
        return "xLights"
    
    def get_file_extension(self) -> str:
        return ".xmodel"
    
    def generate_ring_string_alternative(self, ring_num: int) -> str:
        """
        Alternative ring generation using coordinate-based positioning.
        Creates a more precise distribution based on actual spherical geometry.
        Uses validated total_size to ensure xLights 2D grid limits are respected.
        """
        ring_leds = [pos for pos in self.led_positions if pos.ring_number == ring_num]
        ring_leds.sort(key=lambda pos: pos.position_in_ring)
        
        # Create a sparse array representation using validated size
        result = [""] * self.validated_total_size
        
        if not ring_leds:
            return ",".join(map(str, result))
        
        # Place first and last LEDs
        result[0] = str(ring_leds[0].led_number)
        result[-1] = str(ring_leds[-1].led_number)
        
        # Distribute remaining LEDs based on their angular positions
        if len(ring_leds) > 2:
            for i, led in enumerate(ring_leds[1:-1], 1):
                # Calculate position based on angular distribution
                angle_ratio = i / (len(ring_leds) - 1)
                array_position = int(angle_ratio * (self.validated_total_size - 1))
                result[array_position] = str(led.led_number)
        
        return ",".join(map(str, result))
    
    def generate_sphere_alternative(self) -> List[str]:
        """Generate sphere using the new coordinate-based approach"""
        self.generate_led_positions()
        sphere = []
        
        for ring_num in sorted(self.rings.keys()):
            ring_string = self.generate_ring_string_alternative(ring_num)
            sphere.append(ring_string)
        
        return sphere
    
    def write_xml_model(self, filename: str, sphere: List[str]):
        """
        Write xLights XML model file with enhanced metadata.
        Uses validated total_size for parm1 to ensure xLights compatibility.
        """
        # Create root element with more detailed attributes
        root = ET.Element('custommodel')
        root.set('name', f'{self.model_name} v{self.model_version}')
        root.set('parm1', str(self.validated_total_size))  # Use validated size
        root.set('parm2', str(len(self.rings)))
        root.set('Depth', '1')
        root.set('StringType', 'GRB Nodes')
        root.set('Transparency', '0')
        root.set('PixelSize', '2')
        root.set('ModelBrightness', '0')
        root.set('Antialias', '1')
        root.set('StrandNames', '')
        root.set('NodeNames', '')
        root.set('CustomModel', ";".join(sphere))
        root.set('SourceVersion', '2023.20')
        
        # Add metadata about the generation method
        metadata = ET.SubElement(root, 'metadata')
        metadata.set('generator', 'AtlasV2Generator')
        metadata.set('method', 'coordinate-based')
        metadata.set('total_leds', str(len(self.led_positions)))
        metadata.set('ports', str(self.ports))
        metadata.set('max_grid_size', str(self.max_grid_size))
        metadata.set('original_total_size', str(self.total_size))
        metadata.set('validated_total_size', str(self.validated_total_size))
        
        # Add coordinate information for debugging/visualization
        coords_element = ET.SubElement(root, 'coordinates')
        for led in self.led_positions:
            led_elem = ET.SubElement(coords_element, 'led')
            led_elem.set('number', str(led.led_number))
            led_elem.set('ring', str(led.ring_number))
            led_elem.set('position', str(led.position_in_ring))
            led_elem.set('x', f"{led.x:.2f}")
            led_elem.set('y', f"{led.y:.2f}")
            led_elem.set('z', f"{led.z:.2f}")
        
        # Write XML with pretty formatting
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ")
        
        with open(filename, 'wb') as f:
            tree.write(f, encoding='utf-8', xml_declaration=True)
    
    def write_csv_enhanced(self, filename: str, group_assignment: Dict[int, int]):
        """
        Write enhanced CSV output with additional coordinate information.
        Uses the exact logic from the original Atlas v2 code for group assignment.
        """
        # Define additional headers for 2D version
        additional_headers = ["Avg X", "Avg Y", "Avg Z"]
        
        # Define function to generate additional data (average coordinates)
        def get_additional_data(ring_num: int, led_positions: List) -> List[str]:
            avg_x, avg_y, avg_z = XLightsCommon.get_average_coordinates(ring_num, led_positions)
            return [f"{avg_x:.2f}", f"{avg_y:.2f}", f"{avg_z:.2f}"]
        
        # Use common CSV writing function
        XLightsCommon.write_csv_with_group_assignment(
            filename=filename,
            group_assignment=group_assignment,
            rings=self.rings,
            led_positions=self.led_positions,
            ports=self.ports,
            additional_headers=additional_headers,
            additional_data_func=get_additional_data
        )
    
    def export_coordinates_json(self, filename: str):
        """Export LED coordinates to JSON for external visualization"""
        import json
        
        data = {
            "model_info": {
                "name": self.model_name,
                "version": self.model_version,
                "total_leds": len(self.led_positions),
                "rings": len(self.rings),
                "ports": self.ports,
                "max_grid_size": self.max_grid_size,
                "original_total_size": self.total_size,
                "validated_total_size": self.validated_total_size
            },
            "leds": [
                {
                    "number": led.led_number,
                    "ring": led.ring_number,
                    "position_in_ring": led.position_in_ring,
                    "coordinates": {
                        "x": round(led.x, 2),
                        "y": round(led.y, 2),
                        "z": round(led.z, 2)
                    }
                }
                for led in self.led_positions
            ]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def generate(self, output_path: str) -> bool:
        """
        Generate xLights model files.
        
        Args:
            output_path: Base path for output files (without extension)
            
        Returns:
            True if generation was successful, False otherwise
        """
        try:
            # Generate sphere data
            sphere = self.generate_sphere_alternative()
            group_assignment = self.generate_group_assignment_improved()
            
            # Write xmodel file
            xmodel_path = f"{output_path}.xmodel"
            self.write_xml_model(xmodel_path, sphere)
            
            # Write CSV file
            csv_path = f"{output_path}.csv"
            self.write_csv_enhanced(csv_path, group_assignment)
            
            # Write JSON coordinates file
            json_path = f"{output_path}_coordinates.json"
            self.export_coordinates_json(json_path)
            
            return True
            
        except Exception as e:
            print(f"Error generating xLights model files (.xmodel, .csv, _coordinates.json): {e}")
            return False 