"""Build the landing page's device imagery from real app captures.

    python3 _tools/build_screens.py            # rebuild every slot
    python3 _tools/build_screens.py home swipe # rebuild only these slots

Every image the landing page shows lives in img/screens/ and is produced here.
To swap a screen, point its entry in SOURCES at a new capture (a raw simulator or
device screenshot, 1206x2622 or 1320x2868, light appearance, English) and run
the script. Nothing in index.html needs to change: the page references the slot
names below, never the capture file names.

Slots (documented names, referenced by index.html):

    home      the Home tab                      -> img/screens/home-{360,540,720}.webp
    swipe     the Swipe tab mid-gesture         -> img/screens/swipe-*.webp
    smart     Smart Clean, a similar-photos group -> img/screens/smart-*.webp
    deleted   the Deleted tab with a selection  -> img/screens/deleted-*.webp
    discover  the Discover tab                  -> img/screens/discover-*.webp
    stats-streak, stats-progress
              two crops of the Home capture (the streak and level card, the
              library progress card), used by the Statistics section until an
              English Statistics capture exists -> img/screens/stats-*-{720,1080}.webp

Each phone slot is composited into the real iPhone frame (_tools/frames/Silver.png,
1470x3000, screen aperture 1320x2868 at (75, 66), the same art and method as the
Pdfino site and the ASO pipeline) and exported as lossy WebP with alpha at the
widths in PHONE_WIDTHS. The rendered page shows a phone at 300 px or narrower, so
720 px covers 2x displays.

PATCHES fixes one simulator artefact: the iOS simulator has no emoji font, so the
waving hand after the greeting renders as a "missing glyph" box. The patch paints
the box out with the surrounding page colour and draws the real emoji with
Apple Color Emoji. Remove the entry (or the whole PATCHES dict) once the capture
comes from a device or a final store render.

Requires Pillow with WebP, numpy and scipy (all present on the build Mac).
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
OUT = os.path.join(SITE, "img", "screens")
CAPTURES = os.path.expanduser("~/Developer/Kipply/.redesign-work")

# slot -> capture path. Edit these to swap a screen.
SOURCES = {
    "home": f"{CAPTURES}/wave2/home-top-en-light.png",
    "swipe": f"{CAPTURES}/wave3/WP3/SW5-drag-delete-en-light.png",
    "smart": f"{CAPTURES}/wave3/wp4/SM11-smart-similar-en-light.png",
    "deleted": f"{CAPTURES}/wave3/WP3/D4-selection-en-light.png",
    "discover": f"{CAPTURES}/wave3/wp4/DI1-discover-feed-en-light.png",
}

# slot -> (source slot, crop box as fractions of the screen width and height)
CROPS = {
    "stats-streak": ("home", (0.020, 0.1335, 0.980, 0.2563)),
    "stats-progress": ("home", (0.020, 0.4977, 0.980, 0.5957)),
}

# slot -> list of (kind, box in the capture's own pixels, payload)
PATCHES = {
    "home": [("emoji", (486, 162, 553, 229), "\U0001F44B")],
}

FRAME = {"file": os.path.join(HERE, "frames", "Silver.png"), "origin": (75, 66), "screen": (1320, 2868)}
PHONE_WIDTHS = (360, 540, 720)
CROP_WIDTHS = (720, 1080)
WEBP = {"quality": 82, "method": 6}
EMOJI_FONT = "/System/Library/Fonts/Apple Color Emoji.ttc"


def aperture_mask(frame, origin, screen):
    """The frame PNG's alpha carries the exact screen aperture; keep only the hole
    that does not touch the image border (the outside is transparent too)."""
    alpha = np.asarray(frame)[:, :, 3]
    labels, _ = ndimage.label(alpha == 0)
    border = set(labels[0, :]) | set(labels[-1, :]) | set(labels[:, 0]) | set(labels[:, -1])
    border.discard(0)
    aperture = (alpha == 0) & ~np.isin(labels, list(border))
    x0, y0 = origin
    return Image.fromarray(aperture[y0:y0 + screen[1], x0:x0 + screen[0]].astype(np.uint8) * 255)


def patch_emoji(capture, box, emoji):
    """Paint the missing-glyph box out with the page colour sampled just outside it,
    then draw the emoji at the box's height."""
    x0, y0, x1, y1 = box
    pixels = np.asarray(capture).astype(np.float32)
    left = pixels[y0:y1, x0 - 3:x0].mean(axis=1)
    right = pixels[y0:y1, x1:x1 + 3].mean(axis=1)
    t = np.linspace(0.0, 1.0, x1 - x0)[None, :, None]
    fill = left[:, None, :] * (1 - t) + right[:, None, :] * t
    pixels[y0:y1, x0:x1] = fill
    patched = Image.fromarray(pixels.round().astype(np.uint8))
    font = ImageFont.truetype(EMOJI_FONT, 160)
    glyph = Image.new("RGBA", (220, 220), (0, 0, 0, 0))
    ImageDraw.Draw(glyph).text((20, 20), emoji, font=font, embedded_color=True)
    glyph = glyph.crop(glyph.getbbox())
    height = y1 - y0
    glyph = glyph.resize((round(glyph.width * height / glyph.height), height), Image.LANCZOS)
    patched.paste(glyph, (x0 + (x1 - x0 - glyph.width) // 2, y0), glyph)
    return patched


def load_screen(slot):
    path = SOURCES[slot]
    capture = Image.open(path).convert("RGBA")
    for kind, box, payload in PATCHES.get(slot, []):
        if kind == "emoji":
            capture = patch_emoji(capture.convert("RGB"), box, payload).convert("RGBA")
    if capture.size != FRAME["screen"]:
        # 1206x2622 (iPhone 17 Pro) and 1320x2868 (Pro Max) share the aspect to 0.1%.
        capture = capture.resize(FRAME["screen"], Image.LANCZOS)
    return capture


def save_widths(image, slot, widths):
    for width in widths:
        height = round(image.height * width / image.width)
        image.resize((width, height), Image.LANCZOS).save(os.path.join(OUT, f"{slot}-{width}.webp"), "WEBP", **WEBP)
    print(f"{slot}: {', '.join(f'{w}w' for w in widths)}")


def build_phone(slot, frame, mask):
    screen = load_screen(slot)
    canvas = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    canvas.paste(screen, FRAME["origin"], mask)
    canvas.alpha_composite(frame)
    save_widths(canvas, slot, PHONE_WIDTHS)


def build_crop(slot):
    source, (fx0, fy0, fx1, fy1) = CROPS[slot]
    screen = load_screen(source).convert("RGB")
    w, h = screen.size
    crop = screen.crop((round(fx0 * w), round(fy0 * h), round(fx1 * w), round(fy1 * h)))
    save_widths(crop, slot, CROP_WIDTHS)


def main(slots):
    os.makedirs(OUT, exist_ok=True)
    frame = Image.open(FRAME["file"]).convert("RGBA")
    mask = aperture_mask(frame, FRAME["origin"], FRAME["screen"])
    for slot in slots:
        if slot in SOURCES:
            build_phone(slot, frame, mask)
        elif slot in CROPS:
            build_crop(slot)
        else:
            sys.exit(f"unknown slot {slot!r}; known: {', '.join([*SOURCES, *CROPS])}")


if __name__ == "__main__":
    main(sys.argv[1:] or [*SOURCES, *CROPS])
