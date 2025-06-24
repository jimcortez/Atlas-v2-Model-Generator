Note: This documentation was generated with the assistance of AI and may contain inaccuracies. Please verify details with official xLights documentation or source code.

# xLights 3D xmodel File Format Specification

This document describes the xLights 3D xmodel file format for custom 3D LED models. This specification is based on analysis of the xLights source code and is intended for developers who need to create 3D xmodel files.

## Overview

The 3D xmodel format extends the standard xmodel format to support true 3D LED layouts. Files have a `.xmodel` extension and contain 3D grid-based LED layout information that xLights uses to render models in 3D space.

## Key Concepts

### 3D Grid Structure
xLights uses a 3D grid system to organize LEDs:
- **Grid dimensions**: width × height × depth
- **Each grid position**: Can contain a node number (LED) or be empty (-1)
- **Rendering**: xLights renders each node at its calculated 3D coordinates

### Coordinate System
xLights uses a 3D coordinate system where:
- **X-axis**: Horizontal position (left/right)
- **Y-axis**: Vertical position (up/down) 
- **Z-axis**: Depth position (front/back)

### Screen Coordinate Calculation
xLights calculates screen coordinates for rendering using:
```cpp
screenX = col - width/2
screenY = height - row - 1 - height/2
screenZ = depth - layer - 1 - depth/2
```

## File Structure

### XML Declaration
```xml
<?xml version='1.0' encoding='utf-8'?>
```

### Root Element
```xml
<custommodel 
  name="Model Name 3D Grid v2.0" 
  parm1="60" 
  parm2="200" 
  parm3="1" 
  Depth="200" 
  StringType="RGB Nodes" 
  Transparency="0" 
  PixelSize="2" 
  ModelBrightness="0" 
  Antialias="1" 
  StrandNames="" 
  NodeNames="" 
  StartLatitude="" 
  EndLatitude="" 
  Degrees="" 
  CustomModel="..." 
  CustomModelCompressed="..." 
  SourceVersion="2024.13">
</custommodel>
```

## Root Element Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | string | Display name of the model |
| `parm1` | integer | Grid height (number of rows) |
| `parm2` | integer | Grid width (number of columns) |
| `parm3` | integer | Always 1 for 3D models |
| `Depth` | integer | Grid depth (number of layers) |
| `StringType` | string | LED type specification |
| `Transparency` | integer | Transparency level (0-255) |
| `PixelSize` | integer | Size of pixels in preview |
| `ModelBrightness` | integer | Overall model brightness |
| `Antialias` | integer | Antialiasing setting |
| `StrandNames` | string | Comma-separated strand names |
| `NodeNames` | string | Comma-separated node names |
| `StartLatitude` | string | Not used for 3D models |
| `EndLatitude` | string | Not used for 3D models |
| `Degrees` | string | Not used for 3D models |
| `CustomModel` | string | 3D grid layout string |
| `CustomModelCompressed` | string | Compressed 3D grid layout |
| `SourceVersion` | string | xLights version that created the file |

## CustomModel Format

The `CustomModel` attribute contains a 3D grid layout in the format:
```
"layers|rows;cols"
```

### Syntax
- `|` separates layers (Z-axis)
- `;` separates rows (Y-axis)
- `,` separates columns (X-axis)
- Each position contains a node number or is empty

### Example
```
"1,2,3,4,5;6,7,8,9,10;11,12,13,14,15|16,17,18,19,20;21,22,23,24,25;26,27,28,29,30"
```

This represents:
- **Layer 0**: 3 rows × 5 columns with nodes 1-15
- **Layer 1**: 3 rows × 5 columns with nodes 16-30

## CustomModelCompressed Format

The `CustomModelCompressed` attribute contains a more efficient representation:
```
"node,row,col,layer;node,row,col,layer;..."
```

### Syntax
- `node`: LED number (1-based)
- `row`: Y position (0-based)
- `col`: X position (0-based)
- `layer`: Z position (0-based)

### Example
```
"1,0,0,0;2,0,1,0;3,1,0,0;4,1,1,0"
```

This places:
- Node 1 at position (0,0,0)
- Node 2 at position (1,0,0)
- Node 3 at position (0,1,0)
- Node 4 at position (1,1,0)

## Coordinate Mapping

### Grid Position Calculation
To map 3D coordinates to grid positions:
```python
col = int(round((x + radius) * (grid_width - 1) / (2 * radius)))
row = int(round((radius - y) * (grid_height - 1) / (2 * radius)))
layer = int(round((z + radius) * (grid_depth - 1) / (2 * radius)))
```

### Parameters
- `x, y, z`: 3D coordinates of the LED
- `radius`: Sphere radius (typically 100)
- `grid_width, grid_height, grid_depth`: Grid dimensions

### Example
For a 200×60×200 grid with radius 100:
- X coordinate -100 maps to column 0
- X coordinate +100 maps to column 199
- Y coordinate -100 maps to row 59
- Y coordinate +100 maps to row 0
- Z coordinate -100 maps to layer 0
- Z coordinate +100 maps to layer 199

## Implementation Notes

### Grid Size Selection
Choose grid dimensions based on your model:
- **Height**: Should accommodate the number of vertical elements (e.g., 49 rings)
- **Width/Depth**: Should accommodate the largest horizontal elements
- **Resolution**: Larger grids provide better precision but use more memory

### Performance Considerations
- xLights only renders nodes that exist in the grid
- Empty grid positions don't affect performance
- Use `CustomModelCompressed` for sparse models (less than 20% of grid positions filled)

### Coordinate System Notes
- xLights inverts the Y-axis during rendering
- Grid coordinates are 0-based
- Node numbers are 1-based
- Screen coordinates are calculated relative to grid center

## Example: Ring-Based Sphere

For a sphere with 49 rings stacked vertically:

```xml
<custommodel 
  name="Sphere 3D" 
  parm1="60" 
  parm2="200" 
  parm3="1" 
  Depth="200" 
  StringType="RGB Nodes" 
  CustomModel="..." 
  CustomModelCompressed="..." 
  SourceVersion="2024.13">
</custommodel>
```

- **Grid dimensions**: 200×60×200
- **Height (60)**: Accommodates 49 rings + padding
- **Width/Depth (200)**: Accommodates largest rings (159 LEDs)
- **Structure**: Each ring is a horizontal circle at a specific Y position

## References

- [xLights 3D Model Documentation](https://xlights.org/)
- [xLights Custom Model Guide](https://xlights.org/help/custom-model)
- [3D Coordinate Systems](https://en.wikipedia.org/wiki/Spherical_coordinate_system) 

### parm3 Attribute

**Note:** The `parm3` attribute is present in some 3D xmodel files, but it is **not used** by xLights for rendering, grid logic, or coordinate mapping. It can be safely included or omitted for compatibility, but has no effect on how the model is interpreted or displayed. 