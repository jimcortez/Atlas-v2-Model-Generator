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
- `atlas_v2.xmodel` - For xLights (2D)
- `atlas_v2_3d.xmodel` - For xLights (3D with ring submodels)
- `atlas_v2.mmfl` - For MadMapper
- `atlas_v2.csv` - String configuration data
- `atlas_v2_coordinates.json` - 3D LED coordinates

### 3. Generate Specific Formats
```bash
python generate_models.py --formats xlights
python generate_models.py --formats xlights3d
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

### Using the 3D xmodel in xLights

The 3D model (`atlas_v2_3d.xmodel`) provides enhanced 3D visualization with ring submodels:

#### 1. Import the 3D Model
- Follow the same import process as the 2D model
- The 3D model will appear with proper 3D positioning in the layout view

#### 2. 3D Model Features
- **Ring Submodels**: Each ring is a separate submodel for better organization
- **3D Coordinates**: All LEDs have proper 3D coordinates for realistic visualization
- **Spherical Distribution**: Rings are positioned to form a true sphere shape
- **Individual Ring Control**: You can select and manipulate individual rings

#### 3. 3D Model Configuration
- The 3D model uses the same controller settings as the 2D model
- Ring spacing and positioning are controlled via the `xlights3d` configuration section
- Each ring maintains its LED numbering and controller assignments

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

# xLights 3D Settings
xlights3d:
  ring_spacing: 2.0      # Spacing between rings in 3D space
  ring_radius: 100.0     # Base radius for ring calculations
  vertical_spacing: 2.0  # Vertical spacing between rings

# Output Settings
output:
  default_prefix: "atlas_v2"
  formats:
    xlights:
      enabled: true
    xlights3d:
      enabled: true
    madmapper:
      enabled: true
```

---

## 🧑‍💻 Developer Documentation

- **[Developer Guide](docs/developer-guide.md)** - Project structure, extending the generator, and advanced usage
- **[AI Guide](docs/ai_guide.md)** - Prompts used to create this codebase and templates for AI-assisted development
- **[Output Format Documentation](docs/output_formats/)** - Detailed specifications for generated file formats (xLights xmodel, xLights 3D xmodel, MadMapper mmfl)

