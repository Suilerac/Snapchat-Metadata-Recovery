import json
import os
from pathlib import Path
from src.Image import Image
from src.Video import Video
from tqdm import tqdm


def combine_overlays():
    """
    Combines overlays on all files that have them,
    and otherwise copies the files over to output
    """
    target_dir = "mydata/memories"
    output_dir = "output"
    targets = sorted(os.listdir(target_dir))[:-1]
    for target in tqdm(targets, desc="Combining overlays"):
        # Overlays get combined later
        if "overlay" in target:
            continue
        target_path = f"{target_dir}/{target}"
        name, ext = os.path.splitext(target)
        # Images and videos require different techniques
        if ext == ".mp4":
            file = Video(target_path)
            output = target.replace("-main", '')
        else:
            file = Image(target_path)
            name, _ = os.path.splitext(target)
            output = f"{name.replace("-main", '')}.png"
        output_path = f"{output_dir}/{output}"
        overlay = name.replace("main", 'overlay.png')
        if overlay in targets:
            file.combine(f"{target_dir}/{overlay}", output_path)
        else:
            file.copy_file(output_path)


def restore_dates():
    target_dir = "output"
    targets = sorted(os.listdir(target_dir))
    with open("mydata/json/memories_history.json") as f:
        data = json.load(f)["Saved Media"]
    file_data_pairs = zip(targets, reversed(data))
    pbar = tqdm(total=len(targets), desc="Restoring dates")
    for filename, info in tqdm(file_data_pairs, desc="Restoring dates"):
        datetime = info["Date"].split(" ")[:-1]  # Separate date and time, exclude UTC
        date = datetime[0].replace("-", ":")  # Adapt to fit form
        time = datetime[1]  # Already fits form
        datetime = f"{date} {time}"
        _, ext = os.path.splitext(filename)
        if ext == ".mp4":
            file = Video(f"{target_dir}/{filename}")
        else:
            file = Image(f"{target_dir}/{filename}")
        file.change_date(datetime)
        pbar.update(1)
    pbar.close()


def combine_overlays_videos():
    """
    Combines overlays only on videos,
    purely for debugging
    """
    target_dir = "mydata/memories"
    output_dir = "output"
    targets = sorted(os.listdir(target_dir))[:-1]
    for target in tqdm(targets, desc="Combining overlays"):
        name, ext = os.path.splitext(target)
        if ext != ".mp4":
            continue
        target_path = f"{target_dir}/{target}"
        vid = Video(target_path)
        overlay = name.replace("main", "overlay.png")
        overlay_path = f"{target_dir}/{overlay}"
        output_path = f"{output_dir}/{target}"
        if overlay in targets:
            vid.combine(overlay_path, output_path)


def get_overlay_list():
    """
    Writes out a list of files with overlays,
    purely for debugging
    """
    target_dir = "mydata/memories"
    targets = sorted(os.listdir(target_dir))[:-1]
    with open("Overlays.txt", 'w') as f:
        for target in targets:
            if "overlay" in target:
                vid = target.replace("overlay.png", "main.mp4")
                if vid in targets:
                    f.write(vid)
                    f.write('\n')


def main():
    Path("output").mkdir(exist_ok=True)
    combine_overlays()
    restore_dates()


if __name__ == "__main__":
    main()
