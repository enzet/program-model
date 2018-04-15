from generator import svg


class Node:
    def __init__(self, x: int, y: int, function_number: int,
            is_terminal: bool=False):
        self.x = x
        self.y = y
        self.function_number = function_number
        self.is_terminal = is_terminal


class CFG:
    def __init__(self):
        self.nodes = []
        self.arrows = []

    def add_node(self, x: int, y: int, function_number: int):
        self.nodes.append(Node(x, y, function_number))

    def add_chain(self, x: int, y: int, array: list, is_vertical=True):
        for function_number in array:
            self.add_node(x, y, function_number)

            if is_vertical:
                y += 5
            else:
                x += 5

    def draw(self, file_name: str):
        output_svg = svg.SVG(file_name)
        for node in self.nodes:
            node.draw(output_svg)


if __name__ == "__main__":
    cfg = CFG()

    cfg.add_chain(2, 2, [0, 1, 2])
    cfg.draw("test.svg")
