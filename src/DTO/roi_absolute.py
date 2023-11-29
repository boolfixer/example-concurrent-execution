#
#
#    x_start
#    y_start               width
#           ––––––––––––––––––––––––––––––––––––
#           |                                  |
#           |                                  |
#         h |                                  |
#         e |              ROI                 |
#         i |                                  |
#         g |       region of interest         |
#         h |                                  |
#         t |                                  |
#           |                                  |
#           |                                  |
#           ––––––––––––––––––––––––––––––––––––
#                                               x_end
#                                               y_end
#
#
from __future__ import annotations

from src.DTO.coordinate import Coordinate


class RoiAbsolute:
    def __init__(self, x_start: int, y_start: int, width: int, height: int):
        self.__x_start = x_start
        self.__y_start = y_start
        self.__width = width
        self.__height = height

        self.__x_end = x_start + width
        self.__y_end = y_start + height

        self.__x_center = x_start + int(width / 2)
        self.__y_center = y_start + int(height / 2)

    def get_x_start(self) -> float:
        return self.__x_start

    def get_y_start(self) -> float:
        return self.__y_start

    def get_width(self) -> float:
        return self.__width

    def get_height(self) -> float:
        return self.__height

    def start(self) -> Coordinate:
        return Coordinate(x=self.__x_start, y=self.__y_start)

    def end(self) -> Coordinate:
        return Coordinate(x=self.__x_end, y=self.__y_end)

    def center(self) -> Coordinate:
        return Coordinate(x=self.__x_center, y=self.__y_center)

    def to_rectangle_2d(self) -> tuple[int, int, int, int]:
        return self.__x_start, self.__y_start, self.__width, self.__height

    @staticmethod
    def from_boarding_box(boarding_box: tuple[int, int, int, int]) -> RoiAbsolute:
        return RoiAbsolute(
            x_start=boarding_box[0],
            y_start=boarding_box[1],
            width=boarding_box[2],
            height=boarding_box[3],
        )
