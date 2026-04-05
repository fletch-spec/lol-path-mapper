import math

from PIL import Image, ImageDraw

# Summoner's Rift game coordinate bounds (Hextechdocs)
GAME_X_MIN, GAME_X_MAX = -120, 14870
GAME_Y_MIN, GAME_Y_MAX = -120, 14980

# Jump > this between samples = recall/teleport → start new segment
RECALL_THRESHOLD = 3000

# This map image's playfield sits higher than the standard bounds predict.
# Empirically the path renders ~180px too low at 2048px output; correct by
# shifting up proportionally at any resolution.
_MAP_Y_UP = 140 / 2048  # fraction of image height to subtract from py


def game_to_pixel(game_x, game_y, img_w, img_h):
    px = int((game_x - GAME_X_MIN) / (GAME_X_MAX - GAME_X_MIN) * img_w)
    py = int((1.0 - (game_y - GAME_Y_MIN) / (GAME_Y_MAX - GAME_Y_MIN)) * img_h)
    py -= round(_MAP_Y_UP * img_h)
    return (max(0, min(px, img_w - 1)), max(0, min(py, img_h - 1)))


def split_segments(positions, threshold=RECALL_THRESHOLD):
    """Split position list into segments, breaking on large jumps (recalls/teleports)."""
    if not positions:
        return []
    segments = []
    current = [positions[0]]
    for prev, curr in zip(positions, positions[1:]):
        dist = math.hypot(curr[0] - prev[0], curr[1] - prev[1])
        if dist > threshold:
            segments.append(current)
            current = [curr]
        else:
            current.append(curr)
    segments.append(current)
    return segments


def lerp_color(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def render_path(map_image_path, positions, output_path, downscale=4, line_width=None):
    """Render path onto the map at full resolution, then downscale to reduce file size.

    Args:
        downscale: Factor to reduce output dimensions (4 → 8192x8192 saved as 2048x2048).
                   Set to 1 to skip downscaling.
    """
    base = Image.open(map_image_path).convert("RGBA")
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    img_w, img_h = base.size
    scale = min(img_w, img_h) / 512
    if line_width is None:
        line_width = max(1, int(3 * scale))
    dot_r = max(line_width + 2, int(8 * scale))

    segments = split_segments(positions)
    total_points = sum(len(s) for s in segments)
    print(f"Path segments: {len(segments)}  |  Total points: {total_points}")

    color_start = (50, 100, 255)
    color_end = (255, 50, 50)

    global_total = total_points - 1
    global_i = 0

    for seg in segments:
        if len(seg) < 2:
            global_i += len(seg)
            continue
        pixels = [game_to_pixel(x, y, img_w, img_h) for x, y in seg]
        for i in range(len(pixels) - 1):
            t = global_i / max(global_total, 1)
            color = lerp_color(color_start, color_end, t)
            draw.line([pixels[i], pixels[i + 1]], fill=(*color, 200), width=line_width)
            global_i += 1
        global_i += 1  # account for last point in segment

    # Start (green) and end (red) markers
    first_seg = next((s for s in segments if len(s) >= 1), None)
    last_seg = next((s for s in reversed(segments) if len(s) >= 1), None)

    if first_seg:
        sx, sy = game_to_pixel(*first_seg[0], img_w, img_h)
        draw.ellipse([sx - dot_r, sy - dot_r, sx + dot_r, sy + dot_r], fill=(0, 200, 0, 230))
    if last_seg:
        ex, ey = game_to_pixel(*last_seg[-1], img_w, img_h)
        draw.ellipse([ex - dot_r, ey - dot_r, ex + dot_r, ey + dot_r], fill=(255, 0, 0, 230))

    result = Image.alpha_composite(base, overlay).convert("RGB")

    if downscale > 1:
        out_w, out_h = img_w // downscale, img_h // downscale
        result = result.resize((out_w, out_h), Image.LANCZOS)
        print(f"Downscaled {img_w}x{img_h} → {out_w}x{out_h}")

    result.save(output_path, optimize=True)
    print(f"Saved -> {output_path}")
