class Style:
    def __init__(self, stroke=None, stroke_width=None, fill=None,
            font_size=None, font_family=None, text_anchor=None) -> None:
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.fill = fill
        self.font_family = font_family
        self.text_anchor = text_anchor
        self.font_size = font_size

    def __repr__(self) -> str:
        result = ""
        if self.stroke:
            result += "stroke:" + str(self.stroke) + "; "
        if self.stroke_width:
            result += "stroke-width:" + str(self.stroke_width) + "; "
        if self.fill:
            result += "fill:" + str(self.fill) + "; "
        if self.font_size:
            result += "font-size:" + str(self.font_size) + "; "
        if self.font_family:
            result += "font-family:" + str(self.font_family) + "; "
        if self.text_anchor:
            result += "text-anchor:" + str(self.text_anchor) + "; "
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
        self.style = Style(fill="none", stroke="#000000", stroke_width=1.0)

    def draw(self, file_) -> None:
        file_.write("  <path d = \"M " + str(self.x1) + "," + str(self.y1) +
            " " + str(self.x2) + "," + str(self.y2) + "\" ")
        file_.write("style = \"")
        file_.write(str(self.style))
        file_.write("\" />\n")


class Circle(SVGElement):
    def __init__(self, x: float, y: float, d: float) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self.d = d
        self.style = Style(fill="none", stroke="#000000", stroke_width=1.0)

    def draw(self, file_) -> None:
        x = self.x
        y = self.y
        d = self.d
        c = 0.577
        file_.write("""  <path d = "M %5.1f %5.1f C %5.1f %5.1f
                %5.1f %5.1f %5.1f %5.1f C %5.1f %5.1f %5.1f %5.1f %5.1f
                %5.1f C %5.1f %5.1f %5.1f %5.1f %5.1f %5.1f C %5.1f %5.1f
                %5.1f %5.1f %5.1f %5.1f" """ % (
            x, y + d, x - d * c, y + d, x - d, y + d * c, x - d, y, x - d,
            y - d * c, x - d * c, y - d, x, y - d, x + d * c, y - d, x + d,
            y - d * c, x + d, y, x + d, y + d * c, x + d * c, y + d, x,
            y + d))
        file_.write("style = \"")
        file_.write(str(self.style))
        file_.write("\" />\n")


class Text(SVGElement):
    def __init__(self, x: float, y: float, text: str) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self.text = text
        self.style = Style(fill="#000000", stroke="none")

    def draw(self, file_) -> None:
        file_.write("  <text x = \"" + str(self.x) + "\" y = \"" +
            str(self.y) + "\" ")
        file_.write("style = \"")
        file_.write(str(self.style))
        file_.write("\">")
        file_.write(self.text)
        file_.write("</text>\n")


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
