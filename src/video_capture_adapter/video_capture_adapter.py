from abc import ABC, abstractmethod

from numpy import ndarray

from src.DTO.resolution import Resolution


class VideoCaptureAdapter(ABC):
    @abstractmethod
    def capture_continuous(self) -> ndarray: ...

    @abstractmethod
    def get_resolution(self) -> Resolution: ...
