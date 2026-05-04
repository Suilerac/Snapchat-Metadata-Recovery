import ffmpeg
import subprocess
import os


class Video:
    def __init__(self, path):
        """
        Class for handling a video file

        :param path: Path-string to video file
        """
        self._path = path

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

    def change_date(self, date):
        """
        Changes the exif metadata of the video
        to chosen date.
         
        :param date: Date-string of format YYYY:MM:DD HH:MM:SS
        """
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
    #     """
    #     Overlays input video on top of self, outputting to
    #     output path.

    #     :param input: Path-string to target overlay
    #     :param output: Path-string to output file
    #     """
    #     probe = ffmpeg.probe(self._path)
    #     duration = float(probe["format"]["duration"])
    #     video_stream = next(s for s in probe["streams"] if s["codec_type"] == "video")

    #     base_h = int(video_stream["width"])
    #     base_w = int(video_stream["height"])

    #     base = ffmpeg.input(self._path)
    #     base_video = base.video
    #     base_audio = base.audio
    #     overlay = (
    #         ffmpeg
    #         .input(input, loop=1, t=duration)
    #         .filter('scale', base_w, base_h)
    #         .filter('crop', base_w, base_h)
    #     )
        
    #     try:
    #         (
    #             ffmpeg
    #             .filter([base_video, overlay], 'overlay', x=0, y=0)
    #             .output(base_audio, output, vcodec="libx264", acodec="aac", shortest=None)
    #             .global_args("-loglevel", "quiet")
    #             .run()
    #         )
    #     except ffmpeg.Error as e:
    #         print(e.stderr)

    #     return Video(output)

    def combine(self, input, output):
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

    @property
    def path(self):
        return self._path
