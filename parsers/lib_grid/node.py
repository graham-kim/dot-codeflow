from dataclasses import dataclass

class Coords:
    def __init__(self, in_x: int, in_y: int):
        self._xy = (in_x, in_y)

    @property
    def x(self) -> int:
        return self._xy[0]

    @property
    def y(self) -> int:
        return self._xy[1]

    @property
    def hash(self) -> int:
        return self.x * 1000 + self.y

    def __str__(self) -> str:
        return f"(x{self.x}, y{self.y})"


@dataclass
class Node:
    name: str
    category: str
    label: str
    xy: Coords
    invis: bool
