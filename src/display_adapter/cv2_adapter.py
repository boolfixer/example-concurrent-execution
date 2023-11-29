import cv2
from numpy import ndarray

from src.display_adapter.display_adapter import DisplayAdapter


class Cv2DisplayAdapter(DisplayAdapter):
    __window_name = "Window"

    def display(self, frame: ndarray):
        cv2.namedWindow(self.__window_name, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(self.__window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow(self.__window_name, frame)
        cv2.waitKey(1)
