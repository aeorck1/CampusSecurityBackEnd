from enum import Enum as BaseEnum


class Enum(BaseEnum):

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str(self.name)

    @classmethod
    def mapping(cls):
        return {e.name: e.value for e in cls}

