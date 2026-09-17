"""Stitch the chunked captures from shoot.mjs into one PNG per page, width and theme."""
import glob
import os
import re

from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".redesign-preview")
groups = {}
for part in sorted(glob.glob(os.path.join(OUT, "*.part*.png"))):
    key = re.sub(r"\.part\d+\.png$", "", part)
    groups.setdefault(key, []).append(part)
for key, parts in groups.items():
    parts.sort(key=lambda p: int(re.search(r"part(\d+)", p).group(1)))
    images = [Image.open(p) for p in parts]
    sheet = Image.new("RGB", (images[0].width, sum(i.height for i in images)))
    y = 0
    for image in images:
        sheet.paste(image, (0, y))
        y += image.height
    sheet.save(key + ".png")
    for p in parts:
        os.remove(p)
    print(os.path.basename(key) + f".png {sheet.width}x{sheet.height}")
