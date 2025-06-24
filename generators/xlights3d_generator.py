"""
3D xLights model generator for LED sphere models using classic grid layout.
"""

import xml.etree.ElementTree as ET
import csv
import math
from typing import Dict, List, Tuple
from .base_generator import BaseGenerator, LEDPosition


class XLights3DGenerator(BaseGenerator):
    """Generator for 3D xLights model files using classic grid layout"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.model_name = config['model']['name']
        self.model_version = config['model']['version']
        
        # 3D specific configuration - classic grid format
        self.grid_width = 200  # Large enough for biggest rings
        self.grid_height = 60  # 49 rings + padding
        self.grid_depth = 200  # Large enough for biggest rings
        self.sphere_radius = config.get('xlights3d', {}).get('sphere_radius', 100.0)
    
    def get_format_name(self) -> str:
        return "xLights3D"
    
    def get_file_extension(self) -> str:
        return "_3d.xmodel"
    
    def map_to_grid(self, x: float, y: float, z: float) -> tuple[int, int, int]:
        """
        Map real-world coordinates to grid indices.
        
        Based on xLights coordinate mapping:
        - screenX = col - width/2
        - screenY = height - row - 1 - height/2  
        - screenZ = depth - layer - 1 - depth/2
        
        So we need:
        - col = x + width/2
        - row = height - 1 - (y + height/2)
        - layer = depth - 1 - (z + depth/2)
        
        For a sphere, we need to ensure the coordinates are properly distributed
        across the grid to create a sphere shape, not clusters.
        """
        # Map spherical coordinates to grid coordinates
        # The sphere has radius 100, so coordinates range from -100 to +100
        # We need to map this to grid coordinates 0 to grid_size-1
        
        # Map X coordinate (horizontal)
        col = int(round((x + self.sphere_radius) * (self.grid_width - 1) / (2 * self.sphere_radius)))
        
        # Map Y coordinate (vertical) - note: xLights inverts Y
        row = int(round((self.sphere_radius - y) * (self.grid_height - 1) / (2 * self.sphere_radius)))
        
        # Map Z coordinate (depth)
        layer = int(round((z + self.sphere_radius) * (self.grid_depth - 1) / (2 * self.sphere_radius)))
        
        # Clamp to grid bounds
        col = max(0, min(self.grid_width - 1, col))
        row = max(0, min(self.grid_height - 1, row))
        layer = max(0, min(self.grid_depth - 1, layer))
        
        return col, row, layer
    
    def create_classic_grid_layout(self) -> str:
        """
        Create a classic xLights grid layout string for the CustomModel attribute.
        Format: layers|rows;cols where each position contains a node number or is empty.
        
        Based on xLights source code analysis:
        - X-axis maps to columns (horizontal)
        - Y-axis maps to rows (vertical, inverted)
        - Z-axis maps to layers (depth)
        """
        self.generate_led_positions()
        
        # Create a 3D grid: [layer][row][col] = node_number
        grid = [[[-1 for _ in range(self.grid_width)] 
                for _ in range(self.grid_height)] 
                for _ in range(self.grid_depth)]
        
        # Map each LED to its grid position
        for led in self.led_positions:
            # Map spherical coordinates to grid indices
            col, row, layer = self.map_to_grid(led.x, led.y, led.z)
            
            # Store LED number in grid (1-based for xLights)
            if 0 <= layer < self.grid_depth and 0 <= row < self.grid_height and 0 <= col < self.grid_width:
                grid[layer][row][col] = led.led_number
        
        # Convert grid to CustomModel format: layers|rows;cols
        layers = []
        for layer in range(self.grid_depth):
            rows = []
            for row in range(self.grid_height):
                cols = []
                for col in range(self.grid_width):
                    node_num = grid[layer][row][col]
                    if node_num >= 0:
                        cols.append(str(node_num))
                    else:
                        cols.append("")
                rows.append(",".join(cols))
            layers.append(";".join(rows))
        
        return "|".join(layers)
    
    def create_compressed_model(self) -> str:
        """
        Create compressed model format for CustomModelCompressed attribute.
        Format: "node,row,col,layer;node,row,col,layer;..."
        
        Based on xLights source code: ParseCompressed function
        """
        compressed_entries = []
        for led in self.led_positions:
            # Map coordinates to grid positions
            col, row, layer = self.map_to_grid(led.x, led.y, led.z)
            # Add entry: node,row,col,layer (all 0-based except node which is 1-based)
            compressed_entries.append(f"{led.led_number},{row},{col},{layer}")
        return ";".join(compressed_entries)
    
    def write_3d_xml_model(self, filename: str):
        """
        Write 3D xLights XML model file in classic grid format.
        """
        # Generate LED positions first
        self.generate_led_positions()
        
        # Create the classic grid layout
        custom_model = self.create_classic_grid_layout()
        
        # Create root element
        root = ET.Element('custommodel')
        root.set('name', f'{self.model_name} 3D Grid v{self.model_version}')
        root.set('parm1', str(self.grid_height))  # Height (rows)
        root.set('parm2', str(self.grid_width))   # Width (columns)
        root.set('parm3', '1')  # Always 1 for 3D models
        root.set('Depth', str(self.grid_depth))   # Depth (layers)
        root.set('StringType', 'RGB Nodes')
        root.set('Transparency', '0')
        root.set('PixelSize', '2')
        root.set('ModelBrightness', '0')
        root.set('Antialias', '1')
        root.set('StrandNames', '')
        root.set('NodeNames', '')
        root.set('StartLatitude', '')
        root.set('EndLatitude', '')
        root.set('Degrees', '')
        root.set('CustomModel', custom_model)
        
        # Create compressed model
        compressed_model = self.create_compressed_model()
        root.set('CustomModelCompressed', compressed_model)
        
        # Add source version
        root.set('SourceVersion', '2024.13')
        
        # Write to file
        tree = ET.ElementTree(root)
        tree.write(filename, encoding='utf-8', xml_declaration=True)
    
    def write_3d_csv(self, filename: str, group_assignment: Dict[int, int]):
        """
        Write CSV output with 3D coordinate information.
        """
        headers = [
            "Ring", "LED Start", "LED End", "LEDs Per Ring",
            "DataChannel", "DC Start", "DC End", "DC Total", 
            "PC Start", "PC End", "X", "Y", "Z", "Grid Col", "Grid Row", "Grid Layer"
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
                
                # Get first LED in ring for coordinate example
                ring_leds = [pos for pos in self.led_positions if pos.ring_number == ring_num]
                if ring_leds:
                    first_led = ring_leds[0]
                    x, y, z = first_led.x, first_led.y, first_led.z
                    
                    # Calculate grid positions
                    grid_col, grid_row, grid_layer = self.map_to_grid(x, y, z)
                else:
                    x = y = z = grid_col = grid_row = grid_layer = 0
                
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
                    f"{x:.2f}", f"{y:.2f}", f"{z:.2f}",
                    grid_col, grid_row, grid_layer
                ])
                
                led_start = led_end + 1
    
    def export_3d_coordinates_json(self, filename: str):
        """Export LED coordinates to JSON for external visualization"""
        import json
        
        data = {
            "model_info": {
                "name": self.model_name,
                "version": self.model_version,
                "total_leds": len(self.led_positions),
                "rings": len(self.rings),
                "ports": self.ports,
                "grid_width": self.grid_width,
                "grid_height": self.grid_height,
                "grid_depth": self.grid_depth
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
                    },
                    "grid_position": {
                        "col": self.map_to_grid(led.x, led.y, led.z)[0],
                        "row": self.map_to_grid(led.x, led.y, led.z)[1],
                        "layer": self.map_to_grid(led.x, led.y, led.z)[2]
                    }
                }
                for led in self.led_positions
            ]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def generate_led_positions(self):
        """
        Generate LED positions for a ring-based sphere structure.
        
        Physical structure:
        - 49 rings stacked vertically (rings 1-49)
        - Each ring is a horizontal LED strip wrapped around the sphere
        - LED count varies by ring according to config
        - Rings are distributed from bottom to top of sphere
        """
        self.led_positions = []
        led_number = 1
        
        # Get ring configuration
        rings = self.config['rings']
        sphere_radius = self.config['geometry']['sphere_radius']
        
        # Calculate ring positions (latitude angles)
        # Ring 1 is at the bottom, Ring 49 is at the top
        # Map rings to latitude angles from -π/2 (bottom) to +π/2 (top)
        # Avoid poles by using a slightly smaller range
        latitude_range = math.pi * 0.9  # 90% of full sphere to avoid poles
        
        for ring_num in range(1, 50):  # 49 rings
            leds_in_ring = rings[ring_num]
            
            # Calculate latitude angle for this ring
            # Ring 1 = bottom (-π/2), Ring 49 = top (+π/2)
            latitude = ((ring_num - 1) / 48.0 - 0.5) * latitude_range
            
            # Calculate Y coordinate (height) for this ring
            y = sphere_radius * math.sin(latitude)
            
            # Calculate radius of this ring at this latitude
            ring_radius = sphere_radius * math.cos(latitude)
            
            # Distribute LEDs evenly around this ring
            for led_pos in range(leds_in_ring):
                # Calculate longitude angle (position around the ring)
                longitude = (led_pos * 2 * math.pi) / leds_in_ring
                
                # Calculate X and Z coordinates for this LED on the ring
                x = ring_radius * math.cos(longitude)
                z = ring_radius * math.sin(longitude)
                
                # Create LED position
                led = LEDPosition(
                    led_number=led_number,
                    ring_number=ring_num,
                    position_in_ring=led_pos,
                    x=x,
                    y=y,
                    z=z
                )
                
                self.led_positions.append(led)
                led_number += 1
    
    def generate(self, output_path: str) -> bool:
        """
        Generate 3D xLights model files.
        """
        try:
            # Generate group assignment
            group_assignment = self.generate_group_assignment_improved()
            
            # Write files
            self.write_3d_xml_model(f"{output_path}{self.get_file_extension()}")
            self.write_3d_csv(f"{output_path}_3d.csv", group_assignment)
            self.export_3d_coordinates_json(f"{output_path}_3d_coordinates.json")
            
            return True
            
        except Exception as e:
            print(f"Error generating 3D xLights model files (_3d.xmodel, _3d.csv, _3d_coordinates.json): {e}")
            return False 