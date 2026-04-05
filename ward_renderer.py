from PIL import Image, ImageDraw, ImageFilter

from path_renderer import GAME_X_MAX, GAME_X_MIN, game_to_pixel

WARD_VISION_RADIUS = 900  # game units (approximate for most ward types)

_BLUE_DOT = (30, 144, 255, 210)
_RED_DOT = (220, 50, 50, 210)
_BLUE_VISION = (30, 100, 220, 22)
_RED_VISION = (220, 60, 60, 22)


def _color(creator_id, dot=True):
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
        px, py = game_to_pixel(ev["x"], ev["y"], img_w, img_h)
        color = _color(ev["creator_id"], dot=True)
        draw.ellipse([px - dot_r, py - dot_r, px + dot_r, py + dot_r], fill=color)

    result = Image.alpha_composite(base, overlay)
    _save(result, output_path, downscale)


def render_vision_heatmap(map_path, ward_events, output_path, downscale=4):
    """Render accumulated ward vision coverage as a heatmap overlay.

    Each ward contributes a semi-transparent circle of WARD_VISION_RADIUS.
    Overlapping circles accumulate to show high-vision areas.
    A Gaussian blur is applied for smoothness.
    """
    base = Image.open(map_path).convert("RGBA")
    img_w, img_h = base.size

    vision_px = int(WARD_VISION_RADIUS / (GAME_X_MAX - GAME_X_MIN) * img_w)

    blue_layer = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    red_layer = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    blue_draw = ImageDraw.Draw(blue_layer)
    red_draw = ImageDraw.Draw(red_layer)

    for ev in ward_events:
        px, py = game_to_pixel(ev["x"], ev["y"], img_w, img_h)
        is_blue = ev["creator_id"] <= 5
        draw = blue_draw if is_blue else red_draw
        color = _color(ev["creator_id"], dot=False)
        draw.ellipse(
            [px - vision_px, py - vision_px, px + vision_px, py + vision_px],
            fill=color,
        )

    blur_radius = max(1, vision_px // 4)
    blue_layer = blue_layer.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    red_layer = red_layer.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    result = Image.alpha_composite(base, blue_layer)
    result = Image.alpha_composite(result, red_layer)
    _save(result, output_path, downscale)


def _save(img, output_path, downscale):
    if downscale > 1:
        w, h = img.size
        out_w, out_h = w // downscale, h // downscale
        img = img.resize((out_w, out_h), Image.LANCZOS)
        print(f"Downscaled {w}x{h} → {out_w}x{out_h}")
    img.convert("RGB").save(output_path, optimize=True)
    print(f"Saved -> {output_path}")
