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

ports = 16

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


# This code was found on stackoverflow here: https://stackoverflow.com/questions/35517051/split-a-list-of-numbers-into-n-chunks-such-that-the-chunks-have-close-to-equal
# Splitting into roughly equal lists was not easy!
def partition_list(a, k):
    """
    Partitions a list of numbers into equal groupings by sum
    
    Args:
        a: the list to partition
        k: the number of partitions
    This code was found on stackoverflow here: https://stackoverflow.com/questions/35517051/split-a-list-of-numbers-into-n-chunks-such-that-the-chunks-have-close-to-equal
    
    Splitting into roughly equal lists was not easy!
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
    best_partitions = None
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





groups = partition_list(list(rings.values()), ports)

group_assignment = {}

ring = 1
for group_idx, group in enumerate(groups, 1):  # 1-based indexing
    for ring_num in group:
        group_assignment[ring] = group_idx
        ring = ring +1
        
        
led = 1
group = 1
groupStart = True
groupStartLED = 1
groupTotal = 0
dcEndTotal = 0

orig_stdout = sys.stdout
f = open('atlas_v2.csv', 'w')
sys.stdout = f

print("Ring,LED Start,LED End,LEDs Per Ring,DataChannel,DC Start,DC End,DC Total, PC Start, PC End")
for ring in rings:
    dc = ""
    dcStart = ""
    powerStart = ""
    pcEnd = ""
    dcTotal = ""
    dcEnd = ""
    groupTotal = groupTotal + rings[ring]
    if group_assignment[ring] == group and groupStart:
        dc = group
        dcStart = led
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
    print(f"{ring},{led},{led+rings[ring]-1},{rings[ring]},{dc},{dcStart},{dcEnd},{dcTotal},{dc},{pcEnd}")
    led = led + rings[ring]
sys.stdout = orig_stdout
f.close()
