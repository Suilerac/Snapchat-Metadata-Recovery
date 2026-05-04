import os
from tqdm import tqdm
from src.Image import Image
from src.Video import Video


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