"""
Ward placement renderers.

Two outputs:
  Ward map    — a dot at every ward placement location, blue or red by team.
  Vision heatmap — accumulated vision circles showing total map coverage.

Both render at the full map resolution then downscale, matching the approach
used by path_renderer. game_to_pixel() is imported to keep coordinate
transforms consistent across the project.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from path_renderer import GAME_X_MAX, GAME_X_MIN, game_to_pixel, game_to_pixel_raw

# Approximate vision radius for standard wards (Control Wards are ~900, Stealth ~900)
WARD_VISION_RADIUS = 900  # game units

# RGBA colours for the two rendering modes
_BLUE_DOT    = (30, 144, 255, 210)   # solid dot on the ward map
_RED_DOT     = (220, 50,  50,  210)
_BLUE_VISION = (60, 140, 255, 22)    # low-alpha fill that accumulates; normalised after blur
_RED_VISION  = (255, 70,  60,  22)


def _color(creator_id, dot=True):
    """Return the appropriate RGBA colour for a ward event based on team (1-5 = blue)."""
    if dot:
        return _BLUE_DOT if creator_id <= 5 else _RED_DOT
    return _BLUE_VISION if creator_id <= 5 else _RED_VISION


def render_ward_map(map_path, ward_events, output_path, downscale=4):
    """Render colored dots at ward placement locations.

    Blue team (participants 1-5) = blue dots.
    Red team (participants 6-10) = red dots.
    """
    base = Image.open(map_path).convert("RGBA")
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    img_w, img_h = base.size
    scale = min(img_w, img_h) / 512
    dot_r = max(2, int(4 * scale))

    for ev in ward_events:
        px, py = game_to_pixel_raw(ev["x"], ev["y"], img_w, img_h)
        if not (0 <= px < img_w and 0 <= py < img_h):
            continue
        color = _color(ev["creator_id"], dot=True)
        draw.ellipse([px - dot_r, py - dot_r, px + dot_r, py + dot_r], fill=color)

    result = Image.alpha_composite(base, overlay)
    _save(result, output_path, downscale)


def _normalize_vision_layer(layer, min_alpha=0, max_alpha=200, artifact_threshold=8):
    """Normalise a blurred vision layer to show relative warding density.

    min_alpha=0 means sparse/isolated wards render faintly while heavily
    warded areas (baron, dragon, river) are clearly saturated.  This makes
    density differences visible rather than treating every ward equally.
    artifact_threshold filters sub-pixel blur fringe noise.
    """
    arr   = np.array(layer, dtype=np.float32)
    alpha = arr[..., 3]
    peak  = alpha.max()
    if peak == 0:
        return layer
    norm         = alpha / peak
    arr[..., 3]  = np.where(alpha > artifact_threshold,
                             min_alpha + norm * (max_alpha - min_alpha), 0)
    return Image.fromarray(arr.astype(np.uint8))


def render_vision_heatmap(map_path, ward_events, output_path, downscale=4):
    """Render accumulated ward vision coverage as a heatmap overlay.

    Each ward contributes a semi-transparent circle of WARD_VISION_RADIUS.
    Overlapping circles accumulate to show high-vision areas.
    A Gaussian blur is applied for smoothness, then the alpha is normalised so
    even isolated wards remain discernible against the dark map background.
    """
    base = Image.open(map_path).convert("RGBA")
    img_w, img_h = base.size

    vision_px = int(WARD_VISION_RADIUS / (GAME_X_MAX - GAME_X_MIN) * img_w)

    blue_layer = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    red_layer = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    blue_draw = ImageDraw.Draw(blue_layer)
    red_draw = ImageDraw.Draw(red_layer)

    for ev in ward_events:
        px, py = game_to_pixel_raw(ev["x"], ev["y"], img_w, img_h)
        if not (0 <= px < img_w and 0 <= py < img_h):
            continue
        is_blue = ev["creator_id"] <= 5
        draw = blue_draw if is_blue else red_draw
        color = _color(ev["creator_id"], dot=False)
        draw.ellipse(
            [px - vision_px, py - vision_px, px + vision_px, py + vision_px],
            fill=color,
        )

    blur_radius = max(1, vision_px // 4)
    blue_layer = _normalize_vision_layer(
        blue_layer.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    )
    red_layer = _normalize_vision_layer(
        red_layer.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    )

    result = Image.alpha_composite(base, blue_layer)
    result = Image.alpha_composite(result, red_layer)
    _save(result, output_path, downscale)


def _save(img, output_path, downscale):
    if downscale > 1:
        w, h = img.size
        out_w, out_h = w // downscale, h // downscale
        img = img.resize((out_w, out_h), Image.LANCZOS)
        print(f"Downscaled {w}x{h} -> {out_w}x{out_h}")
    img.convert("RGB").save(output_path, optimize=True)
    print(f"Saved -> {output_path}")
