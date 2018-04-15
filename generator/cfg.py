from generator import svg


class Node:
    def __init__(self, x: int, y: int, function_number: int,
            is_terminal: bool=False):
        self.x = x
        self.y = y
        self.function_number = function_number
        self.is_terminal = is_terminal

    def add(self, output_svg: svg.SVG):
        output_svg.add(svg.Circle(2.5 + self.x * 5, 2.5 + self.y * 5))


class Arrow:
    def __init__(self, x1: float, y1: float, x2: float, y2: float):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def add(self, output_svg: svg.SVG):
        x1 = self.x1
        y1 = self.y1
        x2 = self.x2
        y2 = self.y2
        output_svg.add(svg.Line(2.5 + x1 * 5, 2.5 + y1 * 5,
                                2.5 + x2 * 5, 2.5 + y2 * 5))


class CFG:
    def __init__(self):
        self.nodes = []
        self.arrows = []

    def add_node(self, node: Node):
        self.nodes.append(node)

    def add_arrow(self, arrow: Arrow):
        self.arrows.append(arrow)

    def add_chain(self, x: int, y: int, array: list, is_vertical=True):
        previous_x, previous_y = x, y

        for index, function_number in enumerate(array):
            self.add_node(Node(x, y, function_number))

            if index > 0:
                self.add_arrow(Arrow(previous_x, previous_y, x, y))

            previous_x = x
            previous_y = y

            if is_vertical:
                y += 5
            else:
                x += 5

    def draw(self, file_name: str):
        output_svg = svg.SVG(file_name)
        for arrow in self.arrows:
            arrow.add(output_svg)
        for node in self.nodes:
            node.add(output_svg)
        output_svg.draw()
        output_svg.close()


if __name__ == "__main__":
    cfg = CFG()

    cfg.add_chain(2, 2, [0, 1, 2])
    cfg.draw("test.svg")
