import numpy as np
import math
import sys

# Assuming you used the stock model with 49 Rings, 
# just change the value after each ring number to 
# match the number of LEDs in that ring

rings = { 1: 32,
          2: 54,
          3: 71,
          4: 82,
          5: 90,
          6: 99,
          7: 107,
          8: 113,
          9: 119,
          10: 125,
          11: 129,
          12: 133,
          13: 136,
          14: 140,
          15: 143,
          16: 146,
          17: 148,
          18: 151,
          19: 154,
          20: 154,
          21: 155,
          22: 157,
          23: 158,
          24: 158,
          25: 158,
          26: 158,
          27: 157,
          28: 156,
          29: 155,
          30: 154,
          31: 153,
          32: 151,
          33: 147,
          34: 147,
          35: 143,
          36: 140,
          37: 137,
          38: 133,
          39: 129,
          40: 124,
          41: 119,
          42: 113,
          43: 107,
          44: 99,
          45: 91,
          46: 81,
          47: 70,
          48: 55,
          49: 32
          }

# totalSize is the number of columns in the "screen"
# Should match the value in startString
totalSize = 1000

ports = 32

def generate_ring(startCount, number, totalSize):
    """
    Generates a comma-separated list with the specified properties.

    Args:
        startCount: The first LED in the ring.
        number: The total number of LEDs in the ring.
        totalSize: The size of the "display" to spread the LEDs across.

    Returns:
        The generated list as a comma separated string of integers.
    """

    result = [""] * totalSize
    result[0] = startCount
    result[-1] = startCount + number - 1

    # Calculate the step size for evenly spacing the numbers (rounding up)
    step = int((totalSize - 2) / (number - 2))
    array = np.linspace(0, totalSize-1, endpoint=False, num=number-1)
    counter = 0
    for i in array:
        # Math.ceil is used to convert the float to an int, opting to round up
        result[math.ceil(i)] = startCount + counter
        counter = counter + 1
    return ",".join(map(str, result))  # Convert to comma-separated string



led = 1     
sphere = []

for num in range(0, len(rings)):
    ring_list = generate_ring(led, rings[num+1], totalSize)
    led = led + rings[num+1]
    sphere.append(ring_list)

orig_stdout = sys.stdout
f = open('atlas_v2.xmodel', 'w')
sys.stdout = f
# Print out the strings for the beginning of the xmodel file    
print('<?xml version="1.0" encoding="UTF-8"?>')
print('<custommodel ')

startString = 'name="Atlas v2" parm1="1000" parm2="76" Depth="1" StringType="GRB Nodes" Transparency="0" PixelSize="2" ModelBrightness="0" Antialias="1" StrandNames="" NodeNames="" CustomModel="'
endString = '" SourceVersion="2023.20"  >'

print(startString + ";".join(sphere) + endString)
print('</custommodel>')

sys.stdout = orig_stdout
f.close()

totalLeds = sum(rings.values())
print(totalLeds)


# Get sorted ring numbers.
ring_numbers = np.array(sorted(rings.keys()))

# Calculate group boundaries using NumPy's array_split for near-equal division
group_boundaries = np.array_split(ring_numbers, ports)

# Create the new dictionary
group_assignment = {}
for group_idx, group in enumerate(group_boundaries, 1):  # 1-based indexing
    for ring_num in group:
        group_assignment[ring_num] = group_idx
        
#groupTotal = {}
#for group in range(1, 16):
#    groupTotal[group] = 0
#    for ring in rings:
#        if group_assignment[ring] == group:
#            groupTotal[group] = groupTotal[group] + rings[ring]
#print(groupTotal)

led = 1
group = 1
groupStart = True
groupStartLED = 1
groupTotal = 0
dcEndTotal = 0

orig_stdout = sys.stdout
f = open('atlas_v2.csv', 'w')
sys.stdout = f

print("Ring,LED Start,LED End,LEDs Per Ring,DC Start,DC End,DC Total, PC Start, PC End")
for ring in rings:
    dcStart = ""
    powerStart = ""
    pcEnd = ""
    dcTotal = ""
    dcEnd = ""
    groupTotal = groupTotal + rings[ring]
    if group_assignment[ring] == group and groupStart:
        dcStart = group
        powerStart = group   
        groupStart = False        
    elif group_assignment.get(ring+1, ports+1) != group:
        pcEnd = group
        dcEnd = groupStartLED + groupTotal
        dcTotal = groupTotal
        dcEndTotal = dcEndTotal + groupTotal
        dcEnd = dcEndTotal
        groupStart = True
        group = group + 1
        groupTotal = 0
    print(f"{ring},{led},{led+rings[ring]-1},{rings[ring]},{dcStart},{dcEnd},{dcTotal},{dcStart},{pcEnd}")
    led = led + rings[ring]
sys.stdout = orig_stdout
f.close()