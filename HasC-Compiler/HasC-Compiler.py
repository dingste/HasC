# HasC-Compiler.py
# Einstieg: YAML-Schaltplan einlesen und SVG-Schaltplan generieren

import yaml
import os
import argparse
from dataclasses import dataclass, field
from typing import List, Dict
from xml.etree.ElementTree import Element, SubElement, tostring, parse
from xml.dom import minidom

# ------------------ Datenmodell ------------------ #

@dataclass
class Pin:
    id: str
    label: str
    side: str
    type: str
    direction: str

@dataclass
class Schematic:
    symbol_type: str
    width: int
    height: int
    pins: List[Pin]

@dataclass
class ComponentInstance:
    ref_des: str
    type: str
    value: str = ""
    block: str = ""

@dataclass
class Net:
    name: str
    connections: List[str]

@dataclass
class CircuitDesign:
    name: str
    description: str
    board_type: str
    components: List[ComponentInstance]
    nets: List[Net]

# ------------------ YAML Loader ------------------ #

def load_yaml_file(filepath: str) -> dict:
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)

def load_component_library(directory: str) -> Dict[str, Schematic]:
    symbol_map = {}
    for filename in os.listdir(directory):
        if not filename.endswith(".yaml"):
            continue
        filepath = os.path.join(directory, filename)
        content = load_yaml_file(filepath)
        if "component" not in content:
            continue
        c = content["component"]
        if "schematic" not in c:
            continue
        s = c["schematic"]
        symbol_map[c["id"]] = Schematic(
            symbol_type=s["symbol_type"],
            width=s.get("width", 20),
            height=s.get("height", 10),
            pins=[]  # Pins werden später hinzugefügt
        )
    return symbol_map

def load_circuit_design(filepath: str) -> CircuitDesign:
    raw = load_yaml_file(filepath)["circuit_design"]
    components = [ComponentInstance(**c) for c in raw["components"]]
    nets = [Net(**n) for n in raw["nets"]]
    return CircuitDesign(
        name=raw["name"],
        description=raw["description"],
        board_type=raw["board_type"],
        components=components,
        nets=nets
    )

# ------------------ Symbol-Library ------------------ #

def load_symbol_library(svg_path: str) -> Dict[str, Element]:
    tree = parse(svg_path)
    root = tree.getroot()
    ns = {'svg': 'http://www.w3.org/2000/svg'}
    symbols = {}
    for sym in root.findall("svg:symbol", ns):
        symbol_id = sym.attrib.get("id")
        if symbol_id:
            symbols[symbol_id] = sym
    return symbols

# ------------------ SVG Renderer ------------------ #

def prettify(elem):
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def draw_component_from_symbolsheet(x, y, ref_des: str, schematic: Schematic, symbol_defs: Dict[str, Element]) -> Element:
    group = Element('g', attrib={"transform": f"translate({x},{y})"})
    symbol = symbol_defs.get(schematic.symbol_type)
    if symbol is None:
        raise ValueError(f"Symbol '{schematic.symbol_type}' nicht in SVG-Symbolsheet gefunden")
    for elem in symbol:
        group.append(elem)
    label = SubElement(group, 'text', attrib={
        "x": "0", "y": str(schematic.height + 4), "font-size": "4"
    })
    label.text = ref_des
    return group

def render_svg_schematic(design: CircuitDesign, symbol_map: Dict[str, Schematic], symbol_defs: Dict[str, Element], output_file: str):
    svg = Element('svg', attrib={
        "xmlns": "http://www.w3.org/2000/svg",
        "xmlns:xlink": "http://www.w3.org/1999/xlink",
        "width": "800", "height": "600"
    })

    x, y = 20, 20
    dx, dy = 100, 50

    for comp in design.components:
        schematic = symbol_map.get(comp.type)
        if not schematic:
            raise ValueError(f"Fehlende Symboldefinition für Komponententyp: {comp.type}")
        svg.append(draw_component_from_symbolsheet(x, y, comp.ref_des, schematic, symbol_defs))
        y += dy

    with open(output_file, 'w') as f:
        f.write(prettify(svg))

# ------------------ CLI ------------------ #

def main():
    parser = argparse.ArgumentParser(description="HasC-Compiler: YAML → SVG Schematic Generator")
    parser.add_argument("-i", "--input", required=True, help="Pfad zur circuit_design YAML-Datei")
    parser.add_argument("-o", "--output", required=True, help="Pfad zur Ausgabe-SVG-Datei")
    parser.add_argument("-c", "--components", required=True, help="Pfad zum Komponentenverzeichnis")
    parser.add_argument("-s", "--symbolsheet", required=True, help="Pfad zur zentralen SVG-Symboldatei")
    args = parser.parse_args()

    symbol_map = load_component_library(args.components)
    symbol_defs = load_symbol_library(args.symbolsheet)
    design = load_circuit_design(args.input)
    render_svg_schematic(design, symbol_map, symbol_defs, args.output)

if __name__ == "__main__":
    main()
