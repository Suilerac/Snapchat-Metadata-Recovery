import os

test = "test.mp4"
name, ext = os.path.splitext(test)
print(ext == ".mp4")