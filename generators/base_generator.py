"""
Base generator class for LED sphere models.
This class provides common functionality for all format generators.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Tuple, Any
import math


@dataclass
class LEDPosition:
    """Represents an LED with its position and properties"""
    led_number: int
    ring_number: int
    position_in_ring: int
    x: float
    y: float
    z: float


class BaseGenerator(ABC):
    """Abstract base class for all LED sphere model generators"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the generator with configuration data.
        
        Args:
            config: Configuration dictionary loaded from YAML
        """
        self.config = config
        self.rings = config['rings']
        self.total_size = config['controller']['total_size']
        self.ports = config['controller']['ports']
        self.sphere_radius = config['geometry']['sphere_radius']
        self.led_positions: List[LEDPosition] = []
        
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
    
    @abstractmethod
    def generate(self, output_path: str) -> bool:
        """
        Generate the model file for this format.
        
        Args:
            output_path: Path where the output file should be saved
            
        Returns:
            True if generation was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def get_format_name(self) -> str:
        """Return the name of this format"""
        pass
    
    @abstractmethod
    def get_file_extension(self) -> str:
        """Return the file extension for this format"""
        pass 