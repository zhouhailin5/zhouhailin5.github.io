"""Refine pet-heart.png: remove grayish halo + residual text, crop to content."""
from PIL import Image

p = r"D:\blog\my-log\source\img\pet-heart.png"
im = Image.open(p).convert("RGBA")
px = im.load()
w, h = im.size

def grayish(r, g, b):
    mx, mn = max(r, g, b), min(r, g, b)
    return mx - mn < 34 and mx > 105

for y in range(h):
    for x in range(w):
        r, g, b, a = px[x, y]
        if a == 0:
            continue
        if grayish(r, g, b):
            px[x, y] = (r, g, b, 0)

# hard-clear bottom-right corner where the "gif" watermark sits
for y in range(int(h * 0.82), h):
    for x in range(int(w * 0.70), w):
        r, g, b, a = px[x, y]
        if a != 0:
            mx, mn = max(r, g, b), min(r, g, b)
            if mx - mn < 45 and mx > 85:
                px[x, y] = (r, g, b, 0)

bbox = im.getbbox()
im = im.crop(bbox)
im.save(p)
print("refined:", im.size)
