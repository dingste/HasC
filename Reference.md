# HasC: Reference Guide

This document provides a detailed reference for the HasC project, explaining the core concepts, data structures, and workflow.

## Core Philosophy

HasC promotes a declarative approach to hardware design, defining circuits and layouts through text-based YAML files.  The key principle is to avoid redundancy by declaring information in a single, logical location. Moreover take concepts like derivation or similar with. This approach allows for:

*   **Improved Maintainability:**  Easier to understand and modify designs.
*   **Enhanced Scalability:**  Manage complex projects with a well-defined structure.
*   **Increased Automation:**  Automate design processes and integrate with CI/CD pipelines.

## Data Hierarchy and Directory Structure

The project utilizes a specific directory structure to ensure clarity and reusability:

```
your_project/
├── circuit_designs/
│   ├── main.yaml           # Top-level circuit design
│   └── flex_pcb_circuit.yaml # Example circuit
├── components/generics/
│   ├── qfn_28.yaml         # Generic QFN-28 package properties
│   ├── res_0402.yaml       # Generic 0402 resistor properties
│   └── cap_0402.yaml       # Generic 0402 capacitor properties
├── components/
│   ├── qfn_28_ch582f.yaml  # Specific QFN-28 component (e.g., CH582F)
│   ├── res_0402_10k.yaml   # 10k 0402 resistor
│   ├── cap_0402_100nf.yaml # 100nF 0402 capacitor
│   ├── ntc_0402_10k.yaml   # 10k NTC thermistor
│   ├── pogopin_smp.yaml    # SMP pogopin connector
│   └── battery_cell_LR44.yaml # LR44 battery cell
├── stencils/
│   ├── rough.svg           # Rough layout template
│   ├── qfn_28_4x4_0.4p_ep2.8x2.8.yaml # QFN-28 stencil
│   ├── 0402_smd.yaml       # 0402 SMD stencil
│   ├── pogopin_standard_throughhole.yaml # Through-hole pogopin stencil
│   └── batteryholder_lr44.yaml # LR44 battery holder stencil
----
└── HasC-Compiler/
    ├── __main__.py       # CLI (e.g. argparse, Typer)
    ├── parser/           # YAML parser
    ├── linker/           # Netlist connection builder
    ├── renderer/
    │   ├── schematic.py  # SVG schematic renderer
    │   ├── layout.py     # SVG / Gerber renderer
    │   └── bom.py        # Bill of materials render
    └── models/           # Data for HasC itself

```

### 1. `circuit_designs/`: Circuit Descriptions

These YAML files define specific circuit designs by specifying component instances and their interconnections.

*   **Focus:** Logical connections (netlist) and component instantiation.
*   **Contents:**
    *   `name`, `description`, `board_type` of the circuit.
    *   `include`: Include other circuit designs.
    *   `components`: A list of component instances:
        *   `ref_des`: Reference designator (e.g., `U1`, `R1`).
        *   `type-general`: Reference to a generic component in `components/generics`.
        *   `type`: Reference to a specific component definition in `components/`.
        *   `value`: Component value (e.g., `"100nF"`).
        *   `block`: Visual grouping for the schematic.
    *   `nets`: A list of net definitions:
        *   `name`: Net name (e.g., `VCC_SYSTEM`, `UART0_TX_NET`).
        *   `connections`: List of `RefDes.PinID` pairs.
        *   `type`: Optional net type (e.g., `RF`, `Power`).

**Example: `circuit_designs/flex_pcb_circuit.yaml`**

```yaml
circuit_design:
  name: main
  description: "Main circuit on the flexible PCB."
  board_type: "Flex-PCB"
  include:
	- "Flex_PCB_Circuit"

  components:
    - ref_des: "U1"
      type: "CH582F_QFN28"
      block: "MCU"
    - ref_des: "C1"
      type: "CAP_0402_100nF"
      value: "100nF"
      block: "Adjustment"
    - ref_des: "R1"
      type: "NTC_0402_10k"
      value: "10k"
      block: "Sensor"

  nets:
    - name: "VCC_SYSTEM"
      connections:
        - "J1.P1"
        - "U1.VCC_MCU"
        - "R1.P1"
    - name: "GND_SYSTEM"
      connections:
        - "J3.P1"
        - "U1.GND_MCU"
        - "C1.P2"
```

### 2. `components/generics/`: Generic Component Properties

These YAML files describe generic, reusable component properties.

### 3. `components/`: Component Definitions

These YAML files define specific, orderable component types, linking logical function, schematic symbol, electrical parameters, and physical footprint.

*   **Focus:** Component characteristics and physical representation.
*   **Contents:**
    *   `id`: Unique identifier for the component type.
    *   `type`, `subtype`, `value`, `description`, `manufacturer`, `part_number`, `datasheet_url`: For BOM and documentation.
    *   `schematic`: Schematic symbol definition:
        *   `symbol_type`: Reference to a predefined symbol in the renderer (e.g., `Resistor_IEC`).
        *   `width`, `height`: Symbol size for the renderer.
        *   `pins`: List of pins:
            *   `id`: Logical pin name (e.g., `P1`, `RF_ANT`).
            *   `label`: Text on the symbol (e.g., `1`, `ANT`).
            *   `side`: Pin position on the symbol (e.g., `Left`, `Right`).
            *   `type`: Electrical type (e.g., `Passive`, `Power`, `I/O`).
            *   `direction`: Pin direction (e.g., `Bidirectional`, `Input`).
    *   `stencil_assignment`: Link to the physical footprint:
        *   `stencil_id`: Reference to a stencil definition in `stencils/`.
        *   `overrides`: Optional overrides for specific stencil parameters.
        *   `pin_mapping`: Mapping between logical pin IDs and physical pad numbers.

**Example: `components/NTC_0402_10k.yaml`**

```yaml
component:
  id: "NTC_0402_10k"
  type: "Thermistor"
  subtype: "NTC"
  value: "10k"
  description: "NTC Thermistor, 10 kOhm, 0402 package, Vishay NTCLE100E3103JB0"
  manufacturer: "Vishay"
  part_number: "NTCLE100E3103JB0"
  datasheet_url: "https://www.vishay.com/docs/29049/ntcl-e1.pdf"

  schematic:
    symbol_type: "Thermistor_NTC"
    width: 8
    height: 4
    pins:
      - id: "P1"
        label: "1"
        side: "Left"
        type: "Passive"
        direction: "Bidirectional"
      - id: "P2"
        label: "2"
        side: "Right"
        type: "Passive"
        direction: "Bidirectional"

  stencil_assignment:
    stencil_id: "0402_SMD" # Reference to the stencil definition
    pin_mapping:
      "P1": "1" # Logical pin 'P1' maps to physical pad '1' of the stencil
      "P2": "2" # Logical pin 'P2' maps to physical pad '2' of the stencil
```

### 4. `stencils/`: Physical Stencil Definitions

These YAML files define the physical geometries of footprints, independent of the component type.

*   **Focus:** Physical dimensions of packages and pads, layer information (solder mask, paste mask, silkscreen).
*   **Contents:**
    *   `id`: Unique identifier for the stencil geometry.
    *   `package_type`, `description`, `source`.
    *   `pin_count`: Total number of pads.
    *   `dimensions`: Package dimensions.
    *   `pads`: Detailed definitions of pads (type, shape, size, pitch).
    *   `layers`: Layer-specific instructions (mask expansions, silkscreen lines).
    *   `markings`: Additional markings like pin-1 indicators.

**Example: `stencils/0402_smd.yaml`**

```yaml
stencil:
  id: "0402_SMD"
  package_type: "SMD_Chip"
  description: "Standard SMD stencil for 0402 package (1.0x0.5mm body)"
  source: "IPC-7351 (general guidance)"

  pin_count: 2
  dimensions:
    body_length: 1.0
    body_width: 0.5
    body_height: 0.4
    body_tolerance: 0.1

  pads:
    type: "SMD"
    shape: "Rectangle"
    width: 0.5
    length: 0.5
    pitch: 1.0

  layers:
    solder_mask:
      expansion: 0.05
    paste_mask:
      reduction: 0.0
    silk_screen:
      outline:
        type: "Rectangle"
        length: 1.2
        width: 0.7
        line_width: 0.1
    assembly_outline:
      type: "Rectangle"
      length: 1.0
      width: 0.5
      line_width: 0.05
```

## 5. Compiler Structure

The `compiler/` directory contains the core logic for parsing, linking, and rendering the hardware designs.

*   `__main__.py`: Command-line interface for the compiler.
*   `parser/`: Modules for parsing YAML files into data structures.
*   `linker/`: Modules for building the netlist connections.
*   `renderer/`: Modules for generating output formats (schematics, layouts, BOMs).
    *   `schematic.py`: Generates SVG schematics.
    *   `layout.py`: Generates SVG or Gerber layouts.
    *   `bom.py`: Generates Bills of Materials.
*   `models/`: Data classes representing components, nets, and other design elements.

## Example Compiler Usage

```python
# Example CLI usage (from __main__.py)
import argparse

# ------------------ CLI ------------------ #
parser = argparse.ArgumentParser(description="HasC-Compiler: YAML → SVG Schematic Generator")
parser.add_argument("-i", "--input", required=True, help="Path to the circuit_design YAML file")
parser.add_argument("-o", "--output", required=True, help="Path to the output SVG file")
parser.add_argument("-c", "--components", required=True, help="Path to the components directory")
parser.add_argument("-s", "--symbolsheet", required=True, help="Path to the central SVG symbol file")
args = parser.parse_args()

# Implementations TBD
# symbol_map = load_component_library(args.components)
# symbol_defs = load_symbol_library(args.symbolsheet)
# design = load_circuit_design(args.input)
# render_svg_schematic(design, symbol_map, symbol_defs, args.output)
```

This outline shows a simple CLI structure.  Future development will include `load_component_library`, `load_symbol_library`, `load_circuit_design` and `render_svg_schematic` implementations.

## Further Development

This project is under active development.  We plan to add more detailed documentation, examples, and tutorials in the future.