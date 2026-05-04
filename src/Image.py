import pyexiv2 as pe2
import shutil
from .Mediafile import Mediafile
from PIL import Image as PILImage


class Image(Mediafile):
    def __init__(self, path):
        """
        Class for handling images

        :param path: Path-string to image file
        """
        super().__init__(path)

    def update_metadata(self, date, lat, lon):
        """
        Changes exif metadata of creation date to target date

        :param new_date: target date, string, format YYYY:MM:DD HH:MM:SS
        """
        DTO_KEY = "Exif.Photo.DateTimeOriginal"
        GPS = "Exif.GPSInfo.GPS"

        latdms = self._to_dms(lat)
        londms = self._to_dms(lon)
        latref = "N" if lat >= 0 else "S"
        lonref = "E" if lon >= 0 else "W"

        if lat == 0 and lon == 0:  # No location metadata
            with pe2.Image(self._path) as img:
                img.modify_exif({
                    DTO_KEY: date
                })
            return

        with pe2.Image(self._path) as img:
            img.modify_exif({
                DTO_KEY: date,
                f"{GPS}Latitude": latdms,
                f"{GPS}LatitudeRef": latref,
                f"{GPS}Longitude": londms,
                f"{GPS}LongitudeRef": lonref
                })

    def get_date(self):
        """
        Gets the current creation date given by exif metadata
        """
        DTO_KEY = "Exif.Photo.DateTimeOriginal"

        with pe2.Image(self._path) as img:
            exif = img.read_exif()
            try:
                dto = exif[DTO_KEY]
            except KeyError as e:
                raise KeyError("No DateTime metadata found") from e
            return dto

    def get_location(self):
        """
        Gets the current location given by exif metadata
        """
        LAT_KEY = "Exif.GPSInfo.GPSLatitude"
        LON_KEY = "Exif.GPSInfo.GPSLongitude"

        with pe2.Image(self._path) as img:
            exif = img.read_exif()
            try:
                lat = exif[LAT_KEY]
                lon = exif[LON_KEY]
            except KeyError as e:
                raise KeyError("No DateTime metadata found") from e
            return (lat, lon)

    def copy_file(self, path):
        """
        Copies image file to target path

        :param path: Path-string to target output
        """
        shutil.copy(self._path, path)
        return Image(path)

    def combine(self, input, output):
        """
        Overlays input image on top of self, leading to output image.

        :param input: Path-string to input image to overlay
        :param output: Path-string to output image
        """
        base = PILImage.open(self._path).convert("RGBA")
        overlay = PILImage.open(input).convert("RGBA")

        if overlay.size != base.size:
            overlay = overlay.resize(base.size)

        combined = PILImage.alpha_composite(base, overlay)
        combined.save(output)
        return Image(output)
