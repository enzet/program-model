import math


class Vector:
    """
    2D vector.
    """
    def __init__(self, x: float=0, y: float=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def length(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def norm(self):
        return Vector(self.x / self.length(), self.y / self.length())

    def rotate(self, angle):
        return Vector(self.x * math.cos(angle) - self.y * math.sin(angle),
            self.x * math.sin(angle) + self.y * math.cos(angle))
