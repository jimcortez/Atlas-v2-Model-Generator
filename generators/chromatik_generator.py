"""
Chromatik model generator for LED sphere models.
Generates .lxf JSON fixture files for Chromatik LED mapping software.
"""

import json
import math
from typing import Dict, List, Any
from .base_generator import BaseGenerator


class ChromatikGenerator(BaseGenerator):
    """Generator for Chromatik fixture files (.lxf)"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.model_name = config['model']['name']
        self.model_version = config['model']['version']
        
        # Chromatik specific configuration
        chromatik_config = config.get('chromatik', {})
        self.artnet_host = chromatik_config.get('artnet_host', '127.0.0.1')
        self.artnet_start_universe = chromatik_config.get('artnet_start_universe', 0)
        self.dmx_start_channel = chromatik_config.get('dmx_start_channel', 1)
    
    def get_format_name(self) -> str:
        return "chromatik"
    
    def get_file_extension(self) -> str:
        return ".lxf"
    
    def calculate_ring_center(self, ring_num: int) -> tuple[float, float, float]:
        """
        Calculate the center position of a ring for component positioning.
        Uses the average of all LED positions in the ring.
        
        Args:
            ring_num: Ring number
            
        Returns:
            Tuple of (x, y, z) coordinates for ring center
        """
        ring_leds = [pos for pos in self.led_positions if pos.ring_number == ring_num]
        if not ring_leds:
            return 0.0, 0.0, 0.0
        
        avg_x = sum(led.x for led in ring_leds) / len(ring_leds)
        avg_y = sum(led.y for led in ring_leds) / len(ring_leds)
        avg_z = sum(led.z for led in ring_leds) / len(ring_leds)
        
        return avg_x, avg_y, avg_z
    
    def calculate_ring_spacing(self, ring_num: int) -> float:
        """
        Calculate the spacing between LEDs in a ring.
        Uses the circumference of the ring divided by number of LEDs.
        
        Args:
            ring_num: Ring number
            
        Returns:
            Spacing value in units
        """
        leds_in_ring = self.rings[ring_num]
        if leds_in_ring <= 1:
            return 0.0
        
        # Calculate ring radius at this latitude
        ring_angle = ((ring_num - 1) / (len(self.rings) - 1) - 0.5) * math.pi
        ring_radius = self.sphere_radius * math.cos(ring_angle)
        
        # Calculate circumference
        circumference = 2 * math.pi * ring_radius
        
        # Spacing is circumference divided by number of LEDs
        return circumference / leds_in_ring
    
    def transform_coordinates_for_chromatik(self, x: float, y: float, z: float) -> tuple[float, float, float]:
        """
        Transform coordinates from Z-up (base generator) to Chromatik's coordinate system.
        Chromatik uses Y-axis as vertical. To fix the 90-degree rotation issue,
        we rotate 90 degrees around Y-axis (swapping X and Z, negating X).
        
        Transformation (rotate 90° around Y-axis):
        - Chromatik X = original Z
        - Chromatik Y = original Y (vertical axis stays vertical)
        - Chromatik Z = -original X
        
        This rotates the sphere so the top/bottom axis aligns correctly.
        
        Args:
            x: Original X coordinate
            y: Original Y coordinate
            z: Original Z coordinate
            
        Returns:
            Tuple of (x, y, z) in Chromatik coordinate system
        """
        # Rotate 90 degrees around Y-axis: (X, Y, Z) -> (Z, Y, -X)
        return z, y, -x
    
    def calculate_ring_radius(self, ring_num: int) -> float:
        """
        Calculate the radius of a ring at its latitude.
        Ensures radius is always greater than 0 (minimum 1) to satisfy Chromatik requirements.
        
        Args:
            ring_num: Ring number
            
        Returns:
            Radius of the ring in units (minimum 1)
        """
        # Calculate ring angle (latitude)
        ring_angle = ((ring_num - 1) / (len(self.rings) - 1) - 0.5) * math.pi
        
        # Calculate ring radius at this latitude
        ring_radius = self.sphere_radius * math.cos(ring_angle)
        
        # Ensure radius is always greater than 0 (Chromatik requirement)
        # Use minimum of 1 to avoid zero radius at poles
        if ring_radius <= 0:
            ring_radius = 1.0
        
        return ring_radius
    
    def calculate_ring_center_y(self, ring_num: int) -> float:
        """
        Calculate the Y coordinate (vertical) of the ring center in Chromatik coordinates.
        This is based on the ring's latitude on the sphere.
        
        Args:
            ring_num: Ring number
            
        Returns:
            Y coordinate of the ring center
        """
        # Calculate ring angle (latitude) - same as in base generator
        ring_angle = ((ring_num - 1) / (len(self.rings) - 1) - 0.5) * math.pi
        
        # In the base generator's Z-up system, the vertical coordinate is z = sphere_radius * sin(ring_angle)
        # For the center of a horizontal ring at this latitude, the original coordinates are:
        # (0, 0, sphere_radius * sin(ring_angle))
        
        # Apply the coordinate transformation: (x, y, z) -> (z, y, -x)
        # Original: (0, 0, sphere_radius * sin(ring_angle))
        # Transformed: (sphere_radius * sin(ring_angle), 0, 0)
        # So X = sphere_radius * sin(ring_angle), Y = 0, Z = 0
        
        # However, Chromatik uses Y-up, so the vertical should be in Y.
        # Since my transform puts original z into X, I need to adjust.
        # For the arc center position, I'll use the original z value directly as Y
        # (this assumes we want Y to be the vertical axis in Chromatik)
        original_z = self.sphere_radius * math.sin(ring_angle)
        
        # Use original z as Y coordinate (vertical in Chromatik)
        return original_z
    
    def create_ring_component(self, ring_num: int) -> Dict[str, Any]:
        """
        Create a component definition for a single ring using arc type.
        Each ring is a full 360-degree arc at a specific latitude on the sphere.
        Coordinates are transformed to Chromatik's Y-up coordinate system.
        
        Args:
            ring_num: Ring number
            
        Returns:
            Component dictionary with arc type
        """
        leds_in_ring = self.rings[ring_num]
        
        # Calculate ring center position
        # For horizontal rings on a sphere, center is at (0, y_latitude, 0)
        # where y_latitude is the Y coordinate of the ring's latitude
        center_y = self.calculate_ring_center_y(ring_num)
        center_x = 0.0  # Rings are centered horizontally
        center_z = 0.0  # Rings are centered horizontally
        
        # Calculate ring radius
        ring_radius = self.calculate_ring_radius(ring_num)
        
        # Create arc component
        # For a full circle, degrees is 360.0
        # The arc lies in the X-Z plane (horizontal), with Y as the vertical axis
        # Use normal vector pointing along Y-axis for horizontal rings
        component = {
            "type": "arc",
            "id": f"ring_{ring_num}",
            "mode": "center",
            "x": round(center_x, 2),
            "y": round(center_y, 2),
            "z": round(center_z, 2),
            "radius": int(round(ring_radius)),
            "numPoints": leds_in_ring,
            "degrees": 360.0,
            "normal": {
                "x": 0,
                "y": 1,
                "z": 0
            }
        }
        
        return component
        
        return component
    
    def calculate_led_ranges_per_port(self, group_assignment: Dict[int, int]) -> Dict[int, Dict[str, int]]:
        """
        Calculate the LED number ranges for each port/group.
        
        Args:
            group_assignment: Dictionary mapping ring number to port/group number
            
        Returns:
            Dictionary mapping port number to {'start': first_led, 'num': count}
        """
        # Count LEDs per port
        leds_per_port = {}
        for ring_num, port_num in group_assignment.items():
            if port_num not in leds_per_port:
                leds_per_port[port_num] = []
            leds_per_port[port_num].extend(
                [led.led_number for led in self.led_positions if led.ring_number == ring_num]
            )
        
        # Calculate ranges
        port_ranges = {}
        current_led = 1
        
        for port_num in sorted(leds_per_port.keys()):
            port_leds = sorted(leds_per_port[port_num])
            if port_leds:
                start_led = min(port_leds)
                num_leds = len(port_leds)
                port_ranges[port_num] = {
                    'start': start_led,
                    'num': num_leds
                }
        
        return port_ranges
    
    def calculate_artnet_universe_and_channel(self, led_number: int) -> tuple[int, int]:
        """
        Calculate ArtNet universe and DMX channel for a given LED.
        Each LED uses 3 DMX channels (RGB).
        
        Args:
            led_number: LED number (1-based)
            
        Returns:
            Tuple of (universe, channel) where channel is 1-based DMX channel
        """
        # Calculate base DMX channel (first channel of RGB triplet)
        base_channel = self.dmx_start_channel + (led_number - 1) * 3
        
        # Calculate universe (512 channels per universe)
        universe = self.artnet_start_universe + (base_channel - 1) // 512
        
        # Calculate channel within universe (1-based)
        channel = ((base_channel - 1) % 512) + 1
        
        return universe, channel
    
    def create_output_segments(self, group_assignment: Dict[int, int]) -> List[Dict[str, Any]]:
        """
        Create output segments for each port/group.
        Uses componentId references to reference ring components.
        
        Args:
            group_assignment: Dictionary mapping ring number to port/group number
            
        Returns:
            List of segment dictionaries
        """
        segments = []
        
        # Group rings by port
        rings_per_port = {}
        for ring_num, port_num in group_assignment.items():
            if port_num not in rings_per_port:
                rings_per_port[port_num] = []
            rings_per_port[port_num].append(ring_num)
        
        # Create segments - one segment per ring, using componentId references
        # This allows Chromatik to properly map each ring component
        for port_num in sorted(rings_per_port.keys()):
            port_rings = sorted(rings_per_port[port_num])
            
            # Create a segment for each ring in this port
            # Each segment references the ring component by ID
            for ring_num in port_rings:
                segment = {
                    "componentId": f"ring_{ring_num}"
                }
                segments.append(segment)
        
        return segments
    
    def create_artnet_output(self, group_assignment: Dict[int, int]) -> Dict[str, Any]:
        """
        Create ArtNet output configuration with segments.
        
        Args:
            group_assignment: Dictionary mapping ring number to port/group number
            
        Returns:
            Output dictionary
        """
        # Calculate LED ranges per port
        port_ranges = self.calculate_led_ranges_per_port(group_assignment)
        
        # Create segments
        segments = self.create_output_segments(group_assignment)
        
        # For segmented output, we typically use one universe per segment
        # or calculate based on channel requirements
        # For simplicity, we'll use the starting universe and let Chromatik handle it
        # or we can calculate per segment
        
        output = {
            "protocol": "artnet",
            "host": self.artnet_host,
            "universe": self.artnet_start_universe,
            "segments": segments
        }
        
        return output
    
    def create_fixture_definition(self, group_assignment: Dict[int, int]) -> Dict[str, Any]:
        """
        Create the complete Chromatik fixture definition.
        
        Args:
            group_assignment: Dictionary mapping ring number to port/group number
            
        Returns:
            Complete fixture dictionary
        """
        # Generate LED positions first
        self.generate_led_positions()
        
        # Create components (one per ring)
        components = []
        for ring_num in sorted(self.rings.keys()):
            component = self.create_ring_component(ring_num)
            components.append(component)
        
        # Create ArtNet output
        output = self.create_artnet_output(group_assignment)
        
        # Create fixture definition
        fixture = {
            "label": f"{self.model_name} v{self.model_version}",
            "tags": ["sphere", "led", "atlas"],
            "components": components,
            "outputs": [output]
        }
        
        return fixture
    
    def generate(self, output_path: str) -> bool:
        """
        Generate Chromatik fixture file (.lxf).
        
        Args:
            output_path: Base path for output file (without extension)
            
        Returns:
            True if generation was successful, False otherwise
        """
        try:
            # Generate group assignment
            group_assignment = self.generate_group_assignment_improved()
            
            # Create fixture definition
            fixture = self.create_fixture_definition(group_assignment)
            
            # Write JSON file
            lxf_path = f"{output_path}.lxf"
            with open(lxf_path, 'w', encoding='utf-8') as f:
                json.dump(fixture, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error generating Chromatik fixture file (.lxf): {e}")
            return False

