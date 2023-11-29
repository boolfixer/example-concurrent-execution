from typing import NamedTuple


class Resolution(NamedTuple):
    width: int
    height: int

    def width_center(self) -> int:
        return int(self.width * 0.5)

    def height_center(self) -> int:
        return int(self.height * 0.5)
