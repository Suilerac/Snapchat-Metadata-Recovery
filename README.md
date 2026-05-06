
# Snapchat Metadata Recovery

Tools to reconstruct Snapchat Memories exports: combine overlays, restore original capture dates and locations, and produce shareable media files. If you know me personally and don't want to go through the hassle of setting the project up yourself, just reach out to me with the memories zip file and I'll run it for you when I have time yes.

**Why this exists:** Snapchat exports separate "main" media files and overlay files, and they also don't include original timestamp and location metadata. This project recombines them and reapplies original timestamps from the exported metadata so recovered media keep their original dates and location data.

**Features**
- **Combine overlays:** merges overlay images onto video/image main files and saves results to `output/`.
- **Restore dates:** reads `mydata/json/memories_history.json` and writes original capture datetimes to output media files.

**Requirements**
- **Python:** 3.14 or newer (see `pyproject.toml`).
- **FFmpeg:** system `ffmpeg` binary required for video processing.
- **exiftool** required for editing metadata.
- **Python packages:** `ffmpeg-python`, `piexif`, `pillow`, `pyexiv2`, `tqdm` (listed in `pyproject.toml`).

Setup with UV:
```bash
uv venv --python 3.14
source .venv/bin/activate
uv sync
# ensure ffmpeg is installed (e.g. `brew install ffmpeg` on macOS)
# ensure exiftool is installed (e.g. 'brew install exiftool' on macOS)
```

**Quick usage**
1. Export only memories from Snapchat Account Center
2. Extract the zip file, rename folder to mydata
3. Place mydata folder as is into project directory
4. Run main.py

```bash
python main.py
```

Results are written to the `output/` directory.

**Main scripts**
- **Main runner:** [main.py](main.py)
- **Parent class** [src/Mediafile.py](src/Mediafile.py)
- **Image processing:** [src/Image.py](src/Image.py)
- **Video processing:** [src/Video.py](src/Video.py)

**Functions you may call directly**
- `combine_overlays()` — merges overlays and copies files without overlays.
- `restore_metadata()` — reapplies capture datetimes and location coordinates from exported metadata.

**Notes & troubleshooting**
- This was made in a way that kept previewability with my cloud storage provider. I cannot guarantee it's kept with every provider, as I can't test it.
- If videos fail to combine, confirm `ffmpeg` is available on your PATH.
- This has not been extensively tested as the sample size is purely my own exported snapchat memories, with the script running on my macbook. Things can and probably will break.

**Further development**
This is really just a little pet project written in two days for my own personal needs. I probably won't do much more work on it.
