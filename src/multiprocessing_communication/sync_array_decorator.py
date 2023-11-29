SEPARATOR = ';'


class SyncArrayDecorator:
    def __init__(self, sync_array, init_char):
        self.__init_char = init_char
        self.__sync_array = sync_array

    def read(self) -> tuple[str, ...]:
        concat_values = ''

        with self.__sync_array.get_lock():
            for char in self.__sync_array:
                if char != self.__init_char:
                    concat_values += char

            self.__reset()

            if len(concat_values) > 0:
                return tuple(concat_values.split(SEPARATOR))

            return tuple()

    def write(self, *args) -> None:
        with self.__sync_array.get_lock():
            self.__reset()

            concat_arguments = SEPARATOR.join(args)

            for index, _ in enumerate(concat_arguments):
                self.__sync_array[index] = concat_arguments[index]

    def __reset(self) -> None:
        for index, _ in enumerate(self.__sync_array):
            self.__sync_array[index] = self.__init_char
