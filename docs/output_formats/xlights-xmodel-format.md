Note: This documentation was generated with the assistance of AI and may contain inaccuracies. Please verify details with official xLights documentation or source code.

# xLights xmodel File Format Specification

This document describes the xLights xmodel file format for custom LED models. This specification is intended for developers who need to read, write, or understand xmodel files.

## File Overview

The xmodel format is an XML-based file format used by xLights to define custom LED models. Files have a `.xmodel` extension and contain LED layout information, coordinate data, and model metadata.

## File Structure

### XML Declaration
```xml
<?xml version='1.0' encoding='utf-8'?>
```

### Root Element
```xml
<custommodel name="Model Name" parm1="1000" parm2="49" Depth="1" StringType="GRB Nodes" Transparency="0" PixelSize="2" ModelBrightness="0" Antialias="1" StrandNames="" NodeNames="" CustomModel="..." SourceVersion="2023.20">
  <!-- Child elements -->
</custommodel>
```

## Root Element Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Display name of the model |
| `parm1` | integer | Yes | Maximum number of LEDs per string |
| `parm2` | integer | Yes | Number of strings in the model |
| `Depth` | integer | Yes | Model depth (1 for 2D models) |
| `StringType` | string | Yes | LED type specification |
| `Transparency` | integer | Yes | Transparency level (0-255) |
| `PixelSize` | integer | Yes | Size of pixels in preview |
| `ModelBrightness` | integer | Yes | Overall model brightness |
| `Antialias` | integer | Yes | Antialiasing setting |
| `StrandNames` | string | Yes | Comma-separated strand names |
| `NodeNames` | string | Yes | Comma-separated node names |
| `CustomModel` | string | Yes | LED layout string (see below) |
| `SourceVersion` | string | Yes | xLights version that created the file |

## CustomModel String Format

The `CustomModel` attribute contains the LED layout as a semicolon-separated string. Each semicolon-separated section represents one string (vertical line) of LEDs.

### Syntax
```
"string1;string2;string3;..."
```

Where each string is:
```
"led1,led2,led3,...,ledN"
```

### String Format Rules

- **Semicolons (`;`)** separate different strings
- **Commas (`,`)** separate LED positions within each string
- **Numbers** represent LED indices (1-based)
- **Empty positions** are represented by consecutive commas
- **String count** must equal the `parm2` attribute value

### Examples

**Simple 2-string model:**
```
"1,2,3,4,5;6,7,8,9,10"
```

**String with gaps:**
```
"1,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,2,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,3"
```

**Empty string:**
```
"1,2,3,4,5;;;;"
```

## Child Elements

### metadata Element
```xml
<metadata generator="GeneratorName" method="method-name" total_leds="6119" ports="16" />
```

| Attribute | Type | Description |
|-----------|------|-------------|
| `generator` | string | Name of the generator that created the file |
| `method` | string | Generation method used |
| `total_leds` | integer | Total number of LEDs in the model |
| `ports` | integer | Number of controller ports |

### coordinates Element
Contains individual LED coordinate data for debugging and visualization.

```xml
<coordinates>
  <led number="1" ring="1" position="0" x="0.00" y="0.00" z="100.00" />
  <led number="2" ring="1" position="1" x="10.00" y="5.00" z="95.00" />
  <!-- ... more LED coordinates ... -->
</coordinates>
```

#### led Element Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `number` | integer | LED index (1-based) |
| `ring` | integer | Ring number the LED belongs to |
| `position` | integer | Position within the ring (0-based) |
| `x` | float | X coordinate in 3D space |
| `y` | float | Y coordinate in 3D space |
| `z` | float | Z coordinate in 3D space |

## Coordinate System

xLights uses a right-handed coordinate system:

- **X-axis**: Left to right (negative to positive)
- **Y-axis**: Bottom to top (negative to positive)  
- **Z-axis**: Back to front (negative to positive)

### Typical Coordinate Ranges

- **Radius**: 100 units (typical for spherical models)
- **X, Y, Z**: -100 to +100 (for radius 100 models)

## File Validation Rules

1. **String Count**: Number of semicolon-separated strings must equal `parm2`
2. **LED Indices**: Must be 1-based and sequential
3. **String Length**: Each string cannot exceed `parm1` positions
4. **XML Well-formed**: Must be valid XML
5. **Required Attributes**: All root element attributes are required

## Common StringType Values

| Value | Description |
|-------|-------------|
| `"GRB Nodes"` | RGB LEDs with Green-Red-Blue order |
| `"RGB Nodes"` | RGB LEDs with Red-Green-Blue order |
| `"Single Color"` | Single color LEDs |
| `"4 Channel"` | 4-channel LEDs (RGBW) |

## File Examples

### Minimal Valid xmodel
```xml
<?xml version='1.0' encoding='utf-8'?>
<custommodel name="Test Model" parm1="10" parm2="2" Depth="1" StringType="GRB Nodes" Transparency="0" PixelSize="2" ModelBrightness="0" Antialias="1" StrandNames="" NodeNames="" CustomModel="1,2,3;4,5,6" SourceVersion="2023.20">
  <metadata generator="TestGenerator" method="test" total_leds="6" ports="1" />
</custommodel>
```

### Complete xmodel with Coordinates
```xml
<?xml version='1.0' encoding='utf-8'?>
<custommodel name="Atlas v2 v2.0" parm1="1000" parm2="49" Depth="1" StringType="GRB Nodes" Transparency="0" PixelSize="2" ModelBrightness="0" Antialias="1" StrandNames="" NodeNames="" CustomModel="1,2,3,4,5;6,7,8,9,10;..." SourceVersion="2023.20">
  <metadata generator="AtlasV2Generator" method="coordinate-based" total_leds="6119" ports="16" />
  <coordinates>
    <led number="1" ring="1" position="0" x="0.00" y="0.00" z="100.00" />
    <led number="2" ring="1" position="1" x="10.00" y="5.00" z="95.00" />
  </coordinates>
</custommodel>
```

## References

- [xLights Documentation](https://xlights.org/)
- [xLights Custom Model Guide](https://xlights.org/help/custom-model) 