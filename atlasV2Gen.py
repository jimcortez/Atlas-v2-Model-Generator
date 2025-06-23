import math
import xml.etree.ElementTree as ET
import csv
import argparse
from dataclasses import dataclass
from typing import List, Tuple, Dict
import json

# Model configuration
RINGS = {
    1: 33,
    2: 55,
    3: 70,
    4: 82,
    5: 92,
    6: 100,
    7: 108,
    8: 114,
    9: 120,
    10: 126,
    11: 139,
    12: 134,
    13: 137,
    14: 141,
    15: 144,
    16: 147,
    17: 149,
    18: 152,
    19: 155,
    20: 155,
    21: 156,
    22: 158,
    23: 159,
    24: 159,
    25: 159,
    26: 159,
    27: 158,
    28: 157,
    29: 156,
    30: 155,
    31: 154,
    32: 152,
    33: 148,
    34: 148,
    35: 144,
    36: 141,
    37: 138,
    38: 134,
    39: 130,
    40: 125,
    41: 120,
    42: 114,
    43: 108,
    44: 100,
    45: 92,
    46: 82,
    47: 71,
    48: 56,
    49: 33
}
TOTAL_SIZE = 1000
PORTS = 16


@dataclass
class LEDPosition:
    """Represents an LED with its position and properties"""
    led_number: int
    ring_number: int
    position_in_ring: int
    x: float
    y: float
    z: float


class AtlasV2GeneratorV2:
    """Alternative implementation using coordinate-based positioning"""
    
    def __init__(self, rings: Dict[int, int], total_size: int, ports: int):
        self.rings = rings
        self.total_size = total_size
        self.ports = ports
        self.led_positions: List[LEDPosition] = []
        self.sphere_radius = 100.0  # Virtual radius for coordinate calculation
        
    def calculate_spherical_coordinates(self, ring_num: int, position_in_ring: int, 
                                      leds_in_ring: int) -> Tuple[float, float, float]:
        """
        Calculate 3D coordinates for an LED on a spherical surface.
        Uses spherical coordinates converted to Cartesian.
        """
        # Ring angle (latitude) - rings are horizontal circles
        ring_angle = (ring_num - 1) * math.pi / (len(self.rings) - 1)  # 0 to pi
        
        # Position angle (longitude) within the ring
        if leds_in_ring > 1:
            position_angle = (position_in_ring * 2 * math.pi) / leds_in_ring
        else:
            position_angle = 0
            
        # Convert spherical to Cartesian coordinates
        x = self.sphere_radius * math.sin(ring_angle) * math.cos(position_angle)
        y = self.sphere_radius * math.sin(ring_angle) * math.sin(position_angle)
        z = self.sphere_radius * math.cos(ring_angle)
        
        return x, y, z
    
    def generate_led_positions(self):
        """Generate all LED positions with coordinates"""
        led_number = 1
        for ring_num, leds_in_ring in self.rings.items():
            for position_in_ring in range(leds_in_ring):
                x, y, z = self.calculate_spherical_coordinates(
                    ring_num, position_in_ring, leds_in_ring
                )
                
                led_pos = LEDPosition(
                    led_number=led_number,
                    ring_number=ring_num,
                    position_in_ring=position_in_ring,
                    x=x, y=y, z=z
                )
                self.led_positions.append(led_pos)
                led_number += 1
    
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
    
    def generate_group_assignment_improved(self) -> Dict[int, int]:
        """
        Improved group assignment using dynamic programming for better balance.
        """
        ring_values = list(self.rings.values())
        n_rings = len(ring_values)
        
        # Dynamic programming approach for optimal partitioning
        dp = [[float('inf')] * (self.ports + 1) for _ in range(n_rings + 1)]
        partition = [[0] * (self.ports + 1) for _ in range(n_rings + 1)]
        
        # Base case: 0 rings can be assigned to any number of ports
        for j in range(self.ports + 1):
            dp[0][j] = 0
        
        # Fill dp table
        for i in range(1, n_rings + 1):
            for j in range(1, self.ports + 1):
                if j == 1:
                    # All rings in one group
                    dp[i][j] = sum(ring_values[:i])
                    partition[i][j] = 0
                else:
                    # Try different partition points
                    for k in range(i):
                        current_sum = sum(ring_values[k:i])
                        max_sum = max(dp[k][j-1], current_sum)
                        if max_sum < dp[i][j]:
                            dp[i][j] = max_sum
                            partition[i][j] = k
        
        # Reconstruct the assignment
        group_assignment = {}
        self._reconstruct_assignment(partition, n_rings, self.ports, group_assignment, 1)
        
        return group_assignment
    
    def _reconstruct_assignment(self, partition, i, j, assignment, group_id):
        """Helper method to reconstruct group assignment from DP table"""
        if i == 0 or j == 0:
            return
        
        k = partition[i][j]
        if j == 1:
            # All remaining rings go to current group
            for ring_idx in range(1, i + 1):
                assignment[ring_idx] = group_id
        else:
            # Assign rings from k+1 to i to current group
            for ring_idx in range(k + 1, i + 1):
                assignment[ring_idx] = group_id
            # Recursively assign remaining rings
            self._reconstruct_assignment(partition, k, j - 1, assignment, group_id + 1)
    
    def write_xml_model_alternative(self, filename: str, sphere: List[str]):
        """
        Alternative XML generation using a more structured approach.
        """
        # Create root element with more detailed attributes
        root = ET.Element('custommodel')
        root.set('name', 'Atlas v2 (Alternative)')
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
        metadata.set('generator', 'AtlasV2GeneratorV2')
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
        Enhanced CSV output with additional coordinate information.
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
        data = {
            "model_info": {
                "name": "Atlas v2",
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


def main():
    parser = argparse.ArgumentParser(description='Generate Atlas v2 xLights model and CSV files (Alternative Implementation)')
    parser.add_argument('--xmodel', '-x', default='atlas_v2.xmodel',
                       help='Output filename for xmodel file (default: atlas_v2.xmodel)')
    parser.add_argument('--csv', '-c', default='atlas_v2.csv',
                       help='Output filename for CSV file (default: atlas_v2.csv)')
    parser.add_argument('--json', '-j', default='atlas_v2_coordinates.json',
                       help='Output filename for coordinates JSON file (default: atlas_v2_coordinates.json)')
    args = parser.parse_args()
    
    # Create generator instance
    generator = AtlasV2GeneratorV2(RINGS, TOTAL_SIZE, PORTS)
    
    # Generate sphere using alternative method
    sphere = generator.generate_sphere_alternative()
    
    # Write files
    generator.write_xml_model_alternative(args.xmodel, sphere)
    group_assignment = generator.generate_group_assignment_improved()
    generator.write_csv_enhanced(args.csv, group_assignment)
    generator.export_coordinates_json(args.json)
    
    print(f"Generated files:")
    print(f"  - xModel: {args.xmodel}")
    print(f"  - CSV: {args.csv}")
    print(f"  - Coordinates JSON: {args.json}")
    print(f"  - Total LEDs: {len(generator.led_positions)}")
    print(f"  - Rings: {len(RINGS)}")
    print(f"  - Ports: {PORTS}")


if __name__ == '__main__':
    main() 