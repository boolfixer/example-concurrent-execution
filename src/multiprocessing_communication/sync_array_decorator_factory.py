from config.application_config import ApplicationConfig
from src.multiprocessing_communication.sync_array_decorator import SyncArrayDecorator


class SyncArrayDecoratorFactory:
    def __init__(self):
        self.__init_char = ApplicationConfig().sync_array_init_char

    def create(self, sync_array) -> SyncArrayDecorator:
        return SyncArrayDecorator(sync_array, self.__init_char)
