"""
xLights model generator for LED sphere models.
"""

import xml.etree.ElementTree as ET
import csv
import math
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
        
        # Calculate aspect ratio for height determination
        self.aspect_ratio = self._calculate_aspect_ratio()
        self.calculated_height = self._calculate_height()
    
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
    
    def _calculate_aspect_ratio(self) -> float:
        """
        Calculate aspect ratio: number of rings / number of LEDs at widest point.
        
        Returns:
            Aspect ratio as a float
        """
        num_rings = len(self.rings)
        max_leds_in_ring = max(self.rings.values())
        aspect_ratio = num_rings / max_leds_in_ring
        print(f"Aspect ratio calculation: {num_rings} rings / {max_leds_in_ring} LEDs = {aspect_ratio:.3f}")
        return aspect_ratio
    
    def _calculate_height(self) -> int:
        """
        Calculate grid height using aspect ratio.
        
        Returns:
            Calculated height (clamped to max_grid_size if necessary)
        """
        calculated_height = int(round(self.validated_total_size * self.aspect_ratio))
        
        # Ensure height doesn't exceed the grid size limit
        if calculated_height > self.max_grid_size:
            print(f"Warning: calculated height ({calculated_height}) exceeds xLights 2D limit of {self.max_grid_size}. Clamping to {self.max_grid_size}.")
            calculated_height = self.max_grid_size
        
        print(f"Grid dimensions: {self.validated_total_size} x {calculated_height} (width x height)")
        return calculated_height
    
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
    
    def generate_sphere_with_aspect_ratio(self) -> List[str]:
        """
        Generate sphere using aspect ratio-based height calculation.
        Creates a grid where only ring positions are used, with empty space in between.
        """
        self.generate_led_positions()
        sphere = []
        
        # Create empty strings for the calculated height
        for row in range(self.calculated_height):
            # Create an empty row
            empty_row = [""] * self.validated_total_size
            sphere.append(",".join(map(str, empty_row)))
        
        # Calculate ring positions within the grid
        ring_positions = self._calculate_ring_positions()
        
        # Place ring data at calculated positions
        for ring_num in sorted(self.rings.keys()):
            if ring_num in ring_positions:
                row_index = ring_positions[ring_num]
                ring_string = self.generate_ring_string_alternative(ring_num)
                sphere[row_index] = ring_string
        
        return sphere
    
    def _calculate_ring_positions(self) -> Dict[int, int]:
        """
        Calculate the grid row positions for each ring.
        Distributes rings evenly across the calculated height.
        
        Returns:
            Dictionary mapping ring number to grid row index
        """
        num_rings = len(self.rings)
        ring_positions = {}
        
        # Distribute rings evenly across the available height
        for i, ring_num in enumerate(sorted(self.rings.keys())):
            # Calculate position as a ratio of the total height
            position_ratio = i / (num_rings - 1) if num_rings > 1 else 0.5
            row_index = int(round(position_ratio * (self.calculated_height - 1)))
            
            # Ensure the position is within bounds
            row_index = max(0, min(self.calculated_height - 1, row_index))
            ring_positions[ring_num] = row_index
        
        return ring_positions
    
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
        Write xLights XML model file following the official format specification.
        Includes proper string configuration with individual start channels for each port.
        """
        # Create root element with required attributes
        root = ET.Element('custommodel')
        root.set('name', f'{self.model_name} v{self.model_version}')
        root.set('parm1', str(self.validated_total_size))  # Width (validated size)
        root.set('parm2', str(self.calculated_height))     # Height (calculated from aspect ratio)
        root.set('Depth', '1')
        root.set('DisplayAs', 'Custom')
        root.set('StringType', 'RGB Nodes')
        root.set('PixelSize', '2')
        root.set('Transparency', '0')
        root.set('ModelBrightness', '0')
        root.set('Antialias', '1')
        
        # String configuration - number of strings equals number of ports
        root.set('CustomStrings', str(self.ports))
        
        # Calculate and set individual string start channels
        # Each string starts at a different channel based on the group assignment
        group_assignment = self.generate_group_assignment_improved()
        string_start_channels = self._calculate_string_start_channels(group_assignment)
        
        # Set individual string start channels
        for string_num in range(1, self.ports + 1):
            root.set(f'String{string_num}', str(string_start_channels[string_num]))
        
        # Set the custom model data
        root.set('CustomModel', ";".join(sphere))
        
        # Generate compressed format for better performance
        compressed_data = self._generate_compressed_format(sphere)
        root.set('CustomModelCompressed', compressed_data)
        
        # Set source version
        root.set('SourceVersion', '2024.1')
        
        # Write XML with pretty formatting
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ")
        
        with open(filename, 'wb') as f:
            tree.write(f, encoding='utf-8', xml_declaration=True)
    
    def _calculate_string_start_channels(self, group_assignment: Dict[int, int]) -> Dict[int, int]:
        """
        Calculate the starting LED pixel number for each string/port based on group assignment.
        In xLights, channels refer to pixels (LEDs), not individual RGB color channels.
        
        Args:
            group_assignment: Dictionary mapping ring number to group/port number
            
        Returns:
            Dictionary mapping string number to starting LED pixel number
        """
        # Count LEDs per group/port
        leds_per_group = {}
        for ring_num, group_num in group_assignment.items():
            if group_num not in leds_per_group:
                leds_per_group[group_num] = 0
            leds_per_group[group_num] += self.rings[ring_num]
        
        # Calculate starting LED pixel numbers
        string_start_channels = {}
        current_led = 1
        
        for group_num in sorted(leds_per_group.keys()):
            string_start_channels[group_num] = current_led
            # Each LED is one pixel, so just add the count
            current_led += leds_per_group[group_num]
        
        return string_start_channels
    
    def _generate_compressed_format(self, sphere: List[str]) -> str:
        """
        Generate the compressed format for better performance.
        Format: "node,row,col,layer;node,row,col,layer"
        
        Args:
            sphere: List of strings representing the grid rows
            
        Returns:
            Compressed format string
        """
        compressed_nodes = []
        
        for row_idx, row_string in enumerate(sphere):
            if not row_string.strip():
                continue
                
            # Split the row by commas and process each position
            positions = row_string.split(',')
            for col_idx, node_value in enumerate(positions):
                node_value = node_value.strip()
                if node_value and node_value != "" and node_value != "0":
                    try:
                        node_number = int(node_value)
                        if node_number > 0:
                            # Format: node,row,col,layer (0-based indices)
                            compressed_nodes.append(f"{node_number},{row_idx},{col_idx},0")
                    except ValueError:
                        # Skip invalid node values
                        continue
        
        return ";".join(compressed_nodes)
    
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
    

    
    def generate(self, output_path: str) -> bool:
        """
        Generate xLights model files following the official format specification.
        
        Args:
            output_path: Base path for output files (without extension)
            
        Returns:
            True if generation was successful, False otherwise
        """
        try:
            # Generate sphere data using aspect ratio method
            sphere = self.generate_sphere_with_aspect_ratio()
            group_assignment = self.generate_group_assignment_improved()
            
            # Write xmodel file
            xmodel_path = f"{output_path}.xmodel"
            self.write_xml_model(xmodel_path, sphere)
            
            # Write CSV file for reference
            csv_path = f"{output_path}.csv"
            self.write_csv_enhanced(csv_path, group_assignment)
            
            return True
            
        except Exception as e:
            print(f"Error generating xLights model files (.xmodel, .csv): {e}")
            return False 