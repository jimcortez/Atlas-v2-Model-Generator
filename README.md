# Atlas v2 LED Sphere - xLights Model Generator

A Python script to generate xLights model files and CSV configuration for the Atlas v2 LED Sphere by DrZzs & GrZzs.

This code is based on the work of https://github.com/kraegar/Atlas-v2-xmodel

## Overview

This tool creates:
- An `.xmodel` file that can be imported into xLights
- A CSV file with ring and group assignment information
- A JSON file with detailed 3D coordinate data for each LED
- Enhanced metadata and spatial information for advanced applications

## Features

- **Coordinate-Based Positioning**: Uses precise 3D spherical coordinates for accurate LED placement
- **Dynamic Programming**: Optimized group assignment algorithm for balanced load distribution
- **Enhanced Metadata**: Rich XML structure with coordinate information and generation details
- **Multiple Output Formats**: xModel, CSV, and JSON outputs for different use cases

## Prerequisites

- Python 3.7 or higher (for dataclasses support)
- No external dependencies required (uses only built-in Python libraries)

## Installation

1. Clone this repository:
   ```bash
   git clone git@github.com:jimcortez/Atlas-v2-xmodel.git
   cd Atlas-v2-xmodel
   ```

## Configuration

### LED Ring Configuration

Before running the script, you need to configure the LED counts for each ring. Edit the `RINGS` dictionary in `atlasV2Gen.py`:

```python
RINGS = {
    1: 33,   # Ring 1 has 33 LEDs
    2: 55,   # Ring 2 has 55 LEDs
    # ... continue for all 49 rings
    49: 33   # Ring 49 has 33 LEDs
}
```

### Controller Ports

You can adjust the number of controller ports by modifying the `PORTS` constant:

```python
PORTS = 16  # Change this to match your controller
```

### Sphere Parameters

The script uses a virtual sphere radius for coordinate calculations:

```python
self.sphere_radius = 100.0  # Virtual radius for coordinate calculation
```

## Usage

### Basic Usage

Run the main script with default filenames:

```bash
python atlasV2Gen.py
```

This will generate:
- `atlas_v2.xmodel` - The xLights model file with enhanced metadata
- `atlas_v2.csv` - Configuration data with coordinate information
- `atlas_v2_coordinates.json` - Complete 3D coordinate dataset

### Command Line Options

You can specify custom output filenames using command line arguments:

```bash
# Specify custom filenames for all outputs
python atlasV2Gen.py --xmodel my_model.xmodel --csv my_data.csv --json my_coords.json

# Use short options
python atlasV2Gen.py -x my_model.xmodel -c my_data.csv -j my_coords.json

# Generate only specific outputs
python atlasV2Gen.py --xmodel custom.xmodel
python atlasV2Gen.py -c custom.csv
python atlasV2Gen.py -j custom_coords.json
```

### Available Arguments

- `--xmodel`, `-x`: Output filename for xmodel file (default: `atlas_v2.xmodel`)
- `--csv`, `-c`: Output filename for CSV file (default: `atlas_v2.csv`)
- `--json`, `-j`: Output filename for coordinates JSON file (default: `atlas_v2_coordinates.json`)
- `--help`, `-h`: Show help message and exit

### Examples

```bash
# Generate files with descriptive names
python atlasV2Gen.py --xmodel atlas_v2_sphere.xmodel --csv atlas_v2_config.csv --json atlas_v2_3d.json

# Generate only xmodel with custom name
python atlasV2Gen.py -x my_sphere.xmodel

# Generate only CSV with custom name
python atlasV2Gen.py -c my_config.csv

# Generate only JSON coordinates
python atlasV2Gen.py -j my_3d_coords.json
```

## Output Files

### xmodel File
The generated `.xmodel` file includes:
- Standard xLights model data
- Enhanced metadata about the generation method
- Complete coordinate information for each LED
- Pretty-printed XML formatting for readability

### CSV File
The CSV file contains detailed information about each ring including:
- Ring number and LED counts
- LED start/end positions
- Data channel assignments
- Power channel assignments
- Average 3D coordinates for each ring

### JSON File
The JSON file provides:
- Complete model information
- Individual 3D coordinates for every LED
- Ring and position data for each LED
- Structured format for external tools and visualization

## Technical Details

### Coordinate System

The implementation uses a proper spherical coordinate system:
- **Ring Angle (Latitude)**: 0 to π across the sphere (top to bottom)
- **Position Angle (Longitude)**: 0 to 2π within each ring
- **Conversion**: Spherical coordinates converted to Cartesian (x, y, z)

### Group Assignment Algorithm

The new implementation uses dynamic programming for optimal partitioning:
- Minimizes load differences across controller ports
- Provides better balance than the original greedy algorithm
- Ensures optimal distribution of LED counts

### Data Structures

- **LEDPosition**: Dataclass representing individual LED with coordinates
- **AtlasV2GeneratorV2**: Main class encapsulating all functionality
- **Type Hints**: Full type safety throughout the codebase

## Using the xmodel in xLights

Follow these steps to import and configure your Atlas v2 sphere model in xLights:

### 1. Import the Model

1. Open your xLights project
2. Navigate to the **Layout** tab
3. Click **Import** in the model section
4. Select a location in the show layout view
5. In the file picker dialog, select your generated `.xmodel` file

### 2. Configure Controller Settings

1. **Assign Controller**: Select your controller from the dropdown
2. **Starting Pin**: Set the starting pin number for your controller
3. **Number of Strings**: Set this to match your `PORTS` value (default: 16)
4. **Individual Start Nodes**: Check this box to enable custom start positions

### 3. Configure String Start Positions

Using the values from your generated CSV file, set the start position for each string:

1. Look for rows in the CSV where "PC Start" has a value (indicating the start of a new power channel)
2. Use the "LED Start" value from these rows as your string start positions

**Example Configuration:**
- String 1: `1` (LED Start from first PC Start row)
- String 2: `333` (LED Start from second PC Start row)  
- String 3: `765` (LED Start from third PC Start row)
- String 4: `1148` (LED Start from fourth PC Start row)
- ... continue for all strings

### 4. Verify Configuration

1. Check that all strings have the correct start positions
2. Verify the total number of strings matches your `PORTS` setting
3. Test the model by creating a simple effect to ensure all LEDs respond correctly

## Advanced Usage

### Coordinate Data Applications

The JSON coordinate file can be used for:
- 3D visualization tools
- Advanced lighting effects based on spatial relationships
- Integration with 3D modeling software
- Custom effects that depend on LED positions

### Custom Modifications

The object-oriented design makes it easy to extend:
- Modify coordinate calculations for different sphere geometries
- Add new output formats
- Implement custom group assignment algorithms
- Integrate with external visualization tools

## Tips

- Keep your CSV file handy for reference during configuration
- The "PC Start" values in the CSV indicate where each new power channel begins
- Each string should start at the LED position specified in the corresponding "LED Start" column
- The JSON file is useful for advanced applications requiring precise spatial data
- The enhanced XML includes metadata that can help with debugging and analysis

## Project Information

Learn more about the Atlas v2 LED Sphere project: [YouTube Video](https://www.youtube.com/watch?v=l0WGbmc9_4Q)

## Version History

### v2.0 (Current)
- Complete rewrite with coordinate-based positioning
- Enhanced XML generation with metadata
- Dynamic programming for optimal group assignment
- JSON coordinate export
- Object-oriented design with type safety
- Improved CSV output with spatial information

### v1.0 (Original)
- Basic sparse array positioning
- Simple XML generation
- Greedy algorithm for group assignment
- Functional programming approach

