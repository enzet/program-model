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

    # Sequence comparison

    cfg_repr = CFGRepr()
    x, y = 6, 40

    v0, v1, v2 = v(x, y), v(x + 4, y + 4), v(x, y + 8)
    for i in range(4):
        an(v0, str(i * 2)); an(v1, str(i * 2 + 1))
        aa(v0, v1); aa(v0, v2); aa(v1, v2)
        v0 = v0 + v(0, 8)
        v1 = v1 + v(0, 8)
        v2 = v2 + v(0, 8)
    ant(v0, "8")

    x += 10

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
        cfg_repr.add_chain(v(x, y), chain, is_vertical=False)
        y += 4

    x, y = 0, 0

    def dr(index, x, y, step, count):
        an(v(x, y), str(index), t=index == 10)
        if index == 10:
            return
        if index in [1, 3, 5, 7]:
            count += 1
        if index % 2 == 0:
            aa(v(x, y), v(x + 7, y - step), f=count != 4)
            dr(index + 2, x + 7, y - step, step / 2.0, count)
            aa(v(x, y), v(x + 7, y + step), f=index < 8 or count == 4)
            dr(index + 1, x + 7, y + step, step / 2.0, count)
        else:
            aa(v(x, y), v(x + 7, y), f=index < 8 or count == 4)
            dr(index + 1, x + 7, y, step, count)

    dr(0, x, y, 30, 0)

    cfg_repr.draw("classic_symbolic_tree.svg")

    #print(open("test.svg", "r").read())
