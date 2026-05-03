import pyexiv2 as pe2
import shutil
from PIL import Image as PILImage


class Image:
    def __init__(self, path):
        self._path = path

    def change_date(self, new_date, change_modified=True):
        DTO_KEY = "Exif.Photo.DateTimeOriginal"

        with pe2.Image(self._path) as img:
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

    def combine(self, input, output):
        base = PILImage.open(self._path).convert("RGBA")
        overlay = PILImage.open(input).convert("RGBA")

        if overlay.size != base.size:
            overlay = overlay.resize(base.size)

        combined = PILImage.alpha_composite(base, overlay)
        combined.save(output)
        return Image(output)

    @property
    def path(self):
        return self._path
