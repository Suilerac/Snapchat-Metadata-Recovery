import ffmpeg
import subprocess
import os
from .Mediafile import Mediafile


class Video(Mediafile):
    def __init__(self, path):
        """
        Class for handling a video file

        :param path: Path-string to video file
        """
        super().__init__(path)

    def copy_file(self, path):
        """
        Copies file to target path

        :param path: Path-string to target destination
        """
        (
            ffmpeg
            .input(self._path, loglevel='quiet')
            .output(path, c="copy")
            .run()
        )
        return Video(path)


    def update_metadata(self, date, lat, lon):
        """
        Changes the exif metadata of the video
        to chosen date and location.
         
        :param date: Date-string of format YYYY:MM:DD HH:MM:SS
        :param lat: Latitude
        :param lon: Longitude
        """
        temp_path = f"{self._path[:-4].join("")}_temp.mp4"
        (
            ffmpeg
            .input(self._path, loglevel="quiet")
            .output(
                temp_path,
                vcodec="libx264",
                movflags="faststart"
            )
            .run(overwrite_output=True)
        )
        os.replace(temp_path, self._path)

        if lat == 0 and lon == 0:  # No location metadata
            subprocess.run([
                "exiftool",
                "-overwrite_original",
                "-quiet",

                # QuickTime container dates
                f"-QuickTime:CreateDate={date}",
                f"-QuickTime:ModifyDate={date}",
                f"-QuickTime:TrackCreateDate={date}",
                f"-QuickTime:MediaCreateDate={date}",

                # Apple / iOS ecosystem
                f"-Keys:CreationDate={date}",

                # File system timestamps
                f"-FileCreateDate={date}",
                f"-FileModifyDate={date}",

                self._path
            ], check=True)
        else:
            subprocess.run([
                "exiftool",
                "-overwrite_original",
                "-quiet",

                # QuickTime container dates
                f"-QuickTime:CreateDate={date}",
                f"-QuickTime:ModifyDate={date}",
                f"-QuickTime:TrackCreateDate={date}",
                f"-QuickTime:MediaCreateDate={date}",

                # Apple / iOS ecosystem
                f"-Keys:CreationDate={date}",

                # File system timestamps
                f"-FileCreateDate={date}",
                f"-FileModifyDate={date}",

                f"-QuickTime:GPSCoordinates={lat},{lon}",
                f"-Keys:GPSCoordinates={lat},{lon}",

                self._path], check=True)

    def combine(self, input, output):
        """
        Combines overlay on top of video

        :param input: Overlay file path
        :param output: Final combination path
        """
        probe = ffmpeg.probe(self._path)
        duration = float(probe["format"]["duration"])
        video_stream = next(s for s in probe["streams"] if s["codec_type"] == "video")

        # base_w = int(video_stream["width"])
        # base_h = int(video_stream["height"])
        resolution = (int(video_stream["width"]), int(video_stream["height"]))
        base_w = min(resolution)
        base_h = max(resolution)

        base = ffmpeg.input(self._path)
        base_video = base.video
        base_audio = base.audio

        overlay = (
            ffmpeg
            .input(input, loop=1, t=duration)
            .filter(
                'scale',
                f'if(gt(iw/ih,{base_w}/{base_h}),-1,{base_w})',
                f'if(gt(iw/ih,{base_w}/{base_h}),{base_h},-1)'
            )
            .filter(
                'crop',
                base_w,
                base_h,
                f'(iw-{base_w})/2',
                f'(ih-{base_h})/2'
            )
        )

        video = ffmpeg.filter([base_video, overlay], 'overlay', x=0, y=0)

        (
            ffmpeg
            .output(video, base_audio, output, vcodec="libx264", acodec="aac", shortest=None)
            .global_args("-loglevel", "quiet")
            .run(overwrite_output=True)
        )

        return Video(output)
