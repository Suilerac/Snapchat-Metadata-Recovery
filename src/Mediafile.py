from abc import ABC, abstractmethod


class Mediafile(ABC):
    def __init__(self, path):
        self._path = path

    @abstractmethod
    def update_metadata(self, date, lat, lon):
        pass

    @abstractmethod
    def copy_file(self, path):
        pass

    def _to_dms(self, value):
        deg = int(value)
        min_float = (value - deg) * 60
        min = int(min_float)
        sec = ((min_float - min) * 60)
        return f"{deg}/1 {min}/1 {int(sec * 100)}/100"

    @property
    def path(self):
        return self._path