import math
import xml.etree.ElementTree as ET
import csv

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


def generate_ring(start_count, number, total_size):
    """
    Generates a comma-separated list with the specified properties.
    """
    result = [""] * total_size
    result[0] = start_count
    result[-1] = start_count + number - 1
    if number - 1 > 1:
        array = [i * (total_size - 1) / (number - 2) for i in range(number - 1)]
    else:
        array = [0]
    for counter, i in enumerate(array):
        result[math.ceil(i)] = start_count + counter
    return ",".join(map(str, result))


def partition_list(a, k):
    """
    Partition list a into k groups such that the sum of each group is as balanced as possible.
    Preserves the original order of items within each group.
    Uses a greedy algorithm (Largest Fit Decreasing).
    """
    if k <= 1:
        return [a[:]]
    if k >= len(a):
        return [[x] for x in a]

    # Pair each value with its original index
    indexed_a = list(enumerate(a))
    # Sort by value descending
    sorted_indexed_a = sorted(indexed_a, key=lambda x: x[1], reverse=True)
    groups = [[] for _ in range(k)]
    group_sums = [0] * k

    for idx, value in sorted_indexed_a:
        min_group = group_sums.index(min(group_sums))
        groups[min_group].append((idx, value))
        group_sums[min_group] += value

    # Restore original order within each group
    ordered_groups = []
    for group in groups:
        group_sorted = [v for i, v in sorted(group, key=lambda x: x[0])]
        ordered_groups.append(group_sorted)

    return ordered_groups


def generate_sphere(rings, total_size):
    sphere = []
    led = 1
    for num in range(len(rings)):
        ring_list = generate_ring(led, rings[num + 1], total_size)
        led += rings[num + 1]
        sphere.append(ring_list)
    return sphere


def generate_group_assignment(rings, ports):
    groups = partition_list(list(rings.values()), ports)
    if groups is None:
        groups = []  # Defensive: should never happen
    group_assignment = {}
    ring = 1
    for group_idx, group in enumerate(groups, 1):
        for _ in group:
            group_assignment[ring] = group_idx
            ring += 1
    return group_assignment


def write_xml_model(filename, sphere):
    root = ET.Element('custommodel')
    root.set('name', 'Atlas v2')
    root.set('parm1', str(TOTAL_SIZE))
    root.set('parm2', str(len(RINGS)))
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
    tree = ET.ElementTree(root)
    ET.indent(tree)
    with open(filename, 'wb') as f:
        tree.write(f, encoding='utf-8', xml_declaration=True)


def write_csv(filename, rings, group_assignment, ports):
    """
    Write CSV file with ring and group assignment information.
    """
    headers = [
        "Ring", "LED Start", "LED End", "LEDs Per Ring",
        "DataChannel", "DC Start", "DC End", "DC Total", "PC Start", "PC End"
    ]
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        led_start = 1
        current_group = 1
        group_start = True
        group_led_total = 0
        dc_end_total = 0
        for ring in rings:
            leds_in_ring = rings[ring]
            led_end = led_start + leds_in_ring - 1
            dc = ""
            dc_start = ""
            pc_end = ""
            dc_total = ""
            dc_end = ""
            group_led_total += leds_in_ring
            # Start of a new group
            if group_assignment[ring] == current_group and group_start:
                dc = current_group
                dc_start = led_start
                group_start = False
            # End of the current group
            elif group_assignment.get(ring + 1, ports + 1) != current_group:
                pc_end = current_group
                dc_end = led_start + leds_in_ring - 1
                dc_total = group_led_total
                dc_end_total += group_led_total
                dc_end = dc_end_total
                group_start = True
                current_group += 1
                group_led_total = 0
            writer.writerow([
                ring, led_start, led_end, leds_in_ring,
                dc, dc_start, dc_end, dc_total, dc, pc_end
            ])
            led_start = led_end + 1


def main():
    sphere = generate_sphere(RINGS, TOTAL_SIZE)
    write_xml_model('atlas_v2.xmodel', sphere)
    group_assignment = generate_group_assignment(RINGS, PORTS)
    write_csv('atlas_v2.csv', RINGS, group_assignment, PORTS)


if __name__ == '__main__':
    main()
