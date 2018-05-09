import math
import os

from generator.cfg import CFG, CFGRepr, Node, Arrow, Loop, Ellipsis, Text, \
    Edge, Vertex
from generator.vector import Vector
from generator.svg import SVG, TextWrap


def main(directory_name):

    # Useful abbreviations

    a3 = math.pi / 2

    def v(x, y):
        return Vector(x, y)

    def an(point, id_, l="f", t=False, f=True):
        graph.add(Node(point, name=l, index=id_, is_terminal=t,
            is_feasible=f))

    def ant(point, id_, l="f"):
        graph.add(Node(point, name=l, index=id_, is_terminal=True))

    def aa(point1, point2, f=True):
        graph.add(Arrow(point1, point2, is_feasible=f))

    def al(point, angle):
        graph.add(Loop(point, angle))

    def el(point):
        graph.add(Ellipsis(point, Vector(1, 0)))

    def d(name):
        graph.draw(os.path.join(directory_name, name + ".svg"))

    def line(graph: CFGRepr, x: float, y: float, name: str, indexes: list,
             step: float=7, is_vertical: bool=False, is_terminated: bool=False,
             is_looped: bool=False):
        for i, index in enumerate(indexes):
            if index == "...":
                graph.add(Ellipsis(Vector(x, y), Vector(1, 0)))
            else:
                graph.add(Node(Vector(x, y), name=name, index=index,
                    is_terminal=is_terminated and i == len(indexes) - 1))
                if is_looped and i == len(indexes) - 1:
                    graph.add(Loop(Vector(x, y), math.pi / 2.0))
            if i != len(indexes) - 1:
                if is_vertical:
                    graph.add(Arrow(Vector(x, y), Vector(x, y + step)))
                else:
                    graph.add(Arrow(Vector(x, y), Vector(x + step, y)))
            if is_vertical:
                y += step
            else:
                x += step

    # Concrete execution

    graph = CFGRepr()
    line(graph, 2, 2, "s", ["0", "1", "...", "t", "..."])
    line(graph, 2, 8, "s", ["0", "1", "...", "t"])
    d("concrete_execution")

    # Symbolic execution

    graph = CFGRepr(12.5)

    def se(x, y, vstep, hstep, level, i):
        an(v(x, y), i, l="s")
        aa(v(x, y), v(x + hstep, y - vstep))
        aa(v(x, y), v(x + hstep, y + vstep))
        aa(v(x, y), v(x + hstep, y))
        graph.add(Ellipsis(v(x + hstep, y), v(0, 1)))
        if level == 2:
            return
        next = ",l" if i == "0" else (",m" if i == "0,0" else ",n")
        se(x + hstep, y - vstep, vstep / 2.0, hstep, level + 1, i + ",0")
        se(x + hstep, y + vstep, vstep / 2.0, hstep, level + 1, i + next)

    se(3, 20, 10, 9, 0, "0")
    d("symbolic_execution")

    # Simple program

    graph = CFGRepr()
    x, y = 2, 4

    graph.add(Text(Vector(x, y), TextWrap().add("CFG")))
    line(graph, x, y + 4, "f", ["0", "1"], 5, True, True, True)

    x += 12
    graph.add(Text(Vector(x, y - 2), TextWrap().add("symbolic")))
    graph.add(Text(Vector(x, y), TextWrap().add("execution tree")))
    line(graph, x, y + 4, "f", ["0", "1"], 5, True, True)

    x += 12
    text_wrap = TextWrap().add("P", italic=True).add("0", sub=True)
    graph.add(Text(Vector(x, y), text_wrap))
    line(graph, x, y + 4, "f", ["0", "1"], 5, True, True)

    d("simple")

    # Branch program

    c = CFG()
    s = SVG()
    x, y = 2, 6
    c.add_vertex(Vertex("0", Vector(x + 4, y)))
    c.add_vertex(Vertex("1", Vector(x, y + 4), is_terminal=True))
    c.add_vertex(Vertex("2", Vector(x + 8, y + 4), is_terminal=True))
    c.add_edges([("0", "1"), ("0", "2")])
    c.draw_cfg(s, title=(TextWrap().add("CFG"), Vector(6, 2)))
    x += 10
    c.draw_paths(s, Vector(x, y))

    s.draw(os.path.join(directory_name, "branch_paths.svg"))

    # Branch program

    graph = CFGRepr()
    x, y = 6, 2

    v0, v1, v2 = v(x, y), v(x - 4, y + 4), v(x + 4, y + 4)
    an(v0, "0"); ant(v1, "1"); ant(v2, "2")
    aa(v0, v1); aa(v0, v2); al(v1, a3); al(v2, a3)

    x += 10
    v0, v1 = v(x, y), v(x, y + 5)
    an(v0, "0"); ant(v1, "1"); aa(v0, v1)

    x += 5
    v0, v1 = v(x, y), v(x, y + 5)
    an(v0, "0"); ant(v1, "2"); aa(v0, v1)

    x += 10
    v0, v1, v2 = v(x, y), v(x - 4, y + 4), v(x + 4, y + 4)
    an(v0, "0"); ant(v1, "1"); ant(v2, "2"); aa(v0, v1); aa(v0, v2)

    d("branch2")

    # Cycle program

    graph = CFGRepr()
    x, y = 2, 2

    v0, v1 = v(x, y), v(x, y + 5)
    an(v0, "0"); ant(v1, "1")
    aa(v0, v1); al(v1, a3); al(v0, 0)

    x += 10
    v0, v1 = v(x, y), v(x, y + 5)
    an(v0, "0"); ant(v1, "1"); aa(v0, v1)

    x += 5
    v0, v1, v2 = v(x, y), v(x, y + 5), v(x, y + 10)
    an(v0, "0"); an(v1, "0"); ant(v2, "1"); aa(v0, v1); aa(v1, v2)

    x += 5
    v0, v1, v2, v3 = v(x, y), v(x, y + 5), v(x, y + 10), v(x, y + 15)
    an(v0, "0"); an(v1, "0"); an(v2, "0"); ant(v3, "1")
    aa(v0, v1); aa(v1, v2); aa(v2, v3)

    x += 10
    v0, v1, v2 = v(x, y), v(x - 4, y + 4), v(x + 4, y + 4)
    for i in range(3):
        an(v0, "0"); ant(v1, "1"); aa(v0, v1); aa(v0, v2)
        v0 = v0 + v(4, 4); v1 = v1 + v(4, 4); v2 = v2 + v(4, 4)

    d("cycle")

    # Control flow dependence

    g = CFG()
    g.add_vertices([("0", 6, 2), ("1", 2, 6), ("2", 2, 11), ("3", 10, 6),
                    ("4", 10, 11), ("5", 6, 15)])
    g.add_edges([("0", "1"), ("1", "2"), ("0", "3"), ("3", "4"), ("2", "5"),
                 ("4", "5")])
    s = SVG()
    g.draw_cfg(s)
    s.draw(os.path.join(directory_name, "implicit.svg"))

    # Sequence comparison

    graph = CFGRepr()
    x, y = 2, 2

    v0, v1, v2 = v(x, y), v(x + 4, y + 4), v(x, y + 8)
    for i in range(4):
        an(v0, str(i * 2)); an(v1, str(i * 2 + 1))
        aa(v0, v1); aa(v0, v2); aa(v1, v2)
        v0 = v0 + v(0, 8)
        v1 = v1 + v(0, 8)
        v2 = v2 + v(0, 8)
    ant(v0, "8")

    d("classic_cfg")

    graph = CFGRepr()
    x, y = 2, 2

    for i in range(16):
        k = "0" * (6 - len(bin(i))) + bin(i)[2:]
        chain = ["0"]
        if k[3] == "1": chain.append("1")
        chain.append("2")
        if k[2] == "1": chain.append("3")
        chain.append("4")
        if k[1] == "1": chain.append("5")
        chain.append("6")
        if k[0] == "1": chain.append("7")
        chain.append("8")
        graph.add_chain(v(x, y), chain, is_vertical=True,
            is_terminated=True)
        x += 5

    d("classic_paths")

    graph = CFGRepr()
    x, y = 2, 40 + 2 - 2.5

    def dr(index, x, y, step, count, f):
        an(v(x, y), str(index), t=index == 8, f=f)
        if index == 8:
            return
        if index in [1, 3, 5]:
            count += 1
        if index % 2 == 0:
            aa(v(x, y), v(x + 7, y - step), f=count != 3)
            dr(index + 2, x + 7, y - step, step / 2.0, count, f=count != 3)
            aa(v(x, y), v(x + 7, y + step), f=index < 6 or count == 3)
            dr(index + 1, x + 7, y + step, step / 2.0, count,
                f=index < 6 or count == 3)
        else:
            aa(v(x, y), v(x + 7, y), f=index < 6 or count == 3)
            dr(index + 1, x + 7, y, step, count, f=index < 6 or count == 3)

    dr(0, x, y, 20, 0, True)

    d("classic_symbolic_tree")

    # Sequence comparison 2

    graph = CFGRepr()
    x, y = 2, 2

    v0, v1, v2 = v(x, y), v(x + 4, y + 4), v(x + 4, y + 9)
    v3 = v(x, y + 4 * 9)
    for i in range(4):
        an(v0, str(i * 2)); an(v1, str(i * 2 + 1))
        aa(v0, v1); aa(v0, v3); aa(v1, v2)
        v0 = v0 + v(4, 9)
        v1 = v1 + v(4, 9)
        v2 = v2 + v(4, 9)
    an(v0, "8")
    aa(v0, v3)
    ant(v3, "9")

    d("cascade_cfg")
