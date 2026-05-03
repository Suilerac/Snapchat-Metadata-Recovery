import json
import os
import PIL
from src.Image import Image
from src.Video import Video
from tqdm import tqdm


def combine_overlays():
    target_dir = "mydata/memories"
    targets = sorted(os.listdir(target_dir))[:-1]
    for i in range(len(targets)):
        target_path = f"{target_dir}/{targets[i]}"
        if "overlay" in target_path:
            base_path = f"{target_dir}/{targets[i-1]}"
            base = PIL.Image.open(base_path).convert("RGBA")
            overlay = PIL.Image.open(target_path).convert("RGBA")

            combined = PIL.Image.alpha_composite(base, overlay)
            combined.save(f"temp_output/{targets[i-1]}")


def main():
    target_dir = "mydata/memories"
    with open("mydata/json/memories_history.json") as f:
        data = reversed(json.load(f)["Saved Media"])
    targets = sorted(os.listdir(target_dir))[:-1]
    print(len(data))
    print(len(targets))
    for i in len(targets):
        dir = f"{target_dir}/{targets[i]}"
        target_data = data[i]


if __name__ == "__main__":
    main()
