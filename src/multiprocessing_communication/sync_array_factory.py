from multiprocessing import Array

from config.application_config import ApplicationConfig


class SyncArrayFactory:
    def __init__(self):
        config = ApplicationConfig()

        self.__init_char = config.sync_array_init_char
        self.__size = config.sync_array_size

    def create(self):
        return Array('u', self.__init_char * self.__size)
