# Shapes-py
Assignment 4 for SENG265: Software Methods at UVic

A Python-based SVG art generator that creates HTML files containing randomly generated geometric shapes with customizable properties.

## Features

- Multiple shape types (circles, rectangles, ellipses)
- Configurable shape properties:
  - Size ranges
  - Color ranges (RGB)
  - Opacity levels
  - Position coordinates
- Three generation modes:
  - Random: Fully randomized art with customizable canvas
  - Matrix: Large sparse black and green matrix-style visualization
  - ThinkPad: Wallpaper-sized black and red themed art

## Technical Implementation

**Core Components**
- HTML document generation with SVG canvas
- Shape generation with configurable parameters
- Pandas-based table generation for shape data
- Type hints and proper documentation

## Usage

```python
# Generate all three art styles
python art_generator.py
```

This will create three HTML files:
- a431.html: Random art with varying parameters
- a432.html: Matrix-style visualization (2000x10000)
- a433.html: ThinkPad-themed wallpaper (1900x1170)

## Classes

**HTML Generation**
- `HtmlComponent`: Base class for HTML components
- `HtmlDocument`: HTML document generator
- `SvgCanvas`: SVG viewport handler

**Shape Generation**
- `CircleShape`: Circle SVG generator
- `RectangleShape`: Rectangle SVG generator
- `EllipseShape`: Ellipse SVG generator
- `RandomShape`: Random shape property generator

**Configuration**
- `PyArtConfig`: Configuration handler for shape properties
- `TableGen`: Data table generator for shape properties

## Dependencies

- Python 3.x
- pandas
- typing

## Author

Evan Strasdin

## Note

This implementation intentionally avoids external imports for grading purposes, resulting in a self-contained codebase with comprehensive documentation.
