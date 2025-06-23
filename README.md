# Atlas v2 LED Sphere - xLights Model Generator

A Python script to generate xLights model files and CSV configuration for the Atlas v2 LED Sphere by DrZzs & GrZzs.

This code is based on the work of https://github.com/kraegar/Atlas-v2-xmodel

## Overview

This tool creates:
- An `.xmodel` file that can be imported into xLights
- A CSV file with ring and group assignment information

## Prerequisites

- Python 3.6 or higher
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

## Usage

### Basic Usage

Run the main script with default filenames:

```bash
python atlasV2Gen.py
```

This will generate:
- `atlas_v2.xmodel` - The xLights model file
- `atlas_v2.csv` - Configuration data for ring assignments

### Command Line Options

You can specify custom output filenames using command line arguments:

```bash
# Specify custom filenames
python atlasV2Gen.py --xmodel my_model.xmodel --csv my_data.csv

# Use short options
python atlasV2Gen.py -x my_model.xmodel -c my_data.csv

# Mix and match
python atlasV2Gen.py --xmodel custom.xmodel -c custom.csv
```

### Available Arguments

- `--xmodel`, `-x`: Output filename for xmodel file (default: `atlas_v2.xmodel`)
- `--csv`, `-c`: Output filename for CSV file (default: `atlas_v2.csv`)
- `--help`, `-h`: Show help message and exit

### Examples

```bash
# Generate files with descriptive names
python atlasV2Gen.py --xmodel atlas_v2_sphere.xmodel --csv atlas_v2_config.csv

# Generate only xmodel with custom name
python atlasV2Gen.py -x my_sphere.xmodel

# Generate only CSV with custom name
python atlasV2Gen.py -c my_config.csv
```

## Output Files

### xmodel File
The generated `.xmodel` file can be imported directly into xLights to create your Atlas v2 sphere model.

### CSV File
The CSV file contains detailed information about each ring including:
- Ring number
- LED start/end positions
- Data channel assignments
- Power channel assignments

## Project Information

Learn more about the Atlas v2 LED Sphere project: [YouTube Video](https://www.youtube.com/watch?v=l0WGbmc9_4Q)

