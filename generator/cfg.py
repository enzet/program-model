import math

from typing import List

from generator import svg
from generator.vector import Vector


class CFGElement:
    def __init__(self):
        self.radius = 7.5

    def add(self, output_svg: svg.SVG):
        pass


class Node(CFGElement):
    def __init__(self, point: Vector, name: str="f", index: str="",
            is_terminal: bool=False, is_feasible: bool=True):
        super().__init__()
        self.point = point
        self.name = name
        self.index = index
        self.is_terminal = is_terminal
        self.is_feasible = is_feasible

    def add(self, output_svg: svg.SVG):
        circle = svg.Circle(Vector(2.5, 2.5) + self.point * 5, self.radius)
        circle.style.stroke_width = 0.5
        if not self.is_feasible:
            circle.style.stroke_dasharray = "1,1"
        output_svg.add(circle)

        if self.is_terminal:
            circle = svg.Circle(Vector(2.5, 2.5) + self.point * 5,
                self.radius - 1.0)
            circle.style.stroke_width = 0.5
            if not self.is_feasible:
                circle.style.stroke_dasharray = "1,1"
            output_svg.add(circle)

        text = svg.Text(Vector(2.5, 4.5) + self.point * 5,
            svg.font_wrap(self.name, italic=True) +
            svg.font_wrap(self.index, sub=True))
        text.style.font_size = "10px"
        text.style.font_family = "CMU Serif"
        text.style.text_anchor = "middle"
        output_svg.add(text)


class Text(CFGElement):
    def __init__(self, point: Vector, text: str):
        super().__init__()
        self.point = point
        self.text = text

    def add(self, output_svg: svg.SVG):
        text = svg.Text(Vector(2.5, 4.5) + self.point * 5, self.text)
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
        p1 = Vector(x, y) + n1 * r
        p2 = Vector(x, y) + n1 * 20
        p3 = Vector(x, y) + n2 * 20
        p4 = Vector(x, y) + n2 * r
        path = [[p1, p2, p3, p4]]
        curve = svg.Curve(path)
        curve.style.stroke_width = 0.5
        output_svg.add(curve)

        n = (p4 - p3).norm()
        v = svg.Curve(create_v(p4, n, n.rotate(-math.pi / 2.0)))
        v.style.stroke_width = 0.5
        output_svg.add(v)


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
        a = Vector(2.5, 2.5) + self.point1 * 5
        b = Vector(2.5, 2.5) + self.point2 * 5
        n = (b - a).norm()
        na = a + (n * self.radius)
        nb = b - (n * self.radius)
        line = svg.Line(na.x, na.y, nb.x, nb.y)
        line.style.stroke_width = 0.5
        if not self.is_feasible:
            line.style.stroke_dasharray = "1,1"
        output_svg.add(line)

        v = svg.Curve(create_v(nb, n, n.rotate(-math.pi / 2.0)))
        if not self.is_feasible:
            v.style.stroke_dasharray = "1,1"
        v.style.stroke_width = 0.5
        output_svg.add(v)


class Ellipsis(CFGElement):
    def __init__(self, point: Vector, n: Vector):
        super().__init__()
        self.point = point
        self.n = n

    def add(self, output_svg):
        for i in [-4, 0, 4]:
            p = svg.Circle(Vector(2.5, 2.5) + self.point * 5 + self.n * i, 0.6)
            p.style.stroke = "none"
            p.style.fill = "#000000"
            output_svg.add(p)


class CFGRepr:
    def __init__(self, radius: float=7.5):
        self.elements = []
        self.radius = radius

    def add(self, element: CFGElement):
        element.radius = self.radius
        self.elements.append(element)

    def add_chain(self, point: Vector, array: List[str], is_vertical=True,
            is_terminated=False):
        previous = point

        for index, function_number in enumerate(array):
            if is_terminated and index == len(array) - 1:
                self.add(Node(point, index=function_number,
                    is_terminal=True))
            else:
                self.add(Node(point, index=function_number))
            if index > 0:
                self.add(Arrow(previous, point))

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
        self.vertices = {}
        self.edges = []

    def add_vertex(self, vertex_id, x: int, y: int):
        self.vertices[vertex_id] = Vector(x, y)
        self.repr.add(Node(Vector(x, y), index=vertex_id))

    def add_vertices(self, vertices: list):
        for id_, x, y in vertices:
            self.add_vertex(id_, x, y)

    def add_edges(self, array: list):
        for id_1, id_2 in array:
            self.edges.append([id_1, id_2])
            self.repr.add(Arrow(self.vertices[id_1], self.vertices[id_2]))

    def draw(self, file_name: str):
        self.repr.draw(file_name)
