Note: This documentation was generated with the assistance of AI and may contain inaccuracies. Please verify details with official MadMapper documentation.

# MadMapper mmfl File Format Specification

This document describes the MadMapper mmfl (MadMapper Fixture Library) file format for LED fixture definitions. This specification is intended for developers who need to read, write, or understand mmfl files.

## File Overview

The mmfl format is an XML-based file format used by MadMapper to define LED fixtures and their pixel mapping. Files have a `.mmfl` extension and contain fixture metadata, pixel positioning data, and DMX channel assignments.

## File Structure

### XML Declaration
```xml
<?xml version="1.0" encoding="UTF-8"?>
```

### Root Element
```xml
<fixture>
  <name>Fixture Name</name>
  <type>led</type>
  <manufacturer>Manufacturer Name</manufacturer>
  <model>Model Name</model>
  <version>Version Number</version>
  <pixels>
    <!-- Pixel elements -->
  </pixels>
  <metadata>
    <!-- Metadata elements -->
  </metadata>
</fixture>
```

## Root Element Attributes

The `<fixture>` element is the root container and has no attributes.

## Child Elements

### name Element
```xml
<name>Atlas v2 LED Sphere</name>
```

| Type | Required | Description |
|------|----------|-------------|
| string | Yes | Display name of the fixture |

### type Element
```xml
<type>led</type>
```

| Type | Required | Description |
|------|----------|-------------|
| string | Yes | Fixture type specification |

#### Supported Types

| Value | Description |
|-------|-------------|
| `"led"` | Standard LED fixture with individual pixel control |
| `"rgb"` | RGB LED fixture (deprecated, use `led`) |
| `"dimmer"` | Simple dimmer fixture |

### manufacturer Element
```xml
<manufacturer>Custom</manufacturer>
```

| Type | Required | Description |
|------|----------|-------------|
| string | Yes | Manufacturer name |

### model Element
```xml
<model>Atlas v2</model>
```

| Type | Required | Description |
|------|----------|-------------|
| string | Yes | Model name |

### version Element
```xml
<version>2.0</version>
```

| Type | Required | Description |
|------|----------|-------------|
| string | Yes | Version number |

### pixels Element
Contains individual pixel definitions.

```xml
<pixels>
  <pixel id="1" x="0.00" y="0.00" z="100.00" dmx="1" />
  <pixel id="2" x="10.00" y="5.00" z="95.00" dmx="4" />
  <!-- ... more pixels ... -->
</pixels>
```

#### pixel Element Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | Unique pixel identifier (1-based) |
| `x` | float | Yes | X coordinate in 3D space |
| `y` | float | Yes | Y coordinate in 3D space |
| `z` | float | Yes | Z coordinate in 3D space |
| `dmx` | integer | Yes | Starting DMX channel for this pixel |

### metadata Element
Contains generation and fixture information.

```xml
<metadata>
  <generator>MadMapperGenerator</generator>
  <method>spherical-coordinates</method>
  <total_pixels>6119</total_pixels>
  <ports>16</ports>
  <rings>49</rings>
  <radius>100.0</radius>
</metadata>
```

#### metadata Child Elements

| Element | Type | Required | Description |
|---------|------|----------|-------------|
| `generator` | string | No | Name of the generator that created the file |
| `method` | string | No | Generation method used |
| `total_pixels` | integer | No | Total number of pixels in the fixture |
| `ports` | integer | No | Number of controller ports |
| `rings` | integer | No | Number of LED rings |
| `radius` | float | No | Sphere radius in units |

## Coordinate System

MadMapper uses a right-handed coordinate system:

- **X-axis**: Left to right (negative to positive)
- **Y-axis**: Bottom to top (negative to positive)
- **Z-axis**: Back to front (negative to positive)

### Typical Coordinate Ranges

- **Radius**: 100 units (typical for spherical models)
- **X, Y, Z**: -100 to +100 (for radius 100 models)

## DMX Channel Assignment

### Channel Calculation

Each pixel requires 3 DMX channels (RGB):

```
base_channel = (pixel_id - 1) * 3 + 1
red_channel = base_channel
green_channel = base_channel + 1
blue_channel = base_channel + 2
```

### Channel Ranges

| Component | Channel Offset | Value Range |
|-----------|----------------|-------------|
| Red | +0 | 0-255 |
| Green | +1 | 0-255 |
| Blue | +2 | 0-255 |

### Example Channel Assignment

```
Pixel 1: DMX 1-3 (Red=1, Green=2, Blue=3)
Pixel 2: DMX 4-6 (Red=4, Green=5, Blue=6)
Pixel 3: DMX 7-9 (Red=7, Green=8, Blue=9)
```

### Port Distribution

For multi-port controllers, channels are distributed across ports:

```
port = (base_channel - 1) // 512 + 1
port_channel = ((base_channel - 1) % 512) + 1
```

## File Validation Rules

1. **Pixel IDs**: Must be 1-based and unique
2. **DMX Channels**: Must be sequential and non-overlapping
3. **Coordinates**: Must be valid floating-point numbers
4. **XML Well-formed**: Must be valid XML
5. **Required Elements**: name, type, manufacturer, model, version, pixels are required

## Layout Interpretation

### Grid Projection

MadMapper interprets pixel positions for grid projection:

1. **Calculate bounding box** of all pixel positions
2. **Normalize coordinates** to 0-1 range
3. **Map to grid** for projection mapping
4. **Apply transformations** (scale, rotate, translate)

### Normalization Formula

```
norm_x = (pixel.x - min_x) / (max_x - min_x)
norm_y = (pixel.y - min_y) / (max_y - min_y)
```

### Spherical Projection

For spherical fixtures, MadMapper can apply spherical projection:

1. **Calculate spherical coordinates** from 3D positions
2. **Map to 2D projection** (equirectangular, mercator, etc.)
3. **Apply texture mapping** for video content

## File Examples

### Minimal Valid mmfl
```xml
<?xml version="1.0" encoding="UTF-8"?>
<fixture>
  <name>Test Fixture</name>
  <type>led</type>
  <manufacturer>Test</manufacturer>
  <model>Test Model</model>
  <version>1.0</version>
  <pixels>
    <pixel id="1" x="0.00" y="0.00" z="100.00" dmx="1" />
    <pixel id="2" x="10.00" y="5.00" z="95.00" dmx="4" />
  </pixels>
</fixture>
```

### Complete mmfl with Metadata
```xml
<?xml version="1.0" encoding="UTF-8"?>
<fixture>
  <name>Atlas v2 LED Sphere</name>
  <type>led</type>
  <manufacturer>Custom</manufacturer>
  <model>Atlas v2</model>
  <version>2.0</version>
  <pixels>
    <pixel id="1" x="0.00" y="0.00" z="100.00" dmx="1" />
    <pixel id="2" x="10.00" y="5.00" z="95.00" dmx="4" />
    <pixel id="3" x="20.00" y="10.00" z="90.00" dmx="7" />
  </pixels>
  <metadata>
    <generator>MadMapperGenerator</generator>
    <method>spherical-coordinates</method>
    <total_pixels>6119</total_pixels>
    <ports>16</ports>
    <rings>49</rings>
    <radius>100.0</radius>
  </metadata>
</fixture>
```

## MadMapper Integration

### Import Process

1. **Load mmfl file** in MadMapper
2. **Verify pixel positions** in 3D view
3. **Configure DMX output** settings
4. **Set up grid projection** if needed
5. **Test pixel control** with test patterns

### Grid Setup

1. **Create grid** matching fixture dimensions
2. **Map fixture to grid** using pixel positions
3. **Apply content** to grid
4. **Fine-tune mapping** using MadMapper tools

## References

- [MadMapper Documentation](https://madmapper.com/support/)
- [DMX Protocol Specification](https://en.wikipedia.org/wiki/DMX512)
- [Spherical Coordinate System](https://en.wikipedia.org/wiki/Spherical_coordinate_system) 