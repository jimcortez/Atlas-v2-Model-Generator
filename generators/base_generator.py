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
        
        The sphere is oriented with:
        - Z-axis: vertical (poles at top/bottom)
        - X-Y plane: horizontal (equator)
        - Rings: horizontal circles at different latitudes
        """
        # Use the full latitude range from -pi/2 to +pi/2
        ring_angle = ((ring_num - 1) / (len(self.rings) - 1) - 0.5) * math.pi
        
        # Position angle (longitude) within the ring
        if leds_in_ring > 1:
            position_angle = (position_in_ring * 2 * math.pi) / leds_in_ring
        else:
            position_angle = 0
            
        # Convert spherical to Cartesian coordinates
        # x = r * cos(lat) * cos(lon)
        # y = r * cos(lat) * sin(lon)  
        # z = r * sin(lat)
        x = self.sphere_radius * math.cos(ring_angle) * math.cos(position_angle)
        y = self.sphere_radius * math.cos(ring_angle) * math.sin(position_angle)
        z = self.sphere_radius * math.sin(ring_angle)
        
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
    
    def partition_list(self, a: List[int], k: int) -> List[List[int]]:
        """
        Partitions a list of numbers into equal groupings by sum
        This is the exact algorithm from the original Atlas v2 code
        
        Args:
            a: the list to partition
            k: the number of partitions
        """
        #check degenerate conditions
        if k <= 1: return [a]
        if k >= len(a): return [[x] for x in a]
        #create a list of indexes to partition between, using the index on the
        #left of the partition to indicate where to partition
        #to start, roughly partition the array into equal groups of len(a)/k (note
        #that the last group may be a different size) 
        partition_between = []
        for i in range(k-1):
            partition_between.append((i+1)*len(a)//k)  # Note I did change the code to // to avoid floats
        #the ideal size for all partitions is the total height of the list divided
        #by the number of paritions
        average_height = float(sum(a))/k
        best_score = None
        best_partitions: List[List[int]] = []
        count = 0
        no_improvements_count = 0
        #loop over possible partitionings
        while True:
            #partition the list
            partitions = []
            index = 0
            for div in partition_between:
                #create partitions based on partition_between
                partitions.append(a[index:div])
                index = div
            #append the last partition, which runs from the last partition divider
            #to the end of the list
            partitions.append(a[index:])
            #evaluate the partitioning
            worst_height_diff = 0
            worst_partition_index = -1
            for p in partitions:
                #compare the partition height to the ideal partition height
                height_diff = average_height - sum(p)
                #if it's the worst partition we've seen, update the variables that
                #track that
                if abs(height_diff) > abs(worst_height_diff):
                    worst_height_diff = height_diff
                    worst_partition_index = partitions.index(p)
            #if the worst partition from this run is still better than anything
            #we saw in previous iterations, update our best-ever variables
            if best_score is None or abs(worst_height_diff) < best_score:
                best_score = abs(worst_height_diff)
                best_partitions = partitions
                no_improvements_count = 0
            else:
                no_improvements_count += 1
            #decide if we're done: if all our partition heights are ideal, or if
            #we haven't seen improvement in >5 iterations, or we've tried 100
            #different partitionings
            #the criteria to exit are important for getting a good result with
            #complex data, and changing them is a good way to experiment with getting
            #improved results
            if worst_height_diff == 0 or no_improvements_count > 10 or count > 100:
                return best_partitions
            count += 1
            #adjust the partitioning of the worst partition to move it closer to the
            #ideal size. the overall goal is to take the worst partition and adjust
            #its size to try and make its height closer to the ideal. generally, if
            #the worst partition is too big, we want to shrink the worst partition
            #by moving one of its ends into the smaller of the two neighboring
            #partitions. if the worst partition is too small, we want to grow the
            #partition by expanding the partition towards the larger of the two
            #neighboring partitions
            if worst_partition_index == 0:   #the worst partition is the first one
                if worst_height_diff < 0: partition_between[0] -= 1   #partition too big, so make it smaller
                else: partition_between[0] += 1   #partition too small, so make it bigger
            elif worst_partition_index == len(partitions)-1: #the worst partition is the last one
                if worst_height_diff < 0: partition_between[-1] += 1   #partition too small, so make it bigger
                else: partition_between[-1] -= 1   #partition too big, so make it smaller
            else:   #the worst partition is in the middle somewhere
                left_bound = worst_partition_index - 1   #the divider before the partition
                right_bound = worst_partition_index   #the divider after the partition
                if worst_height_diff < 0:   #partition too big, so make it smaller
                    if sum(partitions[worst_partition_index-1]) > sum(partitions[worst_partition_index+1]):   #the partition on the left is bigger than the one on the right, so make the one on the right bigger
                        partition_between[right_bound] -= 1
                    else:   #the partition on the left is smaller than the one on the right, so make the one on the left bigger
                        partition_between[left_bound] += 1
                else:   #partition too small, make it bigger
                    if sum(partitions[worst_partition_index-1]) > sum(partitions[worst_partition_index+1]): #the partition on the left is bigger than the one on the right, so make the one on the left smaller
                        partition_between[left_bound] -= 1
                    else:   #the partition on the left is smaller than the one on the right, so make the one on the right smaller
                        partition_between[right_bound] += 1

    def generate_group_assignment_improved(self) -> Dict[int, int]:
        """
        Generate group assignment using the exact partitioning algorithm from Atlas v2.
        """
        # Get the ring values in order
        ring_values = [self.rings[ring_num] for ring_num in sorted(self.rings.keys())]
        
        # Use the original Atlas v2 partitioning algorithm
        groups: List[List[int]] = self.partition_list(ring_values, self.ports)
        
        # Create group assignment mapping
        group_assignment = {}
        ring = 1
        for group_idx, group in enumerate(groups, 1):  # 1-based indexing
            for ring_num in group:
                group_assignment[ring] = group_idx
                ring = ring + 1
        
        return group_assignment
    
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