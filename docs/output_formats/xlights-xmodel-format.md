Note: This documentation was generated with the assistance of AI and may contain inaccuracies. Please verify details with official xLights documentation or source code.

# xLights Custom Model XML File Format Documentation

## Overview

Custom models in xLights allow users to create arbitrary grid-based lighting layouts by defining the exact position and channel assignment of each node. These models are stored in XML files with the `.xmodel` extension and use the `custommodel` root element.

## File Structure

### Root Element

All custom model files begin with a standard XML declaration and use the `custommodel` root element:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<custommodel name="Model Name" ... attributes ...>
```

## Required Attributes

### Basic Properties
- **`name`** (string) - Display name of the model
- **`parm1`** (integer) - Width of the grid (number of columns)
- **`parm2`** (integer) - Height of the grid (number of rows)
- **`Depth`** (integer) - Number of layers (default: 1)

### Data Storage
- **`CustomModel`** (string) - Human-readable format defining node positions
- **`CustomModelCompressed`** (string) - Optimized format for better performance

## Data Format Specifications

### Human-Readable Format (`CustomModel`)

The `CustomModel` attribute uses a hierarchical format to define node positions across multiple layers:

**Format:** `"layer1|layer2|layer3"`

Where each layer follows the pattern:
**Layer Format:** `"row1;row2;row3"`

Where each row follows the pattern:
**Row Format:** `"node1,node2,node3"`

**Complete Example:**
```
"1,2,3,4,5;6,7,8,9,10;11,12,13,14,15|16,17,18,19,20;21,22,23,24,25"
```

**Parsing Rules:**
- Layers are separated by `|` (pipe character)
- Rows within a layer are separated by `;` (semicolon)
- Columns within a row are separated by `,` (comma)
- Node numbers indicate the channel assignment (1-based)
- Empty positions or zeros indicate no node at that location
- Negative values (-1) indicate empty positions
- Leading/trailing spaces are ignored

### Compressed Format (`CustomModelCompressed`)

The compressed format is more efficient for parsing and storage:

**Format:** `"node,row,col,layer;node,row,col,layer"`

**Example:**
```
"1,0,0,0;2,0,1,0;3,0,2,0;4,0,3,0;5,0,4,0;6,1,0,0;7,1,1,0;8,1,2,0"
```

**Parsing Rules:**
- Each node definition is separated by `;` (semicolon)
- Each node definition contains: `node_number,row_index,col_index,layer_index`
- Indices are 0-based
- Only nodes that exist are included (no empty positions)
- Layer index is optional (defaults to 0 for single-layer models)

## Optional Attributes

### Display Properties
- **`DisplayAs`** (string) - Display type (default: "Custom")
- **`StringType`** (string) - Type of string: "RGB Nodes", "Single Color White", "Single Color Red", etc. (default: "RGB Nodes")
- **`PixelSize`** (integer) - Size of pixels in preview (default: 2)
- **`Transparency`** (integer) - Transparency level 0-100 (default: 0)
- **`ModelBrightness`** (integer) - Brightness adjustment 0-100 (default: 0)
- **`Antialias`** (integer) - Antialiasing setting (default: 1)

### Channel Configuration
- **`StartChannel`** (string) - Starting channel number or expression
- **`PixelCount`** (integer) - Total number of pixels
- **`PixelType`** (string) - Type of pixel configuration
- **`PixelSpacing`** (integer) - Spacing between pixels
- **`LayoutGroup`** (string) - Layout group assignment

### String Configuration
- **`CustomStrings`** (integer) - Number of strings (default: 1, max: 100)

**Individual String Start Channels:**
- **`String1`** (string) - Starting channel for string 1
- **`String2`** (string) - Starting channel for string 2
- **`String3`** (string) - Starting channel for string 3
- ... (continues for each string)

**String Configuration Examples:**

**Single String (Default):**
```xml
<custommodel name="Single String Model" 
             parm1="10" parm2="5" 
             CustomStrings="1"
             CustomModel="1,2,3,4,5,6,7,8,9,10;11,12,13,14,15,16,17,18,19,20;21,22,23,24,25,26,27,28,29,30;31,32,33,34,35,36,37,38,39,40;41,42,43,44,45,46,47,48,49,50">
</custommodel>
```

**Two Strings with Individual Start Channels:**
```xml
<custommodel name="Two String Model" 
             parm1="10" parm2="5" 
             CustomStrings="2"
             String1="1"
             String2="51"
             CustomModel="1,2,3,4,5,6,7,8,9,10;11,12,13,14,15,16,17,18,19,20;21,22,23,24,25,26,27,28,29,30;31,32,33,34,35,36,37,38,39,40;41,42,43,44,45,46,47,48,49,50">
</custommodel>
```

**Three Strings with Complex Channel Assignment:**
```xml
<custommodel name="Three String Model" 
             parm1="12" parm2="8" 
             CustomStrings="3"
             String1="1"
             String2="97"
             String3="193"
             CustomModel="1,2,3,4,5,6,7,8,9,10,11,12;13,14,15,16,17,18,19,20,21,22,23,24;25,26,27,28,29,30,31,32,33,34,35,36;37,38,39,40,41,42,43,44,45,46,47,48;49,50,51,52,53,54,55,56,57,58,59,60;61,62,63,64,65,66,67,68,69,70,71,72;73,74,75,76,77,78,79,80,81,82,83,84;85,86,87,88,89,90,91,92,93,94,95,96">
</custommodel>
```

**Four Strings with Expression-Based Start Channels:**
```xml
<custommodel name="Four String Model" 
             parm1="8" parm2="6" 
             CustomStrings="4"
             String1="1"
             String2="49"
             String3="97"
             String4="145"
             CustomModel="1,2,3,4,5,6,7,8;9,10,11,12,13,14,15,16;17,18,19,20,21,22,23,24;25,26,27,28,29,30,31,32;33,34,35,36,37,38,39,40;41,42,43,44,45,46,47,48">
</custommodel>
```

**Ten Strings with Sequential Channel Assignment:**
```xml
<custommodel name="Ten String Model" 
             parm1="20" parm2="10" 
             CustomStrings="10"
             String1="1"
             String2="201"
             String3="401"
             String4="601"
             String5="801"
             String6="1001"
             String7="1201"
             String8="1401"
             String9="1601"
             String10="1801"
             CustomModel="1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20;21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40;41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60;61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80;81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100;101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120;121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140;141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160;161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180;181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200">
</custommodel>
```

### Background and Styling
- **`CustomBkgImage`** (string) - Background image file path
- **`CustomBkgLightness`** (integer) - Background lightness adjustment

**Background Examples:**

**With Background Image:**
```xml
<custommodel name="Background Image Model" 
             parm1="16" parm2="9" 
             CustomBkgImage="images/background.png"
             CustomBkgLightness="20"
             CustomModel="1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16;17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32;33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48;49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64;65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80;81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96;97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112;113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128;129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144">
</custommodel>
```

**With Lightness Adjustment:**
```xml
<custommodel name="Lightness Adjusted Model" 
             parm1="8" parm2="8" 
             CustomBkgLightness="-15"
             CustomModel="1,2,3,4,5,6,7,8;9,10,11,12,13,14,15,16;17,18,19,20,21,22,23,24;25,26,27,28,29,30,31,32;33,34,35,36,37,38,39,40;41,42,43,44,45,46,47,48;49,50,51,52,53,54,55,56;57,58,59,60,61,62,63,64">
</custommodel>
```

### Metadata
- **`StrandNames`** (string) - Comma-separated strand names
- **`NodeNames`** (string) - Comma-separated node names
- **`SourceVersion`** (string) - Version of xLights that created the model

**Metadata Examples:**

**With Strand Names:**
```xml
<custommodel name="Named Strands Model" 
             parm1="12" parm2="6" 
             StrandNames="Top Row,Middle Row,Bottom Row"
             CustomModel="1,2,3,4,5,6,7,8,9,10,11,12;13,14,15,16,17,18,19,20,21,22,23,24;25,26,27,28,29,30,31,32,33,34,35,36;37,38,39,40,41,42,43,44,45,46,47,48;49,50,51,52,53,54,55,56,57,58,59,60;61,62,63,64,65,66,67,68,69,70,71,72">
</custommodel>
```

**With Node Names:**
```xml
<custommodel name="Named Nodes Model" 
             parm1="5" parm2="5" 
             NodeNames="Top Left,Top Center,Top Right,Middle Left,Middle Center,Middle Right,Bottom Left,Bottom Center,Bottom Right"
             CustomModel="1,2,3,4,5;6,7,8,9,10;11,12,13,14,15;16,17,18,19,20;21,22,23,24,25">
</custommodel>
```

**With Version Information:**
```xml
<custommodel name="Versioned Model" 
             parm1="10" parm2="10" 
             SourceVersion="2024.1"
             CustomModel="1,2,3,4,5,6,7,8,9,10;11,12,13,14,15,16,17,18,19,20;21,22,23,24,25,26,27,28,29,30;31,32,33,34,35,36,37,38,39,40;41,42,43,44,45,46,47,48,49,50;51,52,53,54,55,56,57,58,59,60;61,62,63,64,65,66,67,68,69,70;71,72,73,74,75,76,77,78,79,80;81,82,83,84,85,86,87,88,89,90;91,92,93,94,95,96,97,98,99,100">
</custommodel>
```

## Complete Examples

### Basic Single-Layer Model
```xml
<?xml version="1.0" encoding="UTF-8"?>
<custommodel name="5x3 Custom Grid" 
             parm1="5" 
             parm2="3" 
             Depth="1"
             DisplayAs="Custom"
             StringType="RGB Nodes"
             PixelSize="2"
             Transparency="0"
             ModelBrightness="0"
             Antialias="1"
             CustomStrings="1"
             CustomModel="1,2,3,4,5;6,7,8,9,10;11,12,13,14,15"
             CustomModelCompressed="1,0,0,0;2,0,1,0;3,0,2,0;4,0,3,0;5,0,4,0;6,1,0,0;7,1,1,0;8,1,2,0;9,1,3,0;10,1,4,0;11,2,0,0;12,2,1,0;13,2,2,0;14,2,3,0;15,2,4,0"
             SourceVersion="2024.1">
</custommodel>
```

### Multi-Layer Model
```xml
<?xml version="1.0" encoding="UTF-8"?>
<custommodel name="3D Custom Model" 
             parm1="4" 
             parm2="3" 
             Depth="2"
             DisplayAs="Custom"
             StringType="RGB Nodes"
             CustomStrings="2"
             String1="1"
             String2="13"
             CustomModel="1,2,3,4;5,6,7,8;9,10,11,12|13,14,15,16;17,18,19,20;21,22,23,24"
             CustomModelCompressed="1,0,0,0;2,0,1,0;3,0,2,0;4,0,3,0;5,1,0,0;6,1,1,0;7,1,2,0;8,1,3,0;9,2,0,0;10,2,1,0;11,2,2,0;12,2,3,0;13,0,0,1;14,0,1,1;15,0,2,1;16,0,3,1;17,1,0,1;18,1,1,1;19,1,2,1;20,1,3,1;21,2,0,1;22,2,1,1;23,2,2,1;24,2,3,1"
             SourceVersion="2024.1">
</custommodel>
```

### Complex Multi-String Model
```xml
<?xml version="1.0" encoding="UTF-8"?>
<custommodel name="Complex Multi-String Model" 
             parm1="16" 
             parm2="12" 
             Depth="1"
             DisplayAs="Custom"
             StringType="RGB Nodes"
             PixelSize="3"
             Transparency="10"
             ModelBrightness="5"
             Antialias="1"
             CustomStrings="4"
             String1="1"
             String2="193"
             String3="385"
             String4="577"
             CustomBkgImage="images/stage_background.jpg"
             CustomBkgLightness="15"
             StrandNames="Front Row,Second Row,Third Row,Back Row"
             NodeNames="Front Left,Front Center,Front Right,Back Left,Back Center,Back Right"
             CustomModel="1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16;17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32;33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48;49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64;65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80;81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96;97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112;113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128;129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144;145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160;161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176;177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192"
             SourceVersion="2024.1">
</custommodel>
```

## Common Patterns

### Empty Grid
```
CustomModel=",,,,;,,,,;,,,,"  // 4x3 empty grid
```

### Single Node
```
CustomModel="1"  // 1x1 grid with one node
```

### Row of Nodes
```
CustomModel="1,2,3,4,5"  // 1x5 horizontal line
```

### Column of Nodes
```
CustomModel="1;2;3;4;5"  // 5x1 vertical line
```

### Checkerboard Pattern
```
CustomModel="1,,1,,1;,2,,2,;1,,1,,1;,2,,2,;1,,1,,1"  // 5x5 checkerboard
```

### Spiral Pattern
```
CustomModel="1,2,3,4;12,13,14,5;11,16,15,6;10,9,8,7"  // 4x4 spiral
```

### Cross Pattern
```
CustomModel=",1,;1,1,1;,1,"  // 3x3 cross
```

## Validation Rules

1. **Grid Dimensions**: `parm1` and `parm2` must be positive integers
2. **Depth**: Must be at least 1
3. **Node Numbers**: Should be positive integers (1-based channel assignment)
4. **Data Consistency**: Both `CustomModel` and `CustomModelCompressed` should represent the same layout
5. **String Count**: `CustomStrings` must be at least 1 and not exceed 100
6. **String Attributes**: If `CustomStrings` > 1, each string should have a corresponding `StringN` attribute

## Error Handling

- **Invalid XML**: Results in loading failure
- **Missing Attributes**: Use sensible defaults
- **Invalid Data Format**: Graceful fallback with error logging
- **Dimension Mismatch**: Automatic padding or truncation
- **Parse Errors**: Invalid numbers are treated as 0 (empty position)
- **Missing String Attributes**: Default to sequential channel assignment 