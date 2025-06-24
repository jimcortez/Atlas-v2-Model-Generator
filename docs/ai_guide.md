# AI Guide: Atlas v2 LED Sphere Model Generator

This guide provides context for AI systems working with the Atlas v2 LED Sphere Model Generator codebase, including the prompts that led to its creation and guidance for extending it.

## Project Creation Prompts

### Initial Request
The project began with a request to create a Python-based system for generating 3D LED sphere models for xLights and MadMapper, focusing on accurate physical representation and file format compatibility.

### Key Development Prompts

1. **Modular Architecture Request**
   - "Refactor the code into a modular package with a `generators/` directory, YAML config, and factory pattern"
   - Result: Created the current modular structure with base classes and format-specific generators

2. **MadMapper Generator Request**
   - "Implement a MadMapper generator with correct DMX channel numbering and grid projection"
   - Result: Added `MadMapperGenerator` with proper fixture library format support

3. **3D xLights Model Request**
   - "Create a 3D xLights model generator using ring submodels"
   - Result: Implemented `XLights3DGenerator` with spherical distribution and metadata

4. **Ring-Based Structure Request**
   - "Update the generator to create a ring-based structure matching the physical object: 49 rings stacked vertically, each ring a horizontal LED strip"
   - Result: Implemented physical ring-based LED positioning system

5. **Documentation Organization**
   - "Move all the documentation for developers from the readme to a new set of markdown files within the docs folder"
   - Result: Organized documentation into user-facing README and developer guides

## Base Prompts for New Generator Development

### Template for Adding New LED Software Support

```
Create a new generator for [SOFTWARE_NAME] LED sphere models. The generator should:

1. Extend the BaseGenerator class in generators/base_generator.py
2. Implement the required methods:
   - get_format_name() -> str
   - get_file_extension() -> str  
   - generate(output_path: str) -> bool
3. Follow the existing pattern of other generators
4. Include proper error handling and user feedback
5. Generate files compatible with [SOFTWARE_NAME]'s expected format

The generator should use the LED positions calculated by the base class and output files that can be imported into [SOFTWARE_NAME].

Reference the existing generators (xlights_generator.py, madmapper_generator.py, xlights3d_generator.py) for implementation patterns.
```

### Template for File Format Research

```
Research the file format specification for [SOFTWARE_NAME] LED model files. Focus on:

1. File extension and structure
2. Required XML elements or data format
3. LED positioning and numbering conventions
4. Controller/channel mapping requirements
5. Any metadata or configuration attributes needed

Provide specific details about how LED coordinates should be mapped and what attributes are required for successful import into [SOFTWARE_NAME].

Include examples of valid file structures if available.
```

### Template for Coordinate System Implementation

```
Implement coordinate mapping for [SOFTWARE_NAME] in the new generator. Consider:

1. How [SOFTWARE_NAME] expects LED positions (2D grid, 3D space, etc.)
2. Coordinate system conventions (origin, axes orientation)
3. Scaling and positioning requirements
4. Any special formatting needed for the coordinate data

The generator should map the spherical LED positions from the base class to the format expected by [SOFTWARE_NAME].

Reference the coordinate mapping implementations in existing generators for patterns.
```

## AI System Context

### Codebase Architecture

- **Modular Design**: Uses factory pattern with base class and format-specific generators
- **Configuration-Driven**: All settings managed via YAML config file
- **LED Positioning**: Spherical coordinate system with 49 rings, 6119 total LEDs
- **File Output**: Multiple formats supported (xLights 2D/3D, MadMapper, CSV, JSON)

### Key Classes and Patterns

1. **BaseGenerator**: Abstract base class with common LED positioning logic
2. **Format Generators**: Specific implementations for each software format
3. **Generator Factory**: Creates appropriate generators based on format name
4. **LEDPosition**: Dataclass for storing LED coordinate and metadata

### Important Implementation Details

- **Spherical Coordinates**: LEDs positioned using latitude/longitude on a sphere
- **Ring-Based Structure**: 49 rings stacked vertically, each with varying LED counts
- **Controller Mapping**: Dynamic group assignment for multi-port controllers
- **File Formats**: XML-based for xLights, custom XML for MadMapper, CSV for data export

### Common Patterns

1. **Error Handling**: All generators include try/catch with specific error messages
2. **File Generation**: Multiple output files per format (main format + CSV + JSON)
3. **Configuration**: Format-specific settings in config.yaml
4. **User Feedback**: Progress messages and file listing on successful generation

### Extension Points

- **New Generators**: Add to `generators/` directory and register in `__init__.py`
- **Configuration**: Add format-specific settings to config.yaml
- **File Formats**: Implement format-specific file writing methods
- **Coordinate Systems**: Extend coordinate mapping for new software requirements

### Validation Requirements

- **File Format Compliance**: Generated files must import successfully into target software
- **Coordinate Accuracy**: LED positions must match physical sphere layout
- **Controller Compatibility**: DMX/channel mapping must work with real controllers
- **Performance**: Generation should complete quickly for large LED counts

### Testing Considerations

- **File Import**: Test generated files in target software
- **Coordinate Verification**: Validate LED positions match expected sphere layout
- **Controller Testing**: Verify DMX/channel assignments work correctly
- **Error Scenarios**: Test with invalid configurations and missing files

This context should help AI systems understand the codebase structure, implementation patterns, and requirements for extending the generator with new LED software support. 