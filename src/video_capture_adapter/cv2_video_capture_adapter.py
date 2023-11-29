import cv2
from numpy import ndarray

from src.DTO.resolution import Resolution
from src.utils.logger import Logger
from src.video_capture_adapter.video_capture_adapter import VideoCaptureAdapter


class Cv2VideoCaptureAdapter(VideoCaptureAdapter):
    __video_capture: cv2.VideoCapture = None
    __logger: Logger = None

    def __init__(self):
        self.__video_capture = cv2.VideoCapture(0)
        self.__logger = Logger()

        if not self.__video_capture.isOpened():
            raise Exception('Failed to init video capture.')

        self.__resolution = Resolution(
            width=int(self.__video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            height=int(self.__video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        )

    def capture_continuous(self) -> ndarray:
        while self.__video_capture.isOpened():
            succeed, frame = self.__video_capture.read()

            if succeed:
                yield frame
            else:
                exception_message = 'Failed to read a frame.'
                self.__logger.exception = exception_message
                self.__logger.flush()

                raise Exception(exception_message)

        exception_message = 'Video capture is closed.'
        self.__logger.exception = exception_message
        self.__logger.flush()

        raise Exception(exception_message)

    def get_resolution(self) -> Resolution:
        return self.__resolution
