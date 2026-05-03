import pyexiv2 as pe2
import shutil
from src.Log import Log
from PIL import Image


class Image:
    def __init__(self, path):
        self._path = path
        self._log = Log()


    def change_date(self, new_date):
        DTO_KEY = "Exif.Photo.DateTimeOriginal"

        with pe2.Image(self._path) as img:
            exif = img.read_exif()
            try:
                dto = exif[DTO_KEY]
            except KeyError as e:
                self._log.warning("No existing datetime metadata found")
            img.modify_exif({DTO_KEY: new_date})


    def get_date(self):
        DTO_KEY = "Exif.Photo.DateTimeOriginal"

        with pe2.Image(self._path) as img:
            exif = img.read_exif()
            try:
                dto = exif[DTO_KEY]
            except KeyError as e:
                raise KeyError("No DateTime metadata found") from e
            return dto


    def copy_image(self, path):
        shutil.copy(self._path, path)
        return Image(path)


    @property
    def path(self):
        return self._path
