"""Extract mascot poses from reference images.
Flood-fill white bg from borders (preserves cream belly), corner cleanup, crop, 2x upscale.
"""
from PIL import Image
from collections import deque
import os

SRC = r"C:\Users\22648\.workbuddy\clipboard-images"
OUT = r"D:\blog\my-log\source\img"

def near_white(r, g, b, thresh=232):
    return r >= thresh and g >= thresh and b >= thresh

def flood_clear(im):
    """BFS from all border pixels; clear connected near-white region."""
    im = im.convert("RGBA")
    w, h = im.size
    px = im.load()
    visited = bytearray(w * h)
    q = deque()
    for x in range(w):
        q.append((x, 0)); q.append((x, h - 1))
    for y in range(h):
        q.append((0, y)); q.append((w - 1, y))
    while q:
        x, y = q.popleft()
        if x < 0 or x >= w or y < 0 or y >= h:
            continue
        i = y * w + x
        if visited[i]:
            continue
        visited[i] = 1
        r, g, b, a = px[x, y]
        if not near_white(r, g, b):
            continue
        px[x, y] = (r, g, b, 0)
        q.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])
    return im

def corner_clear(im, boxes):
    """Clear residual watermark/grayish areas in given boxes (fractions)."""
    px = im.load()
    w, h = im.size
    for fx0, fy0, fx1, fy1 in boxes:
        for y in range(int(h*fy0), int(h*fy1)):
            for x in range(int(w*fx0), int(w*fx1)):
                r, g, b, a = px[x, y]
                if a == 0:
                    continue
                mx, mn = max(r, g, b), min(r, g, b)
                if mx - mn < 45 and mx > 85:
                    px[x, y] = (r, g, b, 0)
    return im

JOBS = [
    # (src, dst, corner_boxes, crop_bottom_frac, crop_right_frac)
    ("clipboard-2026-10-21T09-56-05-845Z-c3117924.png", "pet-lion.png",
     [(0.75, 0.88, 1.0, 1.0)], 0.0, 0.0),
    ("clipboard-2026-10-21T09-56-05-846Z-c89479ff.png", "pet-balance.png",
     [(0.0, 0.0, 0.28, 0.30)], 0.22, 0.0),
]

for src, dst, boxes, cb, cr in JOBS:
    im = Image.open(os.path.join(SRC, src))
    print(src, "orig:", im.size)
    if cb:
        im = im.crop((0, 0, int(im.width * (1 - cr)), int(im.height * (1 - cb))))
    im = flood_clear(im)
    im = corner_clear(im, boxes)
    bbox = im.getbbox()
    im = im.crop(bbox)
    im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS)
    im.save(os.path.join(OUT, dst))
    print("saved:", dst, im.size)
