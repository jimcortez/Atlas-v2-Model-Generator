# Developer Guide: Atlas v2 LED Sphere Model Generator

Welcome, developer! This guide covers the internal structure, extension points, and advanced usage for the Atlas v2 LED Sphere Model Generator.

## Project Structure
```
Atlas-v2-xmodel/
├── config.yaml                # Configuration data
├── generate_models.py         # Main entry point
├── generators/                # Format generators
│   ├── __init__.py           # Generator factory
│   ├── base_generator.py     # Abstract base class
│   ├── xlights_generator.py  # xLights 2D format
│   ├── xlights3d_generator.py # xLights 3D format
│   └── madmapper_generator.py # MadMapper format
└── ... (output files)
```

## Adding New Formats

To add support for a new animation software format:

1. **Create a new generator class** in `generators/`:
```python
from .base_generator import BaseGenerator

class NewFormatGenerator(BaseGenerator):
    def get_format_name(self) -> str:
        return "NewFormat"
    
    def get_file_extension(self) -> str:
        return ".new"
    
    def generate(self, output_path: str) -> bool:
        # Implementation here
        pass
```

2. **Register the generator** in `generators/__init__.py`:
```python
from .new_format_generator import NewFormatGenerator

_generators = {
    'xlights': XLightsGenerator,
    'madmapper': MadMapperGenerator,
    'xlights3d': XLights3DGenerator,
    'newformat': NewFormatGenerator,  # Add this line
}
```

3. **Add configuration** in `config.yaml`:
```yaml
output:
  formats:
    newformat:
      enabled: true
      extension: ".new"
      filename: "atlas_v2.new"
```

## Available Commands

```bash
# List all available formats
python generate_models.py --list-formats

# Generate specific formats
python generate_models.py --formats xlights madmapper

# Use custom configuration file
python generate_models.py --config custom_config.yaml

# Specify output directory and prefix
python generate_models.py --output-dir ./models --prefix my_sphere
```

## Architecture

The system uses a **modular generator pattern**:

- **BaseGenerator**: Abstract base class with common LED positioning logic
- **Format Generators**: Specific implementations for each software format
- **Generator Factory**: Creates appropriate generators based on format name
- **YAML Configuration**: Centralized configuration for all settings
- **Command Line Interface**: Flexible CLI for different use cases

## Output Files

| Format | File Extension | Description |
|--------|---------------|-------------|
| xLights 2D | `.xmodel` | Standard xLights model file |
| xLights 3D | `_3d.xmodel` | 3D xLights model with ring submodels |
| MadMapper | `.mmfl` | MadMapper fixture library file |
| CSV | `.csv` | String configuration data |
| JSON | `_coordinates.json` | 3D LED coordinates for visualization | 