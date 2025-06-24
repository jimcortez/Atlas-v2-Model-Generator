Note: This documentation was generated with the assistance of AI and may contain inaccuracies. Please verify details with official documentation for each file format.

# File Format Specifications

This document provides an overview of the file formats used in the Atlas v2 LED sphere model generator and links to detailed specifications for each format.

## Overview

The Atlas v2 LED sphere model generator produces three main file formats:

1. **xLights xmodel** - Standard 2D LED model format for xLights
2. **xLights 3D xmodel** - Extended 3D LED model format for xLights
3. **MadMapper mmfl** - LED fixture definition format for MadMapper

## File Format Specifications

### [xLights xmodel Format](xlights-xmodel-format.md)
Standard XML-based format for defining 2D LED models in xLights. Supports coordinate-based layouts with spherical LED positioning.

**File Extension:** `.xmodel`

**Key Features:**
- 2D grid-based layout
- Spherical coordinate system
- CustomModel string format
- Metadata and coordinate tracking

### [xLights 3D xmodel Format](xlights-3d-xmodel-format.md)
Extended format for true 3D LED models in xLights. Creates vertical strings that form 3D volumetric arrangements.

**File Extension:** `.xmodel`

**Key Features:**
- 3D grid system (width × height × depth)
- Vertical string layout
- Spherical to grid coordinate mapping
- Optimized string creation

### [MadMapper mmfl Format](madmapper-mmfl-format.md)
XML-based fixture definition format for MadMapper LED installations. Enables precise pixel mapping and DMX channel assignment.

**File Extension:** `.mmfl`

**Key Features:**
- Individual pixel positioning
- DMX channel assignment (RGB per pixel)
- 3D coordinate system
- Grid projection support

## Format Comparison

| Aspect | xLights xmodel | xLights 3D xmodel | MadMapper mmfl |
|--------|----------------|-------------------|----------------|
| **Purpose** | 2D LED models | 3D LED models | LED fixture definition |
| **Layout** | 2D grid | 3D grid | 3D coordinates |
| **Strings** | Horizontal | Vertical | Individual pixels |
| **Coordinates** | Spherical | Spherical + Grid | Spherical |
| **Channels** | Not specified | Not specified | DMX RGB channels |
| **Software** | xLights | xLights | MadMapper |

## Coordinate Systems

All formats use a right-handed coordinate system:

- **X-axis**: Left to right (negative to positive)
- **Y-axis**: Bottom to top (negative to positive)
- **Z-axis**: Back to front (negative to positive)

### Typical Coordinate Ranges

- **Radius**: 100 units (typical for spherical models)
- **X, Y, Z**: -100 to +100 (for radius 100 models)

## File Validation

Each format has specific validation rules:

- **XML Well-formed**: All files must be valid XML
- **Required Elements**: Each format has mandatory elements and attributes
- **Data Consistency**: Internal references must be consistent
- **Coordinate Bounds**: Coordinates must be within expected ranges

## Usage Guidelines

### Choosing a Format

- **xLights xmodel**: For standard 2D LED displays in xLights
- **xLights 3D xmodel**: For true 3D LED installations in xLights
- **MadMapper mmfl**: For projection mapping and LED installations in MadMapper

### Software Compatibility

| Software | Supported Formats |
|----------|-------------------|
| xLights | xmodel, 3D xmodel |
| MadMapper | mmfl |
| QLC+ | mmfl (with conversion) |
| GrandMA | mmfl (with conversion) |

## References

- [xLights Documentation](https://xlights.org/)
- [MadMapper Documentation](https://madmapper.com/support/)
- [DMX Protocol Specification](https://en.wikipedia.org/wiki/DMX512) 