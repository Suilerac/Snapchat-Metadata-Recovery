import json
import os
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
        if ".jpg" in target or ".png" in target:
            file = Image(target_path)
            output = f"{target.replace("main", '')[:-4].join('')}.png"
        else:
            file = Video(target_path)
            output = target.replace("main", '')
        output_path = f"{output_dir}/{output}"
        overlay = f"{output[:-4]}overlay.png"
        if overlay in targets:
            file.combine(f"{target_dir}/{overlay}", output_path)
        else:
            file.copy_file(output_path)


def main():
    target_dir = "mydata/memories"
    with open("mydata/json/memories_history.json") as f:
        data = reversed(json.load(f)["Saved Media"])
    combine_overlays()


if __name__ == "__main__":
    main()
