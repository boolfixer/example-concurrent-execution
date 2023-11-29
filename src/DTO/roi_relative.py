#
#
#    x_start_percent
#    y_start_percent              width
#                   ––––––––––––––––––––––––––––––––––––
#                   |                                  |
#                   |                                  |
#                 h |                                  |
#                 e |              ROI                 |
#                 i |                                  |
#                 g |       region of interest         |
#                 h |                                  |
#                 t |                                  |
#                   |                                  |
#                   |                                  |
#                   ––––––––––––––––––––––––––––––––––––
#                                                       x_end_percent
#                                                       y_end_percent
#
#
from __future__ import annotations

import json

from src.DTO.resolution import Resolution
from src.DTO.roi_absolute import RoiAbsolute


class RoiRelative:
    def __init__(self, x_start_percent: float, y_start_percent: float, width: int, height: int):
        self.__x_start_percent = x_start_percent
        self.__y_start_percent = y_start_percent
        self.__width = width
        self.__height = height

    def get_x_start_percent(self) -> float:
        return self.__x_start_percent

    def get_y_start_percent(self) -> float:
        return self.__y_start_percent

    def get_width(self) -> float:
        return self.__width

    def get_height(self) -> float:
        return self.__height

    def to_roi_absolute(self, resolution: Resolution) -> RoiAbsolute:
        return RoiAbsolute(
            int(resolution.width * self.__x_start_percent),
            int(resolution.height * self.__y_start_percent),
            self.__width,
            self.__height
        )

    @staticmethod
    def from_mavlink_message(msg: str) -> None | RoiRelative:
        data = json.loads(msg)

        if data['id'] != 'ROI':
            return None

        roi = data['value']
        roi = roi.replace('TRGT,', '')
        roi = roi.replace(',#', '')
        roi = roi.split(',', 2)

        x_start_percent = float(roi[0])
        y_start_percent = float(roi[1])
        width = 50
        height = 50

        return RoiRelative(
            x_start_percent,
            y_start_percent,
            width,
            height
        )
