# Atlas v2 LED Sphere - Modular Model Generator

A modular Python tool to generate LED sphere models for xLights, MadMapper, and Chromatik animation software. All configuration is managed via a single YAML file.

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
- `atlas_v2.xmodel` - For xLights (2D grid layout)
- `atlas_v2.csv` - String configuration data for xLights
- `atlas_v2_3d.xmodel` - For xLights (3D with ring submodels)
- `atlas_v2_3d.csv` - 3D string configuration data
- `atlas_v2_3d_coordinates.json` - 3D LED coordinates
- `atlas_v2_coordinates.json` - 2D LED coordinates
- `atlas_v2.mmfl` - For MadMapper
- `atlas_v2.lxf` - For Chromatik

### 3. Generate Specific Formats
```bash
python generate_models.py --formats xlights
python generate_models.py --formats xlights3d
python generate_models.py --formats madmapper
python generate_models.py --formats chromatik
```

### 4. List Available Formats
```bash
python generate_models.py --list-formats
```

### 5. Custom Output
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

### Using the lxf in Chromatik

1. Copy the generated `.lxf` file to the Chromatik fixtures directory:
   - **macOS**: `~/Chromatik/Fixtures/`
   - **Windows**: `%USERPROFILE%\Chromatik\Fixtures\`
   - **Linux**: `~/Chromatik/Fixtures/`
2. Open Chromatik and navigate to the **FIXTURES** section on the left-pane **MODEL** tab
3. The fixture will appear in the **Fixture Chooser** arranged by subdirectory name
4. The fixture uses arc components for each ring with proper 3D positioning
5. ArtNet output is configured with segmented structure matching your controller ports
6. Configure ArtNet settings (host, universe) in the fixture parameters if needed

**Note**: The fixture uses arc components representing each ring as a 360-degree arc at its proper latitude on the sphere. Each ring is positioned correctly in 3D space to form the complete sphere shape.

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

# Chromatik Settings
chromatik:
  artnet_host: "127.0.0.1"  # ArtNet destination IP address
  artnet_start_universe: 0  # Starting ArtNet universe number
  dmx_start_channel: 1      # Starting DMX channel for the first LED

# xLights 3D Settings
xlights3d:
  grid_width: 50       # Width of each 2D slice
  grid_height: 50      # Height of each 2D slice
  grid_depth: 50       # Number of z-layers (depth)
  sphere_radius: 100.0 # Radius for coordinate mapping

# Output Settings
output:
  default_prefix: "atlas_v2"
  formats:
    xlights:
      enabled: true
      extension: ".xmodel"
      filename: "atlas_v2.xmodel"
    xlights3d:
      enabled: true
      extension: "_3d.xmodel"
      filename: "atlas_v2_3d.xmodel"
    madmapper:
      enabled: true
      extension: ".mmfl"
      filename: "atlas_v2.mmfl"
    chromatik:
      enabled: true
      extension: ".lxf"
      filename: "atlas_v2.lxf"
```

---

## 🧑‍💻 Developer Documentation

- **[Developer Guide](docs/developer-guide.md)** - Project structure, extending the generator, and advanced usage
- **[AI Guide](docs/ai_guide.md)** - Prompts used to create this codebase and templates for AI-assisted development
- **[Output Format Documentation](docs/output_formats/)** - Detailed specifications for generated file formats:
  - [xLights xmodel format](docs/output_formats/xlights-xmodel-format.md) - 2D custom model format
  - [xLights 3D xmodel format](docs/output_formats/xlights-3d-xmodel-format.md) - 3D custom model format
  - [MadMapper mmfl format](docs/output_formats/madmapper-mmfl-format.md) - LED fixture library format
  - [File formats overview](docs/output_formats/file-formats.md) - General format information
  - [Chromatik lxf format](https://chromatik.co/guide/custom-fixtures/) - Custom fixture format (external documentation)

---

## 📁 Generated Files

The generator creates the following files:

### xLights Format (`xlights`)
- `{prefix}.xmodel` - 2D custom model for xLights
- `{prefix}.csv` - String configuration data

### xLights 3D Format (`xlights3d`)
- `{prefix}_3d.xmodel` - 3D custom model with ring submodels
- `{prefix}_3d.csv` - 3D string configuration data
- `{prefix}_3d_coordinates.json` - 3D LED coordinates
- `{prefix}_3d_rings.csv` - Ring configuration data

### MadMapper Format (`madmapper`)
- `{prefix}.mmfl` - LED fixture library file

### Chromatik Format (`chromatik`)
- `{prefix}.lxf` - Custom fixture file with arc components for each ring

### Additional Files
- `{prefix}_coordinates.json` - 2D LED coordinates (generated by xLights format)

---

## 🔧 Command Line Options

```bash
python generate_models.py [OPTIONS]

Options:
  -h, --help            Show help message and exit
  -c, --config CONFIG   Path to configuration file (default: config.yaml)
  -o, --output-dir DIR  Output directory for generated files (default: current directory)
  -f, --formats FORMATS Specific formats to generate (xlights, xlights3d, madmapper, chromatik)
  -p, --prefix PREFIX   Output filename prefix (default: from config)
  --list-formats        List available formats and exit
```

