"""
Common functionality for xLights generators (2D and 3D).
This module contains shared logic for CSV generation and other common operations.
"""

import csv
from typing import Dict, List, Tuple, Optional, Callable
from .base_generator import LEDPosition


class XLightsCommon:
    """Common functionality for xLights generators"""
    
    @staticmethod
    def write_csv_with_group_assignment(filename: str, group_assignment: Dict[int, int], 
                                      rings: Dict[int, int], led_positions: List[LEDPosition],
                                      ports: int, additional_headers: Optional[List[str]] = None,
                                      additional_data_func: Optional[Callable[[int, List[LEDPosition]], List]] = None):
        """
        Write CSV output using the exact logic from original Atlas v2 code.
        
        Args:
            filename: Output CSV filename
            group_assignment: Ring to group assignment mapping
            rings: Ring configuration dictionary
            led_positions: List of LED positions
            ports: Number of ports
            additional_headers: Additional CSV headers beyond the standard ones
            additional_data_func: Function to generate additional data for each row
        """
        # Standard headers
        headers = [
            "Ring", "LED Start", "LED End", "LEDs Per Ring",
            "DataChannel", "DC Start", "DC End", "DC Total", 
            "PC Start", "PC End"
        ]
        
        # Add additional headers if provided
        if additional_headers:
            headers.extend(additional_headers)
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            
            led = 1
            group = 1
            groupStart = True
            groupStartLED = 1
            groupTotal = 0
            dcEndTotal = 0
            
            for ring_num in sorted(rings.keys()):
                leds_in_ring = rings[ring_num]
                led_end = led + leds_in_ring - 1
                
                # Use the exact logic from original Atlas v2 code
                dc = ""
                dcStart = ""
                powerStart = ""
                pcEnd = ""
                dcTotal = ""
                dcEnd = ""
                groupTotal = groupTotal + leds_in_ring
                
                if group_assignment[ring_num] == group and groupStart:
                    dc = group
                    dcStart = led
                    powerStart = group   
                    groupStart = False        
                elif group_assignment.get(ring_num+1, ports+1) != group:
                    pcEnd = group
                    dcEnd = groupStartLED + groupTotal
                    dcTotal = groupTotal
                    dcEndTotal = dcEndTotal + groupTotal
                    dcEnd = dcEndTotal
                    groupStart = True
                    group = group + 1
                    groupTotal = 0
                
                # Base row data
                row_data = [
                    ring_num, led, led_end, leds_in_ring,
                    dc, dcStart, dcEnd, dcTotal, powerStart, pcEnd
                ]
                
                # Add additional data if function provided
                if additional_data_func:
                    additional_data = additional_data_func(ring_num, led_positions)
                    row_data.extend(additional_data)
                
                writer.writerow(row_data)
                led = led + leds_in_ring
    
    @staticmethod
    def get_average_coordinates(ring_num: int, led_positions: List[LEDPosition]) -> Tuple[float, float, float]:
        """
        Calculate average coordinates for a ring.
        
        Args:
            ring_num: Ring number
            led_positions: List of LED positions
            
        Returns:
            Tuple of (avg_x, avg_y, avg_z)
        """
        ring_leds = [pos for pos in led_positions if pos.ring_number == ring_num]
        if not ring_leds:
            return 0.0, 0.0, 0.0
        
        avg_x = sum(led.x for led in ring_leds) / len(ring_leds)
        avg_y = sum(led.y for led in ring_leds) / len(ring_leds)
        avg_z = sum(led.z for led in ring_leds) / len(ring_leds)
        
        return avg_x, avg_y, avg_z
    
    @staticmethod
    def get_first_led_coordinates(ring_num: int, led_positions: List[LEDPosition]) -> Tuple[float, float, float]:
        """
        Get coordinates of the first LED in a ring.
        
        Args:
            ring_num: Ring number
            led_positions: List of LED positions
            
        Returns:
            Tuple of (x, y, z) for first LED in ring
        """
        ring_leds = [pos for pos in led_positions if pos.ring_number == ring_num]
        if not ring_leds:
            return 0.0, 0.0, 0.0
        
        first_led = ring_leds[0]
        return first_led.x, first_led.y, first_led.z 