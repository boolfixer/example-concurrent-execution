from cv2 import VideoCapture
from numpy import ndarray

from config.video_resource_config import VideoResourceConfig
from src.DTO.resolution import Resolution
from src.video_capture_adapter.video_capture_adapter import VideoCaptureAdapter


class FileVideoCaptureAdapter(VideoCaptureAdapter):
    __video_capture: VideoCapture = None

    def __init__(self):
        self.__config = VideoResourceConfig()
        self.__resolution = Resolution(width=self.__config.resolution_width, height=self.__config.resolution_height)

    def capture_continuous(self) -> ndarray:
        self.__video_capture: VideoCapture = VideoCapture(self.__config.file_path)

        while True:
            success, frame = self.__video_capture.read()

            if success:
                yield frame
            else:  # Stream ends
                self.__video_capture: VideoCapture = VideoCapture(self.__config.file_path)  # start from the beginning

    def get_resolution(self) -> Resolution:
        return self.__resolution
