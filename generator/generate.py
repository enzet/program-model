import math

from generator.cfg import CFGRepr, Node, Arrow, Loop
from generator.vector import Vector


if __name__ == "__main__":

    # Useful abbreviations

    a3 = math.pi / 2

    def add(element):
        cfg_repr.add_element(element)

    def v(x, y):
        return Vector(x, y)

    def an(point, id_, t=False):
        cfg_repr.add_element(Node(point, id_, is_terminal=t))

    def ant(point, id_):
        cfg_repr.add_element(Node(point, id_, is_terminal=True))

    def aa(point1, point2, f=True):
        cfg_repr.add_element(Arrow(point1, point2, is_feasible=f))

    def al(point, angle):
        cfg_repr.add_element(Loop(point, angle))

    # Branch program

    cfg_repr = CFGRepr()
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

    cfg_repr.draw("branch.svg")

    # Cycle program

    cfg_repr = CFGRepr()
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

    cfg_repr.draw("cicle.svg")


