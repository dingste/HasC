# HasC: Hardware as Code

## Motivation

Tired of fighting with traditional ECAD suites?  Frustrated by incompatible libraries, cryptic symbols, and endless clicking?  HasC aims to bring the benefits of software development practices to hardware design. We believe schematic and PCB design in 2025 should be more straightforward, less error-prone, and easily version controlled.

This project explores the idea of **Hardware as Code**, enabling a declarative approach to circuit design using YAML.

## Key Features

*   **Declarative Design:** Describe your hardware in human-readable and machine-parseable YAML files.
*   **Version Control Friendly:** Track changes and collaborate effectively using standard software development workflows.
*   **Modular & Reusable:** Define components and physical stencils independently for reuse across projects.
*   **Automated Generation:**  Automatically generate schematics, layouts, and Bills of Materials (BOMs) from your YAML definitions.
*   **Clear Separation of Concerns:**  Distinguish between logical component definitions and their physical representations.

## Project Structure

The core of HasC revolves around a specific directory structure and file types:

```
your_project/
├── circuit_designs/     # Circuit descriptions 
├── components/generics/  # Generic component properties
├── components/         # Specific component definitions (linking logic to physical)
└── stencils/           # Physical footprint definitions
```

See the [Reference.md](Reference.md) for a detailed explanation of each directory and file type.

## Getting Started

1.  **Installation:** (Instructions will be added later, after the initial compiler is published)
2.  **Explore the Examples:**  Browse the example YAML files in the repository to understand the structure and syntax.
3.  **Contribute:**  We welcome contributions!  See the [Contributing Guidelines](CONTRIBUTING.md).

## Roadmap

*   [ ] Implement the core YAML parser and data model.
*   [ ] Develop the schematic renderer (SVG output).
*   [ ] Implement the layout generator (SVG/Gerber output).
*   [ ] Create a comprehensive component library in YAML.
*   [ ] Add support for more advanced features (e.g., simulation integration).

## Contributing

We are actively seeking contributors to help us build HasC!  If you're passionate about hardware design and software development, we encourage you to get involved.  (See [Contributing Guidelines](CONTRIBUTING.md))

## License

Apache 2.0