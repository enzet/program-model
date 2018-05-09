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

        text_wrap = svg.TextWrap()
        text_wrap.add(self.name, italic=True)
        text_wrap.add(self.index, sub=True)

        text = svg.Text(Vector(2.5, 4.5) + self.point * 5, text_wrap,
                style=svg.Style(font_size="10px", font_family="CMU Serif",
                    text_anchor="middle"))
        output_svg.add(text)


class Text(CFGElement):
    def __init__(self, point: Vector, text: svg.TextWrap):
        super().__init__()
        self.point = point
        self.text = text

    def add(self, output_svg: svg.SVG):
        text = svg.Text(Vector(2.5, 4.5) + self.point * 5, self.text,
            style=svg.Style(font_size="10px", font_family="CMU Serif",
                text_anchor="middle"))
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
        output_svg = svg.SVG()
        self.create_svg(output_svg)
        output_svg.draw(file_name)

    def create_svg(self, drawing: svg.SVG):
        for element in self.elements:
            element.add(drawing)


class Vertex:
    def __init__(self, id_, point: Vector, is_terminal=False):
        self.id_ = id_
        self.point = point
        self.is_terminal = is_terminal
        self.children = []

    def add_child(self, child):
        self.children.append(child)


class Edge:
    def __init__(self, vertex_id_1, vertex_id_2):
        self.vertex_id_1 = vertex_id_1
        self.vertex_id_2 = vertex_id_2


class CFG:
    def __init__(self):
        self.repr = CFGRepr()
        self.vertices = {}
        self.edges = []
        self.init_id = None

    def add_vertex(self, vertex: Vertex):
        self.vertices[vertex.id_] = vertex
        self.repr.add(Node(vertex.point, index=vertex.id_,
            is_terminal=vertex.is_terminal))

        if vertex.is_terminal:
            self.repr.add(Loop(vertex.point, angle=math.pi * 0.5))

        if not self.init_id:
            self.init_id = vertex.id_

    def add_vertices(self, vertices: list):
        for id_, x, y in vertices:
            self.add_vertex(Vertex(id_, Vector(x, y)))

    def add_edges(self, array: list):
        for id_1, id_2 in array:
            self.edges.append(Edge(id_1, id_2))
            self.repr.add(Arrow(self.vertices[id_1].point,
                self.vertices[id_2].point))

            self.vertices[id_1].add_child(self.vertices[id_2])

    def draw_cfg(self, drawing: svg.SVG, title=None):
        if title:
            title_text, title_point = title
            self.repr.add(Text(title_point, title_text))

        self.repr.create_svg(drawing)

    def draw_paths(self, drawing: svg.SVG, point: Vector):
        repr = CFGRepr()

        queue = [self.vertices[self.init_id]]

        def draw(queue, x, y, wstep, hstep, index):
            if len(queue[-1].children) == 0:
                repr.add(Text(Vector(x, y),
                    svg.TextWrap().add("P", italic=True)
                        .add(str(index), sub=True)))
                yy = y + 4
                for inx, child in enumerate(queue):
                    repr.add(Node(Vector(x, yy), index=child.id_,
                        is_terminal=child.is_terminal))
                    if inx != len(queue) - 1:
                        repr.add(Arrow(Vector(x, yy), Vector(x, yy + hstep)))
                    yy += hstep
            else:
                for child in queue[-1].children:
                    x += wstep
                    draw(queue + [child], x, y, wstep, hstep, index)
                    index += 1

        draw(queue, point.x, point.y, 5, 5, 0)

        repr.create_svg(drawing)
