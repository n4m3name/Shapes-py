#!/usr/bin/env python

import argparse
from typing import List
from typing import IO
from typing import NamedTuple
import random
import pandas as pd


"""
Note/preamble:
    This file is an absolute monstrosity, at the discretion of the prof who encouraged me to avoid using imports (I'm assuming
    this is for the sake of automated grading).
    I had originally configured the files as a project, with a relative import statement for preceding files - after being
    advised against this I assumed that we were to copy the preceding file's contents into the next project file in order 
    to render them accessible.
    I've attempted to make good use of dosctrings to avoid confusion and make the code legible/usable despite
    the massive size of the file (this obviously did not help the size, but will hopefully help whoever ends up reading this).
    Direct (#) comments were mostly excluded due to the fairly extensive docstrings and simple code.
"""

##---------------------------------------------------------##
## BEGIN SECTION A41: FILE & SHAPE GENERATION
##---------------------------------------------------------##


class HtmlComponent:
    """HtmlComponent superclass - Renders HTML components."""

    def __init__(self, file: IO[str]) -> None:
        """
        __init__() method:
            Initialize HtmlComponent with a file object
        Args:
            file (IO[str]): File to write to
        """
        self.file = file

    def write_html_comment(self, comment: str, indent_level: int = 0) -> None:
        """
        write_html_comment() method:
            Writes an html <!--comment--> to the output file
        Args:
            comment (str): Comment to be written to file
            indent_level (int): Indentation level of the comment, 3 spaces
        """
        indentation = "   " * indent_level
        self.file.write(f"{indentation}<!-- {comment} -->\n")

    def write_html_line(self, line: str, indent_level: int = 0) -> None:
        """
        write_html_line() method:
            Writes a line of text to the output file
        Args:
            line (str): Comment to be written to file
            indent_level (int): Indentation level of the line, 3 spaces
        """
        indentation = "   " * indent_level
        self.file.write(f"{indentation}{line}\n")


class HtmlDocument(HtmlComponent):
    """HTML Document class - Generate HTML documents."""

    def __init__(self, filename: str, title: str) -> None:
        """
        __init__() method:
            Initialize HtmlDocument with a titled and named file object
        Args:
            filename (str): Name of the file
            title (str): Title of the file
        """
        self.filename = filename
        self.title = title
        self.file = None

    def __enter__(self) -> 'HtmlDocument':
        """
        __enter__() method:
            Allows for/necessitates use of context manager,
            outputs necessary opening code for .html file setup
        """
        self.file = open(self.filename, "w")
        self.write_html_line("<html>")
        self.write_html_line("<head>")
        self.write_html_line(f"<title>{self.title}</title>", 1)
        self.write_html_line("</head>")
        self.write_html_line("<body>")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        __exit__() method:
            Allows for/necessitates use of context manager,
            outputs necessary closing code for .html file setup
        """
        self.write_html_line("</body>")
        self.write_html_line("</html>")
        self.file.close()


class Shape(NamedTuple):
    """Shape superclass - Base class for shapes"""
    pass

    def draw(self, indent_level: int = 2) -> None:
        """
        draw() method:
            Init - Allows for calling shape-specific draw() method on ambiguous
            shape instances
        Args:
            indent_level (int): Indentation level of the line, 3 spaces
        """
        raise NotImplementedError("draw method must be implemented in subclass")


class SvgCanvas(HtmlComponent):
    """SvgCanvas subclass - Define viewport and output svg"""

    def __init__(self, file: IO[str], width: int = 0, height: int = 0, bg: str = "white") -> None:
        """
        __init__() method:
            Initialize SvgCanvas with spec'd width, height & background color
        Args:
            width (str)
            height (str)
            bg (str): Background color, 'white' or 'black'
        """
        super().__init__(file)
        self.file = file
        self.width = width
        self.height = height
        self.bg = bg

    def __enter__(self) -> 'SvgCanvas':
        """
        __enter__() method:
            Allows for/necessitates use of context manager,
            outputs necessary opening code for svg viewport setup
        """
        self.write_html_comment("Define SVG drawing box", 1)
        self.write_html_line(f'<svg width="{self.width}" height="{self.height}" style="background-color: {self.bg};">', indent_level=1)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        __exit__() method:
            Allows for/necessitates use of context manager,
            outputs necessary closing code for svg viewport setup
        """
        self.write_html_line("</svg>", 1)

    def genArt(self, shape: Shape, indent_level: int = 2) -> None:
        """
        genArt() method:
            Writes line of svg code from shape.draw to output file
        Args:
            shape (Shape): An instance of the Shape subclasses
            indent_level (int): Indentation level of the line, 3 spaces

        """
        line = shape.draw(indent_level)
        self.write_html_line(line)


class CircleShape(NamedTuple):
    """
    CircleShape class - Holds data & produces line of code for an svg circle
    Args: (All svg values)
        x, y (int): x, y position
        rad (int): circle radius
        width, height: (int): Arbitrary, for ease of use with RandomShape (...)
        rx, ry: (int): ...
        red, green, blue (int): RGB values
        op: Opacity
    """

    x: int
    y: int
    rad: int
    width: int
    height: int
    rx: int
    ry: int
    red: int
    green: int
    blue: int
    op: float

    def draw(self, indent_level: int = 2) -> str:
        """
        draw() method:
            Produces svg code line for a circle with characteristics spec'd upon init
        Args:
            indent_level (int): Indentation level of the comment, 3 spaces
        """
        ts: str = "   " * indent_level
        line1: str = f'<circle cx="{self.x}" cy="{self.y}" r="{self.rad}" '
        line2: str = f'fill="rgb({self.red}, {self.green}, {self.blue})" fill-opacity="{self.op}"></circle>'
        return f"{ts}{line1+line2}"


class RectangleShape(NamedTuple):
    """
    RectangleShape class - Holds data & produces line of code for an svg rectangle
    Args: (All svg values)
        x, y (int): x, y position
        rad (int): Arbitrary, for ease of use with RandomShape (...)
        width, height: (int): Rectangle width, height
        rx, ry: (int): ...
        red, green, blue (int): RGB values
        op: Opacity
    """

    x: int
    y: int
    rad: int
    width: int
    height: int
    rx: int
    ry: int
    red: int
    green: int
    blue: int
    op: float

    def draw(self, indent_level: int = 2) -> str:
        """
        draw() method:
            Produces svg code line for a rectangle with characteristics spec'd upon init
        Args:
            indent_level (int): Indentation level of the comment, 3 spaces
        """
        ts: str = "   " * indent_level
        line1: str = f'<rect x="{self.x}" y="{self.y}" width="{self.width}" height="{self.height}" '
        line2: str = f'fill="rgb({self.red}, {self.green}, {self.blue})" fill-opacity="{self.op}"></rect>'
        return f"{ts}{line1+line2}"


class EllipseShape(NamedTuple):
    """
    EllipseShape class - Holds data & produces line of code for an svg ellipse
    Args: (All svg values)
        x, y (int): x, y position
        rad (int): Arbitrary, for ease of use with RandomShape (...)
        width, height: (int): ...
        rx, ry: (int): x and y radii of ellipse
        red, green, blue (int): RGB values
        op: Opacity
    """

    x: int
    y: int
    rad: int
    width: int
    height: int
    rx: int
    ry: int
    red: int
    green: int
    blue: int
    op: float

    def draw(self, indent_level: int = 2) -> str:
        """
        draw() method:
            Produces svg code line for a rectangle with characteristics spec'd upon init
        Args:
            indent_level (int): Indentation level of the comment, 3 spaces
        """
        ts: str = "   " * indent_level
        line1: str = f'<ellipse cx="{self.x}" cy="{self.y}" rx="{self.rx}" ry="{self.ry}" '
        line2: str = f'fill="rgb({self.red}, {self.green}, {self.blue})" fill-opacity="{self.op}"></ellipse>'
        return f"{ts}{line1+line2}"


##---------------------------------------------------------##
## BEGIN SECTION A42: TABLE GENERATION
##---------------------------------------------------------##


class PyArtConfig:
    """ PyArtConfig class - Holds & provides methods to adjust svg output ranges of shape characteristics"""

    def __init__(self, c: SvgCanvas, shape_type_range=[0, 1, 2], \
                 radius_range=(0, 100), rxy_range=(10, 30), w_h_range=(10, 100), \
                 color_r_range=(0, 255), color_g_range=(0, 255), color_b_range=(0,255), \
                 opacity_range=(0, 1)) -> None:
        """
        __init__() method:
            Initialize PyArtConfig with spec'd ranges
        Args:
            c (SvgCanvas)
            shape_type_range (list[int, int, int]): 0-circle, 1-rectangle, 2-ellipse
            radius_range (tuple(int, int)): Svg radius range of circle
            rxy_range (tuple(int, int)): Svg radii ranges of ellipse
            w_h_range (tuple(int, int)): Svg width/height of rectangle
            color_<r,g,b>_range (tuple(int, int)): Svg ranges for r, g, b
            opacity_range (tuple(int, int)): Svg range for opacity
        """
        self.shape_type_range = shape_type_range
        self.x_range = (0, c.width)
        self.y_range = (0, c.height)
        self.radius_range = radius_range
        self.rxy_range = rxy_range
        self.w_h_range = w_h_range
        self.r_range = color_r_range
        self.g_range = color_g_range
        self.b_range = color_b_range
        self.opacity_range = opacity_range
    
    def shapes(self, shape: int, amt: int) -> None:
        """
        shapes() method:
            Adjust range of shapes
        Args:
            shape (int): 0-circle, 1-rectangle, 2-ellipse
            amt (int): 0-none, 1-all/only
        """
        if shape in [0, 1, 2]:
            if amt == 1:
                self.shape_type_range = [shape]
            elif amt == 0:
                shape_ranges = {0: [1, 2], 1: [0, 2], 2: [0, 1]}
                self.shape_type_range = shape_ranges.get(shape, [])
            else: None

    def size(self, shape_sizes: dict) -> None:
        """
        size() method:
            Adjust range(s) of shape size(s)
        Args:
            shape_sizes (dict - {shape:size, ...}):
                shape (char): 'c'-circle, 'r'-rectangle, 'e'-ellipse
                size (char): 's'-small, 'm'-medium, 'l'-large
        """
        ranges = {
            ('c', 's') : ('radius_range', (0, 33)),
            ('r', 's') : ('w_h_range', (10, 40)),
            ('e', 's') : ('rxy_range', (10, 17)),
            ('c', 'm') : ('radius_range', (33, 66)),
            ('r', 'm') : ('w_h_range', (40, 70)),
            ('e', 'm') : ('rxy_range', (17, 24)),
            ('c', 'l') : ('radius_range', (66, 100)),
            ('r', 'l') : ('w_h_range', (70, 100)),
            ('e', 'l') : ('rxy_range', (24, 30))
        }
        for shape, size in shape_sizes.items():
            attr_name, value = ranges.get((shape, size), (None, None))
            if attr_name and value:
                setattr(self, attr_name, value)

    def color(self, color_amounts: dict) -> None:
        """
        color() method:
            Adjust range(s) of shape colors(s)
        Args:
            color_amounts (dict - {color:amt, ...}):
                color (char): 'r'-red, 'g'-green, 'b'-blue
                amt: 0-none, 1-lo, 2-med, 3-hi, 4-max
        """
        color_ranges = [(0, 0), (0, 85), (85, 170), (170, 255), (255, 255)]
        for color, amount in color_amounts.items():
            if color == 'r': 
                self.r_range = color_ranges[amount]
            elif color == 'g':
                self.g_range = color_ranges[amount]
            elif color == 'b':
                self.b_range = color_ranges[amount]
            else:
                None

    def op_amt(self, amt: int) -> None:
        """
        op_amt() method:
            Adjust range of shape opacity
        Args:
            amt (int): 0-lo, 1-med, 2-hi, 3-max
        """
        opacity_ranges = [(0, 0.33), (0.33, 0.66), (0.66, 1), (1, 1)]
        if amt in [0, 1, 2, 3]:
            self.opacity_range = opacity_ranges[amt]


class RandomShape:
    """ RandomShape class - Generate random Svg shape characteristics based on spec'd ranges"""

    def __init__(self, config: PyArtConfig) -> None:
        """
        __init__() method:
            Initialize RandomShape
        Args:
            config (PyArtConfig)
        """
        self.config = config
        self.generate_shape()

    def generate_shape(self) -> None:
        """
        generate_shape() method:
            Generate random Svg shape characteristics based on config ranges
        """
        self.shape_type = random.choice(self.config.shape_type_range)
        self.radius = random.randint(*self.config.radius_range)
        self.width = random.randint(*self.config.w_h_range)
        self.height = random.randint(*self.config.w_h_range)
        self.rx = random.randint(*self.config.rxy_range)
        self.ry = random.randint(*self.config.rxy_range)
        self.x = random.randint(*self.config.x_range)
        self.y = random.randint(*self.config.y_range)
        self.color_r = random.randint(*self.config.r_range)
        self.color_g = random.randint(*self.config.g_range)
        self.color_b = random.randint(*self.config.b_range)
        self.opacity = round(random.uniform(*self.config.opacity_range), 1)

    def __str__(self) -> str:
        """
        __str__() method:
            Generate string of random svg values over multi lines
        """
        return f"{self.shape_type}\n" \
               f"{self.x}\n" \
               f"{self.y}\n" \
               f"{self.radius}\n" \
               f"{self.width}\n" \
               f"{self.height}\n" \
               f"{self.rx}\n" \
               f"{self.ry}\n" \
               f"{self.color_r}\n" \
               f"{self.color_g}\n" \
               f"{self.color_b}\n" \
               f"{self.opacity}"

    def as_Part2_line(self) -> str:
        """
        as_Part2_line() method:
            Return string of object data formatted as a single line
        """
        return str(self).replace('\n', ' ')

    def as_svg(self) -> str:
        """
        as_svg() method:
            Return a string of the object data in the form of SVG commands
        """
        input_string = self.as_Part2_line()
        data = list(map(int, input_string.split(" ")[1:-1]))  # Extract the shape data as a list of integers
        data.append(float(input_string.split(" ")[-1]))  # Append the float value to the data list
        if self.shape_type == 0: # circle
            svg = CircleShape(*data).draw()
        elif self.shape_type == 1: # rectangle
            svg = RectangleShape(*data).draw()
        else: # ellipse
            svg = EllipseShape(*data).draw()
        return svg


class TableGen:
    """TableGen class - Generates a dataframe table"""

    def __init__(self, lines: list) -> None:
        """
        __init__() method:
            Initialize TableGen
        Args:
            lines (list): List of lines generated by as_Part2_line()
        """
        self.lines = lines

    def gen_df(self) -> pd.DataFrame:
        """
        gen_df() method:
            Generate dataframe table based on list input
        """
        data = [line.split(' ') for line in self.lines]
        headers = ['SHA', 'X', 'Y', 'RAD', 'RX', 'RY', 'W', 'H', 'R', 'G', 'B', 'OP']
        df = pd.DataFrame(data, columns=headers)
        df['CNT'] = df.index
        df = df[['CNT'] + headers] # Replace index w 'CNT' row
        return df.to_string(index=False)


##---------------------------------------------------------##
## BEGIN SECTION A43: CARD GENERATION
##---------------------------------------------------------##


class GenRandom:
    """GenRandom class - Generate a fully randomized html 'card'"""

    def rand_dict(type: str) -> dict:
        """
        rand_dict() method:
            Format a random dictionary to pass to RandomShape methods,
            based on input type
        Args:
            type (str): 'size' for RandomShape.size(), 'color' for RandomShape.color()
        """
        if type == 'size':
            keys = ['c', 'r', 'e']
            values = ['s', 'm', 'l']
        elif type == 'color':
            keys = ['r', 'g', 'b']
            values = [0, 1, 2, 3, 4]
        else:
            return {}
        keys = random.sample(keys, random.randint(1, 3))  # Select up to 3 unique keys
        return {k: random.choice(values) for k in keys} # Return dict w random corresponding values

    def gen() -> None:
        """
        gen() method:
            Generate the html file
        """
        filename = "a431.html"
        title = "a431 - CardGenRandom"
        canvas_w = random.randint(100, 1440)
        canvas_h = random.randint(100, 900)
        canvas_color = random.choice(['black', 'white'])
        with HtmlDocument(filename, title) as doc:
            with SvgCanvas(doc.file, canvas_w, canvas_h) as canvas:
                # Randomize all possible values
                config = PyArtConfig(canvas)
                config.shapes(random.choice([0, 1, 2]), random.choice([0 , 1]))
                config.size(GenRandom.rand_dict('size'))
                config.color(GenRandom.rand_dict('color'))
                config.op_amt(random.randint(0,4))
                num_shapes = random.randint(1,1000)
                for _ in range(num_shapes):
                    rand = RandomShape(config)
                    canvas.write_html_line(rand.as_svg())


class GenMatrix():
    """GenMatrix class - Generate a huge, sparse black and green html 'card'"""

    def gen() -> None:
        """
        gen() method:
            Generate the html file
        """
        filename = "a432.html"
        title = "a432 - GenMatrix"
        canvas_w = 2000 # huge canvas
        canvas_h = 10000 # happy scrolling
        with HtmlDocument(filename, title) as doc:
            with SvgCanvas(doc.file, canvas_w, canvas_h, 'black') as canvas: # black canvas
                config = PyArtConfig(canvas)
                config.shapes(1, 1) # rectangles only
                config.size({'r': 's'}) # all small 
                config.color({'g': 3, 'r': 0, 'b': 0}) # green only
                num_shapes = 1000 # not a lot for a big canvas
                for _ in range(num_shapes):
                    rand = RandomShape(config)
                    canvas.write_html_line(rand.as_svg())

class GenThinkPad():
    """GenThinkPad class - Generate a wallpaper-sized black and red html 'card'"""

    def gen() -> None:
        filename = "a433.html"
        title = "a433 - GenThinkPad"
        canvas_w = 1900 # fills out a firefox/linux viewport
        canvas_h = 1170 # ctrl+0 for 0 zoom
        with HtmlDocument(filename, title) as doc:
            with SvgCanvas(doc.file, canvas_w, canvas_h, 'black') as canvas: # black canvas
                config = PyArtConfig(canvas)
                config.color({'g': 0,'b': 0}) # all red
                num_shapes = 300 # not too crowded
                for _ in range(num_shapes):
                    rand = RandomShape(config)
                    canvas.write_html_line(rand.as_svg())
        return


def main() -> None:
    """
    main method:
        Generate three html 'cards', a431.html, a432.html and a433.html
    """
    GenRandom.gen()
    GenMatrix.gen()
    GenThinkPad.gen()


if __name__ == "__main__":
    main()