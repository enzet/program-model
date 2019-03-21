from typing import List

from generator.vector import Vector


class Style:
    def __init__(self, stroke=None, stroke_width=None, stroke_dasharray=None,
            fill=None, font_size=None, font_family=None, text_anchor=None) \
            -> None:
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.stroke_dasharray = stroke_dasharray
        self.fill = fill
        self.font_family = font_family
        self.text_anchor = text_anchor
        self.font_size = font_size

    def __mul__(self, other):
        if other.stroke:
            self.stroke = other.stroke
        if other.stroke_width:
            self.stroke_width = other.stroke_width
        if other.stroke_dasharray:
            self.stroke_dasharray = other.stroke_dasharray
        if other.fill:
            self.fill = other.fill
        if other.font_family:
            self.font_family = other.font_family
        if other.text_anchor:
            self.text_anchor = other.text_anchor
        if other.font_size:
            self.font_self = other.font_size
        return self

    def __repr__(self) -> str:
        result = ""
        if self.stroke:
            result += "stroke:" + str(self.stroke) + "; "
        if self.stroke_width:
            result += "stroke-width:" + str(self.stroke_width) + "; "
        if self.stroke_dasharray:
            result += "stroke-dasharray:" + str(self.stroke_dasharray) + "; "
        if self.fill:
            result += "fill:" + str(self.fill) + "; "
        if self.font_size:
            result += "font-size:" + str(self.font_size) + "; "
        if self.font_family:
            result += "font-family:" + str(self.font_family) + "; "
        if self.text_anchor:
            result += "text-anchor:" + str(self.text_anchor) + "; "
        return result[:-1]


class SVGElement:
    def __init__(self):
        self.style = Style()
        self.boundary_box = Box(Vector(), Vector())

    def draw(self, file_, show_boundary: bool=False):
        if show_boundary:
            file_.write(self.boundary_box.to_path())


class Line(SVGElement):
    def __init__(self, x1: float, y1: float, x2: float, y2: float) -> None:
        super().__init__()
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.style = Style(fill="none", stroke="#000000", stroke_width=1.0)
        self.boundary_box = Box(Vector(x1, y1), Vector(x2, y2))

    def draw(self, file_, show_boundary: bool=False) -> None:
        file_.write("    <path d=\"M " + str(self.x1) + "," + str(self.y1) +
            " " + str(self.x2) + "," + str(self.y2) + "\" ")
        file_.write("style = \"")
        file_.write(str(self.style))
        file_.write("\" />\n")
        super().draw(file_, show_boundary)


class Circle(SVGElement):
    def __init__(self, point: Vector, r: float) -> None:
        super().__init__()
        self.point = point
        self.r = r
        self.style = Style(fill="none", stroke="#000000", stroke_width=1.0)
        self.boundary_box = Box(self.point - Vector(r, r),
            self.point + Vector(r, r))

    def draw(self, file_, show_boundary: bool=False) -> None:
        x = self.point.x
        y = self.point.y
        r = self.r
        c = 0.577
        file_.write("    <path d=\"M %5.1f %5.1f C %5.1f %5.1f "
                "%5.1f %5.1f %5.1f %5.1f C %5.1f %5.1f %5.1f %5.1f %5.1f "
                "%5.1f C %5.1f %5.1f %5.1f %5.1f %5.1f %5.1f C %5.1f %5.1f "
                "%5.1f %5.1f %5.1f %5.1f\" " % (
            x, y + r, x - r * c, y + r, x - r, y + r * c, x - r, y,
            x - r, y - r * c, x - r * c, y - r, x, y - r, x + r * c, y - r,
            x + r, y - r * c, x + r, y, x + r, y + r * c, x + r * c, y + r,
            x, y + r))
        file_.write("style = \"")
        file_.write(str(self.style))
        file_.write("\" />\n")
        super().draw(file_, show_boundary)


def str_pair(pair: Vector) -> str:
    return str(pair.x) + " " + str(pair.y)


class Box:
    def __init__(self, point1, point2):
        self.point1 = Vector(point1.x, point1.y)
        self.point2 = Vector(point2.x, point2.y)

    def resize(self, point: Vector):
        if point.x < self.point1.x:
            self.point1.x = point.x
        if point.y < self.point1.y:
            self.point1.y = point.y
        if point.x > self.point2.x:
            self.point2.x = point.x
        if point.y > self.point2.y:
            self.point2.y = point.y

    def __mul__(self, other):
        if other.point1.x < self.point1.x:
            self.point1.x = other.point1.x
        if other.point1.y < self.point1.y:
            self.point1.y = other.point1.y
        if other.point2.x > self.point2.x:
            self.point2.x = other.point2.x
        if other.point2.y > self.point2.y:
            self.point2.y = other.point2.y
        return self

    def to_path(self) -> str:
        p1 = self.point1
        p2 = self.point2

        return ("<path "
            "style=\"fill:none; stroke:#FF0000; stroke-width:0.2;\" "
            "d=\"M %f,%f L %f,%f L %f,%f L %f,%f Z\" />\n" %
            (p1.x, p1.y, p1.x, p2.y, p2.x, p2.y, p2.x, p1.y))


class Curve(SVGElement):
    def __init__(self, description: List[List[Vector]]):
        super().__init__()
        self.description = description
        self.style = Style(fill="none", stroke="#000000", stroke_width=1.0)
        self.boundary_box = Box(description[0][0], description[0][0])
        for segment in self.description:
            for point in segment:
                self.boundary_box.resize(point)

    def draw(self, file_, show_boundary: bool=False) -> None:
        path = self.description
        file_.write("    <path d=\"")
        file_.write("M " + str_pair(path[0][0]))
        for segment in self.description:
            file_.write(" C " + str_pair(segment[1]) + " " +
                str_pair(segment[2]) + " " + str_pair(segment[3]) + " ")
        file_.write("\" ")
        file_.write("style=\"")
        file_.write(str(self.style))
        file_.write("\" />\n")
        super().draw(file_, show_boundary)


class TextWrap:
    def __init__(self, text=None):
        self.elements = []
        if text:
            self.add(text)

    def add(self, text: str, italic: bool=False, sub: bool=False):
        result = "<tspan style=\""
        if italic:
            result += "font-style:italic; "
        if sub:
            result += "font-size:65%; baseline-shift:sub; "
        result += "\">" + text + "</tspan>"

        self.elements.append((text, result))
        return self

    def __len__(self) -> int:
        length = 0
        for text, _ in self.elements:
            length += len(text)
        return length

    def __repr__(self) -> str:
        representation = ""
        for _, r in self.elements:
            representation += r
        return representation


class Text(SVGElement):
    def __init__(self, point: Vector, text: TextWrap, style: Style) -> None:
        super().__init__()
        self.point = point
        self.text = text
        self.style = Style(fill="#000000", stroke="none", font_size=10) * style
        self.boundary_box = Box(point, point)

        a1 = 0
        a2 = 1
        if self.style.text_anchor == "middle":
            a1 = 0.5
            a2 = 0.5
        if self.style.text_anchor == "rigth":
            a1 = 1
            a2 = 0

        self.boundary_box = Box(
            Vector(point.x - self.style.font_size * len(text) * a1 * 0.45,
                point.y - self.style.font_size * 0.8),
            Vector(point.x + self.style.font_size * len(text) * a2 * 0.45,
                point.y + self.style.font_size * 0.2))

    def draw(self, file_, show_boundary: bool=False) -> None:
        """
        Write <text> tag into SVG file.

        :param file_: output file.
        :param show_boundary: draw text boundary box.
        """
        file_.write("    <text x=\"" + str(self.point.x) + "\" y=\"" +
            str(self.point.y) + "\" ")
        file_.write("style=\"")
        file_.write(str(self.style))
        file_.write("\">")
        file_.write(str(self.text))
        file_.write("</text>\n")
        super().draw(file_, show_boundary)


class SVG:
    """
    SVG document.
    """
    def __init__(self) -> None:
        self.elements = []
        self.boundary_box = Box(Vector(), Vector())

    def add(self, element: SVGElement) -> None:
        """
        Add SVG element to SVG document.

        :param element: SVG element.
        """
        self.elements.append(element)
        self.boundary_box = self.boundary_box * element.boundary_box

    def draw(self, file_name: str) -> None:
        """
        Write the whole SVG document into a file.

        :param file_name: result SVG file name.
        """
        width = self.boundary_box.point2.x
        height = self.boundary_box.point2.y

        file_ = open(file_name, "w+")
        file_.write("<?xml version=\"1.0\" encoding=\"UTF-8\" "
            "standalone=\"no\"?>\n\n")
        file_.write("<svg version=\"1.1\" baseProfile=\"full\" ")
        file_.write("xmlns=\"http://www.w3.org/2000/svg\" ")
        file_.write("width=\"" + str(width) + "\" ")
        file_.write("height=\"" + str(height) + "\">\n")

        for element in self.elements:
            element.draw(file_)

        file_.write('</svg>\n')
        file_.close()
