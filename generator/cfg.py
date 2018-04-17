import math

from typing import List

from generator import svg
from generator.vector import Vector


class CFGElement:
    def __init__(self):
        pass

    def add(self, output_svg: svg.SVG):
        pass


class Node(CFGElement):
    def __init__(self, point: Vector, function_number: str,
            is_terminal: bool = False):
        super().__init__()
        self.point = point
        self.function_number = function_number
        self.is_terminal = is_terminal

    def add(self, output_svg: svg.SVG):
        d = 7.5
        circle = svg.Circle(Vector(2.5, 2.5) + self.point * 5, d)
        circle.style.stroke_width = 0.5
        output_svg.add(circle)

        if self.is_terminal:
            d = 6.5
            circle = svg.Circle(Vector(2.5, 2.5) + self.point * 5, d)
            circle.style.stroke_width = 0.5
            output_svg.add(circle)

        text = svg.Text(Vector(2.5, 4.5) + self.point * 5,
            "<tspan style=\"font-style:italic;\">f</tspan>" +
            "<tspan style=\"font-size:65%; baseline-shift:sub;\">" +
            self.function_number + "</tspan>")
        text.style.font_size = "10px"
        text.style.font_family = "CMU Serif"
        text.style.text_anchor = "middle"
        output_svg.add(text)


class Loop(CFGElement):
    def __init__(self, point: Vector, angle: float):
        super().__init__()
        self.point = point
        self.angle = angle

    def add(self, output_svg: svg.SVG):
        x = 2.5 + self.point.x * 5
        y = 2.5 + self.point.y * 5
        r = 7.5
        a1 = self.angle + math.pi / 9.0
        a2 = self.angle - math.pi / 9.0
        n1 = Vector(math.cos(a1), math.sin(a1))
        n2 = Vector(math.cos(a2), math.sin(a2))
        path = [[Vector(x, y) + n1 * 7.5,
            Vector(x, y) + n1 * 20,
            Vector(x, y) + n2 * 20,
            Vector(x, y) + n2 * 7.5]]
        curve = svg.Curve(path)
        curve.style.stroke_width = 0.5
        output_svg.add(curve)


def create_v(point: Vector, n: Vector, m: Vector):
    return [[point - n * 3 - m * 3, point - n * 2.5 - m * 1.5,
            point - n * 1.5 - m * 0.5, point],
        [point, point - n * 1.5 + m * 0.5, point - n * 2.5 + m * 1.5,
            point - n * 3 + m * 3]]


class Arrow(CFGElement):
    def __init__(self, point1: Vector, point2: Vector, is_feasible: bool=True):
        super().__init__()
        self.point1 = point1
        self.point2 = point2
        self.is_feasible = is_feasible

    def add(self, output_svg: svg.SVG):
        r1 = 7.5
        r2 = 7.5
        a = Vector(2.5, 2.5) + self.point1 * 5
        b = Vector(2.5, 2.5) + self.point2 * 5
        n = (b - a).norm()
        na = a + (n * r1)
        nb = b - (n * r2)
        line = svg.Line(na.x, na.y, nb.x, nb.y)
        line.style.stroke_width = 0.5
        if not self.is_feasible:
            line.style.stroke_dasharray = "1,3"
        output_svg.add(line)

        v = svg.Curve(create_v(nb, n, n.rotate(-math.pi / 2.0)))
        v.style.stroke_width = 0.5
        output_svg.add(v)


class CFGRepr:
    def __init__(self):
        self.elements = []

    def add_element(self, element: CFGElement):
        self.elements.append(element)

    def add_chain(self, point: Vector, array: List[str], is_vertical=True):
        previous = point

        for index, function_number in enumerate(array):
            self.add_element(Node(point, function_number))

            if index > 0:
                self.add_element(Arrow(previous, point))

            previous = point

            if is_vertical:
                point = point + Vector(0, 5)
            else:
                point = point + Vector(5, 0)

    def draw(self, file_name: str):
        output_svg = svg.SVG(file_name)
        for element in self.elements:
            element.add(output_svg)
        output_svg.draw()
        output_svg.close()


class CFG:
    def __init__(self):
        self.repr = CFGRepr()
        self.vertices = []
        self.edges = []

    def add_vertex(self, vertex_id):
        self.vertices.append(vertex_id)

    def add_edge(self, vertex_1_id, vertex_2_id):
        self.edges.append([vertex_1_id, vertex_2_id])

    def draw(self, file_name: str):
        self.repr.draw(file_name)
