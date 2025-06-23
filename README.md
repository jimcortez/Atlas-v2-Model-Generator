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

### Tips

- Keep your CSV file handy for reference during configuration
- The "PC Start" values in the CSV indicate where each new power channel begins
- Each string should start at the LED position specified in the corresponding "LED Start" column

## Project Information

Learn more about the Atlas v2 LED Sphere project: [YouTube Video](https://www.youtube.com/watch?v=l0WGbmc9_4Q)

