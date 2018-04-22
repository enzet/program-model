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
        self.boundary_box = Box(Vector(0, 0), Vector(0, 0))

    def draw(self, file_):
        pass


class Line(SVGElement):
    def __init__(self, x1: float, y1: float, x2: float, y2: float) -> None:
        super().__init__()
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.style = Style(fill="none", stroke="#000000", stroke_width=1.0)
        self.boundary_box = Box(Vector(x1, y1), Vector(x2, y2))

    def draw(self, file_) -> None:
        file_.write("    <path d=\"M " + str(self.x1) + "," + str(self.y1) +
            " " + str(self.x2) + "," + str(self.y2) + "\" ")
        file_.write("style = \"")
        file_.write(str(self.style))
        file_.write("\" />\n")


class Circle(SVGElement):
    def __init__(self, point: Vector, r: float) -> None:
        super().__init__()
        self.point = point
        self.r = r
        self.style = Style(fill="none", stroke="#000000", stroke_width=1.0)
        self.boundary_box = Box(self.point - Vector(r, r),
            self.point + Vector(r, r))

    def draw(self, file_) -> None:
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


class Curve(SVGElement):
    def __init__(self, description: List[List[Vector]]):
        super().__init__()
        self.description = description
        self.style = Style(fill="none", stroke="#000000", stroke_width=1.0)
        self.boundary_box = Box(description[0][0], description[0][0])
        for segment in self.description:
            for point in segment:
                self.boundary_box.resize(point)

    def draw(self, file_) -> None:
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

        # p1 = self.boundary_box.point1
        # p2 = self.boundary_box.point2
        # file_.write("<path "
        #     "style=\"fill:none; stroke:#FF0000; stroke-width:1;\" "
        #     "d=\"M %f,%f L %f,%f L %f,%f L %f,%f Z\" />\n" %
        #     (p1.x, p1.y, p1.x, p2.y, p2.x, p2.y, p2.x, p1.y))


class Text(SVGElement):
    def __init__(self, point: Vector, text: str) -> None:
        super().__init__()
        self.point = point
        self.text = text
        self.style = Style(fill="#000000", stroke="none")
        self.boundary_box = Box(point, point)

    def draw(self, file_) -> None:
        file_.write("    <text x=\"" + str(self.point.x) + "\" y=\"" +
            str(self.point.y) + "\" ")
        file_.write("style=\"")
        file_.write(str(self.style))
        file_.write("\">")
        file_.write(self.text)
        file_.write("</text>\n")


class SVG:
    def __init__(self, file_name: str) -> None:
        self.elements = []
        self.file_ = open(file_name, "w")
        self.height = 10
        self.width = 10

    def add(self, element: SVGElement) -> None:
        self.elements.append(element)
        if element.boundary_box.point2.x + 5 > self.width:
            self.width = element.boundary_box.point2.x + 5
        if element.boundary_box.point2.y + 5 > self.height:
            self.height = element.boundary_box.point2.y + 5

    def draw(self) -> None:
        self.file_.write("<?xml version=\"1.0\" encoding=\"UTF-8\" "
            "standalone=\"no\"?>\n\n")
        self.file_.write("<svg version=\"1.1\" baseProfile=\"full\" ")
        self.file_.write("xmlns=\"http://www.w3.org/2000/svg\" ")
        self.file_.write("width=\"" + str(self.width) + "\" ")
        self.file_.write("height=\"" + str(self.height) + "\">\n")
        for element in self.elements:
            element.draw(self.file_)

    def close(self) -> None:
        self.file_.write('</svg>\n')
        self.file_.close()


def font_wrap(text: str, italic: bool=False, sub: bool=False) -> str:
    result = "<tspan style=\""

    if italic:
        result += "font-style:italic; "
    if sub:
        result += "font-size:65%; baseline-shift:sub; "

    result += "\">" + text + "</tspan>"
    return result
