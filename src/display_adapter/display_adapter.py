from abc import ABC, abstractmethod


class DisplayAdapter(ABC):
    @abstractmethod
    def display(self, frame): ...
