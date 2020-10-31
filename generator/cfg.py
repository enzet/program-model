"""
Control-flow graph, execution path, and symbolic execution tree generator.
"""
import math

from typing import List

import svgwrite
from svgwrite import Drawing
import numpy as np


FONT: str = "CMU Serif"


def rotation_matrix(angle) -> np.array:
    """
    Get a matrix to rotate 2D vector by the angle.

    :param angle: angle in radians
    """
    return np.array([
        [np.cos(angle), np.sin(angle)],
        [-np.sin(angle), np.cos(angle)]])


def to_grid(point: np.array) -> np.array:
    """
    Convert grid positions to real positions.
    """
    return np.array((2.5, 2.5)) + point * 5


class CFGElement:
    """
    Control-flow graph graphical element.
    """
    def __init__(self):
        self.radius: float = 7.5

    def add(self, output_svg: Drawing) -> None:
        """
        Add graphical representation of the element to the output SVG.
        """
        pass


class Node(CFGElement):
    """
    Control-flow graph node representation.
    """
    def __init__(
            self, point: np.array, name: str = "s", index: str = "",
            is_terminal: bool = False, is_feasible: bool = True):

        super().__init__()
        self.point: np.array = point
        self.name: str = name
        self.index: str = index
        self.is_terminal: bool = is_terminal
        self.is_feasible: bool = is_feasible

    def add(self, svg: Drawing) -> None:
        circle = svg.circle(
            to_grid(self.point), self.radius,
            stroke_width=0.5, fill="none", stroke="black")
        if not self.is_feasible:
            circle.update({"stroke-dasharray": "1,1"})
        svg.add(circle)

        if self.is_terminal:
            circle = svg.circle(to_grid(self.point),
                self.radius - 1.0, fill="none", stroke="black")
            circle.update({"stroke-width": 0.5})
            if not self.is_feasible:
                circle.update({"stroke-dasharray": "1,1"})
            svg.add(circle)

        text_wrap = svg.text(
            "", np.array((0, 2)) + to_grid(self.point), font_size="10px",
            font_family=FONT, text_anchor="middle")
        text_wrap.add(svg.tspan(self.name, font_style="italic"))
        text_wrap.add(svg.tspan(
            self.index, font_size="65%", baseline_shift="sub"))

        svg.add(text_wrap)


class Text(CFGElement):
    def __init__(self, text: svgwrite.text.Text):
        super().__init__()
        self.text: svgwrite.text.Text = text
        self.text.update({
            "font-family": FONT, "font-size": "10px", "text-anchor": "middle"})

    def add(self, svg: Drawing) -> None:
        svg.add(self.text)


class Loop(CFGElement):
    def __init__(self, point: np.array, angle: float):
        super().__init__()
        self.point: np.array = point
        self.angle: float = angle

    def add(self, svg: Drawing) -> None:
        point: np.array = to_grid(self.point)
        radius: float = 7.5
        a1 = self.angle + math.pi / 9.0
        a2 = self.angle - math.pi / 9.0
        n1 = np.array((math.cos(a1), math.sin(a1)))
        n2 = np.array((math.cos(a2), math.sin(a2)))
        p1 = point + n1 * radius
        p2 = point + n1 * 20
        p3 = point + n2 * 20
        p4 = point + n2 * radius
        svg.add(svg.path(
            d=["M", p1, "C", p2, p3, p4], fill="none", stroke="black",
            stroke_width=0.5))

        n = (p4 - p3) / np.linalg.norm(p4 - p3)
        svg.add(svg.path(
            d=create_v(p4, n, np.dot(rotation_matrix(-math.pi / 2.0), n)),
            stroke_width=0.5, fill="none", stroke="black"))


def create_v(point: np.array, n: np.array, m: np.array) -> list:
    return [
        "M", point - n * 3 - m * 3,
        "C", point - n * 2.5 - m * 1.5, point - n * 1.5 - m * 0.5, point,
        "C", point - n * 1.5 + m * 0.5, point - n * 2.5 + m * 1.5,
        point - n * 3 + m * 3]


class Arrow(CFGElement):
    def __init__(
            self, point1: np.array, point2: np.array, is_feasible: bool = True):

        super().__init__()
        assert point1[0] != point2[0] or point1[1] != point2[1]
        self.point1 = point1
        self.point2 = point2
        self.is_feasible = is_feasible

    def add(self, svg: Drawing) -> None:

        a: np.array = to_grid(self.point1)
        b: np.array = to_grid(self.point2)
        n = (b - a) / np.linalg.norm((b - a))
        na = a + (n * self.radius)
        nb = b - (n * self.radius)
        line = svg.line(na, nb, stroke_width=0.5, fill="none", stroke="black")
        if not self.is_feasible:
            line.update({"stroke-dasharray": "1,1"})
        svg.add(line)

        v = svg.path(
            d=create_v(nb, n, np.dot(rotation_matrix(-math.pi / 2.0), n)),
            stroke_width=0.5, fill="none", stroke="black")
        if not self.is_feasible:
            v.update({"stroke-dasharray": "1,1"})
        svg.add(v)


class Ellipsis(CFGElement):
    def __init__(self, point: np.array, n: np.array):
        super().__init__()
        self.point = point
        self.n = n

    def add(self, svg):
        for i in [-4, 0, 4]:
            svg.add(svg.circle(
                to_grid(self.point) + self.n * i, 0.6,
                stroke="none", fill="black"))


class CFGRepresentation:
    def __init__(self, radius: float = 7.5):
        self.elements: List[CFGElement] = []
        self.radius: float = radius

    def add(self, element: CFGElement):
        element.radius = self.radius
        assert isinstance(element, CFGElement)
        self.elements.append(element)

    def add_chain(
            self, point: np.array, array: List[str], is_vertical=True,
            is_terminated=False):

        previous = point

        for index, function_number in enumerate(array):
            if is_terminated and index == len(array) - 1:
                self.add(Node(point, index=function_number, is_terminal=True))
            else:
                self.add(Node(point, index=function_number))
            if index > 0:
                self.add(Arrow(previous, point))

            previous = point
            point = point + (np.array((0, 5)) if is_vertical else np.array((5, 0)))

    def draw(self, file_name: str, size: np.array):
        svg: Drawing = Drawing(size=list(map(str, size)))
        self.create_svg(svg)
        with open(file_name, "w+") as output_file:
            svg.write(output_file)

    def create_svg(self, drawing: Drawing):
        for element in self.elements:  # type: CFGElement
            element.add(drawing)


class Vertex:
    def __init__(self, id_: str, point: np.array, is_terminal: bool = False):
        self.id_: str = id_
        self.point: np.array = point
        self.is_terminal: bool = is_terminal
        self.children = []

    def add_child(self, child):
        self.children.append(child)


class Edge:
    def __init__(self, vertex_id_1, vertex_id_2):
        self.vertex_id_1 = vertex_id_1
        self.vertex_id_2 = vertex_id_2


class CFG:
    def __init__(self):
        self.repr = CFGRepresentation()
        self.vertices = {}
        self.edges = []
        self.init_id = None

    def add_vertex(self, vertex: Vertex):
        self.vertices[vertex.id_] = vertex
        self.repr.add(Node(
            vertex.point, index=vertex.id_, is_terminal=vertex.is_terminal))

        if vertex.is_terminal:
            self.repr.add(Loop(vertex.point, angle=math.pi * 0.5))

        if not self.init_id:
            self.init_id = vertex.id_

    def add_vertices(self, vertices: list):
        for id_, x, y in vertices:
            self.add_vertex(Vertex(id_, np.array((x, y))))

    def add_edges(self, array: list):
        for id_1, id_2 in array:
            self.edges.append(Edge(id_1, id_2))
            self.repr.add(Arrow(self.vertices[id_1].point,
                self.vertices[id_2].point))

            self.vertices[id_1].add_child(self.vertices[id_2])

    def draw_cfg(self, drawing: Drawing, title: Text = None):
        if title:
            self.repr.add(title)

        self.repr.create_svg(drawing)

    def draw_paths(self, svg: Drawing, point: np.array):
        repr = CFGRepresentation()

        queue = [self.vertices[self.init_id]]

        def draw(queue, x, y, wstep, hstep, index):
            if len(queue[-1].children) == 0:
                text_wrap = svg.text(
                    "", to_grid(np.array((x, y))),
                    font_size="10px", font_family=FONT,
                    text_anchor="middle")
                text_wrap.add(svg.tspan("P", font_style="italic"))
                text_wrap.add(svg.tspan(
                    str(index), font_size="65%", baseline_shift="sub"))
                repr.add(Text(text_wrap))
                yy = y + 4
                for inx, child in enumerate(queue):
                    repr.add(Node(
                        np.array((x, yy)), index=child.id_,
                        is_terminal=child.is_terminal))
                    if inx != len(queue) - 1:
                        repr.add(Arrow(np.array((x, yy)), np.array((x, yy + hstep))))
                    yy += hstep
            else:
                for child in queue[-1].children:
                    x += wstep
                    draw(queue + [child], x, y, wstep, hstep, index)
                    index += 1

        draw(queue, point[0], point[1], 5, 5, 0)

        repr.create_svg(svg)
