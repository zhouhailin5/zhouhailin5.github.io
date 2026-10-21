"""Remove near-white background from mascot images and save transparent PNGs."""
from PIL import Image
import os

SRC = r"C:\Users\22648\.workbuddy\clipboard-images"
JOBS = [
    ("clipboard-2026-10-21T09-11-23-849Z-92a5f113.png", "pet-idle.png"),
    ("clipboard-2026-10-21T09-11-23-851Z-c62a23c9.png", "pet-heart.png"),
]
OUT = r"D:\blog\my-log\source\img"

def remove_white(im, thresh=235):
    im = im.convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if r >= thresh and g >= thresh and b >= thresh:
                px[x, y] = (r, g, b, 0)
    return im

for src, dst in JOBS:
    p = os.path.join(SRC, src)
    im = Image.open(p)
    print(src, "size:", im.size)
    out = remove_white(im)
    # upscale 2x for smoother display
    out = out.resize((out.width * 2, out.height * 2), Image.LANCZOS)
    out.save(os.path.join(OUT, dst))
    print("saved:", dst, out.size)
