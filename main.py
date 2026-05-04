import json
import os
from pathlib import Path
from src.Image import Image
from src.Video import Video
from tqdm import tqdm


def combine_overlays():
    target_dir = "mydata/memories"
    output_dir = "temp_output"
    targets = sorted(os.listdir(target_dir))[:-1]
    for target in tqdm(targets, desc="Combining overlays"):
        if "overlay" in target:
            continue
        target_path = f"{target_dir}/{target}"
        name, ext = os.path.splitext(target)
        if ext == "jpg" or ext == "png":
            file = Image(target_path)
            name, _ = os.path.splitext(target)
            output = f"{name.replace("main", '')}.png"
        else:
            file = Video(target_path)
            output = target.replace("main", '')
        output_path = f"{output_dir}/{output}"
        overlay = f"{name.replace("main", '')}overlay.png"
        if overlay in targets:
            file.combine(f"{target_dir}/{overlay}", output_path)
        else:
            file.copy_file(output_path)


def main():
    target_dir = "mydata/memories"
    with open("mydata/json/memories_history.json") as f:
        data = reversed(json.load(f)["Saved Media"])
    Path("temp_output").mkdir(exist_ok=True)
    combine_overlays()


if __name__ == "__main__":
    main()
