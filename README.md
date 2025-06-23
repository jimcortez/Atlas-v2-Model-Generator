# Atlas v2 LED Sphere - Modular Model Generator

A modular Python tool to generate LED sphere models for xLights and MadMapper animation software. All configuration is managed via a single YAML file.

---

## 🚀 Quick Start (For Users)

### 1. Install Requirements
```bash
pip install PyYAML
```

### 2. Generate Models
```bash
python generate_models.py
```

This generates all enabled formats from `config.yaml`. By default, you'll get:
- `atlas_v2.xmodel` - For xLights
- `atlas_v2.mmfl` - For MadMapper
- `atlas_v2.csv` - String configuration data
- `atlas_v2_coordinates.json` - 3D LED coordinates

### 3. Generate Specific Formats
```bash
python generate_models.py --formats xlights
python generate_models.py --formats madmapper
```

### 4. Custom Output
```bash
python generate_models.py --output-dir ./models --prefix my_sphere
```

---

## 📋 Usage Guide

### Using the xmodel in xLights

Follow these steps to import and configure your Atlas v2 sphere model in xLights:

#### 1. Import the Model
- Open your xLights project
- Navigate to the Layout tab
- Click Import in the model section
- Select a location in the show layout view
- In the file picker dialog, select your generated `.xmodel` file

#### 2. Configure Controller Settings
- **Assign Controller**: Select your controller from the dropdown
- **Starting Pin**: Set the starting pin number for your controller
- **Number of Strings**: Set this to match your PORTS value (default: 16)
- **Individual Start Nodes**: Check this box to enable custom start positions

#### 3. Configure String Start Positions
Using the values from your generated CSV file, set the start position for each string:

- Look for rows in the CSV where "PC Start" has a value (indicating the start of a new power channel)
- Use the "LED Start" value from these rows as your string start positions

**Example Configuration:**
- String 1: 1 (LED Start from first PC Start row)
- String 2: 333 (LED Start from second PC Start row)
- String 3: 765 (LED Start from third PC Start row)
- String 4: 1148 (LED Start from fourth PC Start row)
- ... continue for all strings

#### 4. Verify Configuration
- Check that all strings have the correct start positions
- Verify the total number of strings matches your PORTS setting
- Test the model by creating a simple effect to ensure all LEDs respond correctly

### Using the mmfl in MadMapper

1. Open MadMapper and go to the **LED Fixture Library**
2. Click **Import** and select your `.mmfl` file
3. The fixture will be available with proper DMX channel mapping
4. The grid projection uses the `grid_resolution` setting from your config

---

## ⚙️ Configuration

Edit `config.yaml` to customize your model:

```yaml
model:
  name: "Atlas v2"
  version: "2.0"
  description: "LED Sphere by DrZzs & GrZzs"

# LED Ring Configuration (49 rings, 6119 total LEDs)
rings:
  1: 33
  2: 55
  # ... (see config.yaml for full list)
  49: 33

# Controller Settings
controller:
  ports: 16
  total_size: 1000

# Geometry Settings
geometry:
  sphere_radius: 100.0
  coordinate_system: "spherical"

# MadMapper Settings
madmapper:
  grid_resolution: 100  # Grid size for projection
  dmx_start_channel: 1  # Starting DMX channel

# Output Settings
output:
  default_prefix: "atlas_v2"
  formats:
    xlights:
      enabled: true
    madmapper:
      enabled: true
```

---

## 🛠️ Developer Information

### Project Structure
```
Atlas-v2-xmodel/
├── config.yaml                # Configuration data
├── generate_models.py         # Main entry point
├── generators/                # Format generators
│   ├── __init__.py           # Generator factory
│   ├── base_generator.py     # Abstract base class
│   ├── xlights_generator.py  # xLights format
│   └── madmapper_generator.py # MadMapper format
└── ... (output files)
```

### Adding New Formats

1. **Create Generator Class**
   ```python
   # generators/myformat_generator.py
   from .base_generator import BaseGenerator
   
   class MyFormatGenerator(BaseGenerator):
       def get_format_name(self) -> str:
           return "MyFormat"
       
       def get_file_extension(self) -> str:
           return ".myf"
       
       def generate(self, output_path: str) -> bool:
           # Your generation logic here
           pass
   ```

2. **Register in Factory**
   ```python
   # generators/__init__.py
   from .myformat_generator import MyFormatGenerator
   
   _generators = {
       'xlights': XLightsGenerator,
       'madmapper': MadMapperGenerator,
       'myformat': MyFormatGenerator,  # Add this line
   }
   ```

3. **Add to Config**
   ```yaml
   # config.yaml
   output:
     formats:
       myformat:
         enabled: true
         extension: ".myf"
         filename: "atlas_v2.myf"
   ```

### Available Commands

```bash
# List available formats
python generate_models.py --list-formats

# Generate with custom settings
python generate_models.py --formats xlights,madmapper --output-dir ./output --prefix custom
```

### Architecture

- **BaseGenerator**: Abstract base class with common LED positioning logic
- **GeneratorFactory**: Factory pattern for creating format-specific generators
- **YAML Configuration**: Centralized configuration for all settings
- **Modular Design**: Easy to add new formats without modifying existing code

---

## 📁 Output Files

| Format | Extension | Description |
|--------|-----------|-------------|
| xLights | `.xmodel` | xLights model file for Layout tab |
| MadMapper | `.mmfl` | MadMapper LED fixture library file |
| CSV | `.csv` | String configuration and group assignments |
| JSON | `.json` | 3D coordinates for all LEDs |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your new format generator
4. Update documentation
5. Submit a pull request

---

## 📄 License & Credits

- Based on the work of https://github.com/kraegar/Atlas-v2-xmodel
- Modular rewrite with support for multiple animation software platforms

