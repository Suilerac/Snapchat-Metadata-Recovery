import ffmpeg
import subprocess
import os


class Video:
    def __init__(self, path):
        self._path = path

    def copy_video(self, path):
        (
            ffmpeg
            .input(self._path)
            .output(path, c="copy")
            .run()
        )
        return Video(path)

    def change_date(self, date):
        temp_path = f"{self._path[:-4].join("")}_temp.mp4"
        (
            ffmpeg
            .input(self._path)
            .output(
                temp_path,
                vcodec="libx264",
                movflags="faststart"
            )
            .run(overwrite_output=True)
        )
        os.replace(temp_path, self._path)
        subprocess.run([
            "exiftool",
            "-overwrite_original",

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

    # def combine(self, input, output):
    #     probe = ffmpeg.probe(self._path)
    #     duration = float(probe["format"]["duration"])
    #     video = ffmpeg.input(self._path)
    #     overlay = ffmpeg.input(input, loop=1)
    #     try:
    #         (
    #             ffmpeg
    #             .overlay(video, overlay)
    #             .output(
    #                 output,
    #                 shortest=None,
    #                 vcodec="libx264",
    #                 acodec="copy",
    #                 t=duration)
    #             .run()
    #         )
    #     except ffmpeg.Error as e:
    #         print(e.stderr)

    def combine(self, input, output):
        base = ffmpeg.input(self._path)
        overlay = ffmpeg.input(input, loop=1)
        (
            ffmpeg
            .overlay(base, overlay)
            .output(output, shortest=None, vcodec="libx264")
            .run()
        )

    @property
    def path(self):
        return self._path
