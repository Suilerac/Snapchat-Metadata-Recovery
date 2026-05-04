
# Snapchat Metadata Recovery

Tools to reconstruct Snapchat Memories exports: combine overlays, restore original capture dates, and produce shareable media files.

**Why this exists:** Snapchat exports separate "main" media files and overlay files, and they also don't include original timestamp and location metadata. This project recombines them and reapplies original timestamps from the exported metadata so recovered media keep their original dates. At the moment it does not recover location data.

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
- **Image processing:** [src/Image.py](src/Image.py)
- **Video processing:** [src/Video.py](src/Video.py)

**Functions you may call directly**
- `combine_overlays()` — merges overlays and copies files without overlays.
- `restore_dates()` — reapplies capture datetimes from exported metadata.
- `combine_overlays_videos()` — debug helper to combine overlays only for videos.
- `get_overlay_list()` — writes `Overlays.txt` listing video files that have overlays.

**Notes & troubleshooting**
- Currently this does not restore location data, only timestamps
- This was made in a way that kept previewability with my cloud storage provider. I cannot guarantee it's kept with every provider, as I can't test it.
- If videos fail to combine, confirm `ffmpeg` is available on your PATH.
- This has not been extensively tested as the sample size is purely my own exported snapchat memories. Things can and probably will break.

**Further development**
This is really just a little pet project written in two days for my own personal needs. I might add location data restoration as well, but I won't do much work on this beyond that.
