class Style:
    def __init__(self, stroke="#000000", stroke_width=1.0, fill="none") -> None:
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.fill = fill

    def __repr__(self) -> str:
        result = ""
        result += "stroke:" + str(self.stroke) + "; "
        result += "stroke-width:" + str(self.stroke_width) + "; "
        result += "fill:" + str(self.fill) + "; "
        return result[:-1]


class SVGElement:
    def __init__(self):
        self.style = Style()

    def set_style(self, style: Style) -> None:
        self.style = style

    def draw(self, file_):
        pass


class Line(SVGElement):
    def __init__(self, x1: float, y1: float, x2: float, y2: float) -> None:
        super().__init__()
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def draw(self, file_) -> None:
        x1 = self.x1
        y1 = self.y1
        x2 = self.x2
        y2 = self.y2
        file_.write("  <path d = \"M " + str(x1) + "," + str(y1) + " " +
            str(x2) + "," + str(y2) + "\" ")
        file_.write('style = "')
        file_.write(str(self.style))
        file_.write('" />\n')


class Circle(SVGElement):
    def __init__(self, x: float, y: float) -> None:
        super().__init__()
        self.x = x
        self.y = y

    def draw(self, file_) -> None:
        x = self.x
        y = self.y
        d = 7.5
        c = 0.577
        file_.write("""  <path d = "M %5.1f %5.1f C %5.1f %5.1f
                %5.1f %5.1f %5.1f %5.1f C %5.1f %5.1f %5.1f %5.1f %5.1f
                %5.1f C %5.1f %5.1f %5.1f %5.1f %5.1f %5.1f C %5.1f %5.1f
                %5.1f %5.1f %5.1f %5.1f" """ % (
            x, y + d, x - d * c, y + d, x - d, y + d * c, x - d, y, x - d,
            y - d * c, x - d * c, y - d, x, y - d, x + d * c, y - d, x + d,
            y - d * c, x + d, y, x + d, y + d * c, x + d * c, y + d, x,
            y + d))
        file_.write('style = "')
        file_.write(str(self.style))
        file_.write('" />\n')


class SVG:
    def __init__(self, file_name: str) -> None:
        self.elements = []
        self.file_ = open(file_name, "w")

    def add(self, element: SVGElement) -> None:
        self.elements.append(element)

    def draw(self) -> None:
        width = 600
        height = 400
        self.file_.write("<?xml version=\"1.0\" encoding=\"UTF-8\" "
            "standalone=\"no\"?>\n\n")
        self.file_.write("<svg version=\"1.1\" baseProfile=\"full\" ")
        self.file_.write("xmlns=\"http://www.w3.org/2000/svg\" ")
        self.file_.write("width=\"" + str(width) + "\" ")
        self.file_.write("height=\"" + str(height) + "\">\n")
        for element in self.elements:
            element.draw(self.file_)

    def close(self) -> None:
        self.file_.write('</svg>\n')
        self.file_.close()
