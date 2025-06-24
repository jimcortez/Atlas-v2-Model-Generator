"""
xLights model generator for LED sphere models.
"""

import xml.etree.ElementTree as ET
import csv
from typing import Dict, List
from .base_generator import BaseGenerator


class XLightsGenerator(BaseGenerator):
    """Generator for xLights model files"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.model_name = config['model']['name']
        self.model_version = config['model']['version']
    
    def get_format_name(self) -> str:
        return "xLights"
    
    def get_file_extension(self) -> str:
        return ".xmodel"
    
    def generate_ring_string_alternative(self, ring_num: int) -> str:
        """
        Alternative ring generation using coordinate-based positioning.
        Creates a more precise distribution based on actual spherical geometry.
        """
        ring_leds = [pos for pos in self.led_positions if pos.ring_number == ring_num]
        ring_leds.sort(key=lambda pos: pos.position_in_ring)
        
        # Create a sparse array representation
        result = [""] * self.total_size
        
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
                array_position = int(angle_ratio * (self.total_size - 1))
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
        """
        # Create root element with more detailed attributes
        root = ET.Element('custommodel')
        root.set('name', f'{self.model_name} v{self.model_version}')
        root.set('parm1', str(self.total_size))
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
        """
        headers = [
            "Ring", "LED Start", "LED End", "LEDs Per Ring",
            "DataChannel", "DC Start", "DC End", "DC Total", 
            "PC Start", "PC End", "Avg X", "Avg Y", "Avg Z"
        ]
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            
            led_start = 1
            current_group = 1
            group_start = True
            group_led_total = 0
            dc_end_total = 0
            
            for ring_num in sorted(self.rings.keys()):
                leds_in_ring = self.rings[ring_num]
                led_end = led_start + leds_in_ring - 1
                
                # Calculate average coordinates for this ring
                ring_leds = [pos for pos in self.led_positions if pos.ring_number == ring_num]
                avg_x = sum(led.x for led in ring_leds) / len(ring_leds) if ring_leds else 0
                avg_y = sum(led.y for led in ring_leds) / len(ring_leds) if ring_leds else 0
                avg_z = sum(led.z for led in ring_leds) / len(ring_leds) if ring_leds else 0
                
                dc = ""
                dc_start = ""
                pc_end = ""
                dc_total = ""
                dc_end = ""
                group_led_total += leds_in_ring
                
                # Start of a new group
                if group_assignment[ring_num] == current_group and group_start:
                    dc = current_group
                    dc_start = led_start
                    group_start = False
                
                # End of the current group
                elif group_assignment.get(ring_num + 1, self.ports + 1) != current_group:
                    pc_end = current_group
                    dc_end = led_start + leds_in_ring - 1
                    dc_total = group_led_total
                    dc_end_total += group_led_total
                    dc_end = dc_end_total
                    group_start = True
                    current_group += 1
                    group_led_total = 0
                
                writer.writerow([
                    ring_num, led_start, led_end, leds_in_ring,
                    dc, dc_start, dc_end, dc_total, dc, pc_end,
                    f"{avg_x:.2f}", f"{avg_y:.2f}", f"{avg_z:.2f}"
                ])
                
                led_start = led_end + 1
    
    def export_coordinates_json(self, filename: str):
        """Export LED coordinates to JSON for external visualization"""
        import json
        
        data = {
            "model_info": {
                "name": self.model_name,
                "version": self.model_version,
                "total_leds": len(self.led_positions),
                "rings": len(self.rings),
                "ports": self.ports
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