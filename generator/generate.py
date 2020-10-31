import math
import os
import numpy as np
import svgwrite
from svgwrite import Drawing

from generator.cfg import (
    CFG, CFGRepresentation, Node, Arrow, Loop, Ellipsis, Text, Vertex)


def v(x, y):
    return np.array((x, y))


class Generator:
    """
    Graph generator.
    """
    def __init__(self, directory_name: str):
        self.directory_name = directory_name
        self.graph = CFGRepresentation()
        self.ids = []

    def add(self, element) -> None:
        self.graph.add(element)

    def draw(self, id_: str, size: np.array = np.array((50, 50))) -> None:
        file_name: str = os.path.join(self.directory_name, f"{id_}.svg")
        self.graph.draw(file_name, np.array((5, 5)) + size * 5)
        self.ids.append(id_)

    def line(
            self, graph: CFGRepresentation, x: float, y: float, name: str,
            indices: list, step: float = 7.0, is_vertical: bool = False,
            is_terminated: bool = False, is_looped: bool = False):

        for i, index in enumerate(indices):
            if index == "...":
                graph.add(Ellipsis(np.array((x, y)), np.array((1, 0))))
            else:
                graph.add(Node(
                    np.array((x, y)), name=name, index=index,
                    is_terminal=is_terminated and i == len(indices) - 1))
                if is_looped and i == len(indices) - 1:
                    graph.add(Loop(np.array((x, y)), math.pi / 2.0))
            if i != len(indices) - 1:
                if is_vertical:
                    graph.add(Arrow(np.array((x, y)), np.array((x, y + step))))
                else:
                    graph.add(Arrow(np.array((x, y)), np.array((x + step, y))))
            if is_vertical:
                y += step
            else:
                x += step

    def generate(self):

        # Concrete execution

        self.graph = CFGRepresentation()

        self.line(self.graph, 2, 2, "s", ["0", "1", "...", "t", "..."])
        self.line(self.graph, 2, 8, "s", ["0", "1", "...", "t"])
        self.draw("concrete_execution", np.array((7 * 4 + 4, 10)))

        # Symbolic execution

        self.graph = CFGRepresentation(12.5)

        def se(x, y, vstep, hstep, level, i):
            point = v(x, y)
            self.add(Node(
                point, name="s", index=i, is_terminal=False, is_feasible=True))
            point_ = v(x, y)
            point_1 = v(x + hstep, y - vstep)
            self.add(Arrow(point_, point_1, is_feasible=True))
            point_2 = v(x, y)
            point_3 = v(x + hstep, y + vstep)
            self.add(Arrow(point_2, point_3, is_feasible=True))
            point_4 = v(x, y)
            point_5 = v(x + hstep, y)
            self.add(Arrow(point_4, point_5, is_feasible=True))
            self.add(Ellipsis(v(x + hstep, y), v(0, 1)))
            if level == 2:
                return
            next = ",l" if i == "0" else (",m" if i == "0,0" else ",n")
            se(x + hstep, y - vstep, vstep / 2.0, hstep, level + 1, i + ",0")
            se(x + hstep, y + vstep, vstep / 2.0, hstep, level + 1, i + next)

        se(3, 20, 10, 9, 0, "0")
        self.draw("symbolic_execution", np.array((9 * 3 + 6, 40)))

        # Simple program

        self.graph = CFGRepresentation()
        x, y = 2, 4

        self.add(Text(svgwrite.text.Text(
            "CFG", np.array((2.5, 2.5)) + np.array((x, y)) * 5)))
        self.line(self.graph, x, y + 4, "s", ["0", "1"], 5, True, True, True)

        x += 12
        self.add(Text(svgwrite.text.Text(
            "symbolic", np.array((2.5, 2.5)) + np.array((x, y - 2)) * 5)))
        self.add(Text(svgwrite.text.Text(
            "execution tree", np.array((2.5, 2.5)) + np.array((x, y)) * 5)))
        self.line(self.graph, x, y + 4, "s", ["0", "1"], 5, True, True)

        x += 12
        text_wrap = svgwrite.text.Text(
            "", np.array((2.5, 2.5)) + np.array((x, y)) * 5)
        text_wrap.add(svgwrite.text.TSpan("P", font_style="italic"))
        text_wrap.add(svgwrite.text.TSpan(
            "0", font_size="65%", baseline_shift="sub"))
        self.add(Text(text_wrap))
        self.line(self.graph, x, y + 4, "s", ["0", "1"], 5, True, True)

        self.draw("simple", np.array((x + 2, 18)))

        # Branch program

        c = CFG()
        s = Drawing()
        x, y = 2, 6
        c.add_vertex(Vertex("0", np.array((x + 4, y))))
        c.add_vertex(Vertex("1", np.array((x, y + 4)), is_terminal=True))
        c.add_vertex(Vertex("2", np.array((x + 8, y + 4)), is_terminal=True))
        c.add_edges([("0", "1"), ("0", "2")])
        c.draw_cfg(s, title=(Text(svgwrite.text.Text(
            "CFG", np.array((2.5, 2.5)) + np.array((6, 2)) * 5))))
        x += 10
        c.draw_paths(s, np.array((x, y)))

        with open(os.path.join(self.directory_name, "branch_paths.svg"), "w+") as output_file:
            s.write(output_file)

        # Branch program

        self.graph = CFGRepresentation()
        x, y = 6, 2

        v0, v1, v2 = v(x, y), v(x - 4, y + 4), v(x + 4, y + 4)
        self.add(Node(v0, index="0"))
        self.add(Node(v1, index="1", is_terminal=True))
        self.add(Node(v2, index="2", is_terminal=True))
        self.add(Arrow(v0, v1))
        self.add(Arrow(v0, v2))
        angle = math.pi / 2
        self.add(Loop(v1, angle))
        angle1 = math.pi / 2
        self.add(Loop(v2, angle1))

        x += 10
        v0, v1 = v(x, y), v(x, y + 5)
        self.add(Node(v0, index="0"))
        self.add(Node(v1, index="1", is_terminal=True))
        self.add(Arrow(v0, v1))

        x += 5
        v0, v1 = v(x, y), v(x, y + 5)
        self.add(Node(v0, index="0"))
        self.add(Node(v1, index="2", is_terminal=True))
        self.add(Arrow(v0, v1, is_feasible=True))

        x += 10
        v0, v1, v2 = v(x, y), v(x - 4, y + 4), v(x + 4, y + 4)
        self.add(Node(v0, index="0"))
        self.add(Node(v1, index="1", is_terminal=True))
        self.add(Node(v2, index="2", is_terminal=True))
        self.add(Arrow(v0, v1))
        self.add(Arrow(v0, v2))

        self.draw("branch2")

        # Cycle program

        self.graph = CFGRepresentation()
        x, y = 2, 2

        v0, v1 = v(x, y), v(x, y + 5)
        self.add(Node(v0, index="0"))
        self.add(Node(v1, index="1", is_terminal=True))
        self.add(Arrow(v0, v1))
        angle2 = math.pi / 2
        self.add(Loop(v1, angle2))
        self.add(Loop(v0, 0))

        x += 10
        v0, v1 = v(x, y), v(x, y + 5)
        self.add(Node(v0, index="0"))
        self.add(Node(v1, index="1", is_terminal=True))
        self.add(Arrow(v0, v1))

        x += 5
        v0, v1, v2 = v(x, y), v(x, y + 5), v(x, y + 10)
        self.add(Node(v0, index="0"))
        self.add(Node(v1, index="0"))
        self.add(Node(v2, index="1", is_terminal=True))
        self.add(Arrow(v0, v1))
        self.add(Arrow(v1, v2))

        x += 5
        v0, v1, v2, v3 = v(x, y), v(x, y + 5), v(x, y + 10), v(x, y + 15)
        self.add(Node(v0, index="0"))
        self.add(Node(v1, index="0"))
        self.add(Node(v2, index="0"))
        self.add(Node(v3, index="1", is_terminal=True))
        self.add(Arrow(v0, v1))
        self.add(Arrow(v1, v2))
        self.add(Arrow(v2, v3))

        x += 10
        v0, v1, v2 = v(x, y), v(x - 4, y + 4), v(x + 4, y + 4)
        for i in range(3):
            self.add(Node(v0, index="0"))
            self.add(Node(v1, index="1", is_terminal=True))
            self.add(Arrow(v0, v1))
            self.add(Arrow(v0, v2))
            v0 = v0 + v(4, 4)
            v1 = v1 + v(4, 4)
            v2 = v2 + v(4, 4)

        self.draw("cycle")

        # Control flow dependence

        g = CFG()
        g.add_vertices([
            ("0", 6, 2), ("1", 2, 6), ("2", 2, 11), ("3", 10, 6), ("4", 10, 11),
            ("5", 6, 15)])
        g.add_edges([
            ("0", "1"), ("1", "2"), ("0", "3"), ("3", "4"), ("2", "5"),
            ("4", "5")])
        s = Drawing()
        g.draw_cfg(s)
        with open(os.path.join(self.directory_name, "implicit.svg"), "w+") as output_file:
            s.write(output_file)

        # Sequence comparison

        self.graph = CFGRepresentation()
        x, y = 2, 2

        v0, v1, v2 = v(x, y), v(x + 4, y + 4), v(x, y + 8)
        for i in range(4):
            id_ = str(i * 2)
            self.add(Node(v0, index=id_))
            id_1 = str(i * 2 + 1)
            self.add(Node(v1, index=id_1))
            self.add(Arrow(v0, v1))
            self.add(Arrow(v0, v2))
            self.add(Arrow(v1, v2))
            v0 = v0 + v(0, 8)
            v1 = v1 + v(0, 8)
            v2 = v2 + v(0, 8)
        self.add(Node(v0, index="8", is_terminal=True))

        self.draw("classic_cfg", (v0 + v(2 + 4, 2)))

        self.graph = CFGRepresentation()
        x, y = 2, 2

        for i in range(16):
            k = "0" * (6 - len(bin(i))) + bin(i)[2:]
            chain = ["0"]
            if k[3] == "1":
                chain.append("1")
            chain.append("2")
            if k[2] == "1":
                chain.append("3")
            chain.append("4")
            if k[1] == "1":
                chain.append("5")
            chain.append("6")
            if k[0] == "1":
                chain.append("7")
            chain.append("8")
            self.graph.add_chain(v(x, y), chain, is_terminated=True)
            x += 5

        self.draw("classic_paths")

        self.graph = CFGRepresentation()
        x, y = 2, 40 + 2 - 2.5

        def dr(index, x, y, step, count, f):
            point = v(x, y)
            id_ = str(index)
            t = index == 8
            self.add(Node(point, index=id_, is_terminal=t, is_feasible=f))
            if index == 8:
                return
            if index in [1, 3, 5]:
                count += 1
            if index % 2 == 0:
                point_ = v(x, y)
                point_1 = v(x + 7, y - step)
                f1 = count != 3
                self.add(Arrow(point_, point_1, is_feasible=f1))
                dr(index + 2, x + 7, y - step, step / 2.0, count, f=count != 3)
                point_2 = v(x, y)
                point_3 = v(x + 7, y + step)
                f2 = index < 6 or count == 3
                self.add(Arrow(point_2, point_3, is_feasible=f2))
                dr(index + 1, x + 7, y + step, step / 2.0, count,
                    f=index < 6 or count == 3)
            else:
                point_4 = v(x, y)
                point_5 = v(x + 7, y)
                f3 = index < 6 or count == 3
                self.add(Arrow(point_4, point_5, is_feasible=f3))
                dr(index + 1, x + 7, y, step, count, f=index < 6 or count == 3)

        dr(0, x, y, 20, 0, True)

        self.draw("classic_symbolic_tree", np.array((60, 80 + 4 - 5)))

        # Sequence comparison 2

        self.graph = CFGRepresentation()
        x, y = 2, 2

        v0, v1, v2 = v(x, y), v(x + 4, y + 4), v(x + 4, y + 9)
        v3 = v(x, y + 4 * 9)
        for i in range(4):
            id_2 = str(i * 2)
            self.add(Node(v0, index=id_2))
            id_3 = str(i * 2 + 1)
            self.add(Node(v1, index=id_3))
            self.add(Arrow(v0, v1))
            self.add(Arrow(v0, v3))
            self.add(Arrow(v1, v2))
            v0 = v0 + v(4, 9)
            v1 = v1 + v(4, 9)
            v2 = v2 + v(4, 9)
        self.add(Node(v0, index="8"))
        self.add(Arrow(v0, v3))
        self.add(Node(v3, index="9", is_terminal=True))

        self.draw("cascade_cfg")

        with open("result.html", "w+") as debug_file:
            debug_file.write("".join(map(
                lambda x: f"<img src=\"image/{x}.svg\">", self.ids)))
