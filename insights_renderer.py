"""
Rendering for match insights.
Map overlays use PIL; charts use matplotlib.
"""

import math
from PIL import Image, ImageDraw, ImageFilter

from path_renderer import GAME_X_MAX, GAME_X_MIN, game_to_pixel


# ── shared helper ─────────────────────────────────────────────────────────────

def _save(img, output_path, downscale):
    if downscale > 1:
        w, h = img.size
        out_w, out_h = w // downscale, h // downscale
        img = img.resize((out_w, out_h), Image.LANCZOS)
        print(f"Downscaled {w}x{h} → {out_w}x{out_h}")
    img.convert("RGB").save(output_path, optimize=True)
    print(f"Saved -> {output_path}")


def _game_units_to_px(units, img_w):
    return int(units / (GAME_X_MAX - GAME_X_MIN) * img_w)


# ── XP gain heatmap ───────────────────────────────────────────────────────────

def render_xp_heatmap(map_path, xp_locations, output_path, downscale=4):
    """Cyan/teal heatmap showing where XP was earned.

    Expects the high-resolution output of insights.xp_gain_locations() where each
    entry has a small per-sample weight. Accumulation of many overlapping small blobs
    reveals the true XP hotspots (lane, jungle, objectives).
    """
    base = Image.open(map_path).convert("RGBA")
    img_w, img_h = base.size

    if not xp_locations:
        _save(base, output_path, downscale)
        return

    # Each sample covers roughly one position-poll worth of map area (~300 units)
    r = max(2, _game_units_to_px(280, img_w))

    # Normalise against the 95th-percentile sample weight to avoid outliers
    # dominating the colour scale (e.g. a single objective XP spike)
    weights = sorted(xp for _, _, xp in xp_locations)
    p95 = weights[int(len(weights) * 0.95)]
    if p95 == 0:
        p95 = weights[-1] or 1

    overlay = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    for x, y, xp in xp_locations:
        px, py = game_to_pixel(x, y, img_w, img_h)
        t = min(1.0, xp / p95)
        alpha = int(12 + 30 * t)          # low per-sample alpha; accumulation builds intensity
        draw.ellipse([px - r, py - r, px + r, py + r], fill=(0, 210, 170, alpha))

    # Blur enough to blend adjacent samples into smooth gradients
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=max(2, r)))
    result = Image.alpha_composite(base, overlay)
    _save(result, output_path, downscale)


# ── team fight clusters ───────────────────────────────────────────────────────

def _load_font(size):
    """Try common system font paths; fall back to PIL default."""
    from PIL import ImageFont
    for path in [
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]:
        try:
            return ImageFont.truetype(path, size=size)
        except Exception:
            pass
    return ImageFont.load_default()


def _draw_outlined_text(draw, pos, text, font, fill=(255, 255, 255), outline=(0, 0, 0)):
    """Draw text with a 1-pixel dark outline for legibility over any background."""
    x, y = pos
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        draw.text((x + dx, y + dy), text, font=font, fill=(*outline, 220))
    draw.text((x, y), text, font=font, fill=(*fill, 255))


def render_teamfight_clusters(map_path, clusters, output_path, downscale=4):
    """Annotated circles for each team fight.

    Visual hierarchy:
      • Large filled circles  (4+ kills) = proper team fights
      • Small outlined circles (2–3 kills) = skirmishes
    Colour: blue won / red won / grey = even.
    Label: game-time minute stamped at the circle centre.
    """
    base = Image.open(map_path).convert("RGBA")
    img_w, img_h = base.size
    overlay = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    base_r  = _game_units_to_px(350, img_w)
    font_sz = max(14, img_w // 280)
    font    = _load_font(font_sz)

    # Draw smallest clusters first so larger ones render on top
    for cluster in sorted(clusters, key=lambda c: c["size"]):
        cx, cy = game_to_pixel(cluster["centroid"][0], cluster["centroid"][1], img_w, img_h)
        size   = cluster["size"]

        # Cube-root scaling: 2 kills → ~base_r, 10 kills → ~2.2×base_r
        r = int(base_r * (size ** (1 / 3)))

        is_teamfight = size >= 4

        if cluster["winner"] == "blue":
            fill_rgb, outline_rgb = (30, 120, 255), (140, 200, 255)
        elif cluster["winner"] == "red":
            fill_rgb, outline_rgb = (210, 45, 45), (255, 130, 110)
        else:
            fill_rgb, outline_rgb = (140, 140, 140), (210, 210, 210)

        fill_alpha    = 170 if is_teamfight else 70
        outline_alpha = 230

        # Glow
        draw.ellipse([cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6],
                     fill=(*fill_rgb, 40))
        # Main circle
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     fill=(*fill_rgb, fill_alpha),
                     outline=(*outline_rgb, outline_alpha))

        # Individual kill dots
        dot_r = max(3, r // 6)
        for kill in cluster["members"]:
            kx, ky = game_to_pixel(kill["x"], kill["y"], img_w, img_h)
            draw.ellipse([kx - dot_r, ky - dot_r, kx + dot_r, ky + dot_r],
                         fill=(255, 255, 255, 200))

    # Draw text labels in a second pass (always on top of circles)
    label_draw = ImageDraw.Draw(base)  # draw directly on base after composite
    result = Image.alpha_composite(base, overlay)
    label_draw2 = ImageDraw.Draw(result)

    for cluster in clusters:
        cx, cy = game_to_pixel(cluster["centroid"][0], cluster["centroid"][1], img_w, img_h)
        size = cluster["size"]
        r    = int(base_r * (size ** (1 / 3)))

        mins = int(cluster["start_min"])
        secs = int((cluster["start_min"] - mins) * 60)
        label = f"{mins}:{secs:02d}"

        # Centre the text in the circle
        bbox = label_draw2.textbbox((0, 0), label, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        _draw_outlined_text(label_draw2, (cx - tw // 2, cy - th // 2), label, font)

    _save(result, output_path, downscale)


# ── lane aggression ───────────────────────────────────────────────────────────

def render_lane_aggression(map_path, aggression_info, output_path, downscale=4):
    """Density cloud of laning-phase positions with avg-position marker and score annotation."""
    base = Image.open(map_path).convert("RGBA")
    img_w, img_h = base.size

    # Density cloud
    heat = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    hdraw = ImageDraw.Draw(heat)
    dot_r = max(3, img_w // 800)

    for x, y in aggression_info["laning_positions"]:
        px, py = game_to_pixel(x, y, img_w, img_h)
        hdraw.ellipse([px - dot_r, py - dot_r, px + dot_r, py + dot_r],
                      fill=(255, 165, 0, 55))

    heat = heat.filter(ImageFilter.GaussianBlur(radius=dot_r * 3))
    result = Image.alpha_composite(base, heat)

    # Avg position marker
    markers = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    mdraw = ImageDraw.Draw(markers)
    ax, ay = game_to_pixel(aggression_info["avg_pos"][0], aggression_info["avg_pos"][1], img_w, img_h)
    mr = max(8, img_w // 350)
    mdraw.ellipse([ax - mr, ay - mr, ax + mr, ay + mr],
                  fill=(255, 165, 0, 230), outline=(255, 255, 255, 230))

    result = Image.alpha_composite(result, markers)
    _save(result, output_path, downscale)


# ── activity chart ────────────────────────────────────────────────────────────

def render_activity_chart(stats, per_minute, champion_name, output_path):
    """Dark-theme matplotlib chart: CS/min, gold/min, and per-minute activity bars."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    ACTIVITY_COLORS = {
        "Farming":  "#4CAF50",
        "Fighting": "#F44336",
        "Base":     "#2196F3",
        "Roaming":  "#FF9800",
    }
    BG      = "#1a1a2e"
    PANEL   = "#16213e"
    GRID    = "#2a2a4a"
    TEXT    = "#e0e0e0"
    SUBTEXT = "#aaaaaa"

    minutes    = [r["minute"]     for r in per_minute]
    cs_bars    = [r["cs_gained"]  for r in per_minute]
    gold_bars  = [r["gold_gained"] for r in per_minute]
    activities = [r["activity"]   for r in per_minute]

    fig, axes = plt.subplots(3, 1, figsize=(15, 9), facecolor=BG,
                             gridspec_kw={"height_ratios": [2, 2, 1]})

    title = (f"{champion_name}  —  "
             f"{stats['kills']}/{stats['deaths']}/{stats['assists']} KDA  |  "
             f"{stats['total_cs']} CS ({stats['cs_per_min']}/min)  |  "
             f"{stats['gold_earned']:,}g ({int(stats['gold_per_min'])}/min)  |  "
             f"{stats['recalls']} recalls  |  "
             f"{stats['tower_participations']} towers  |  "
             f"{stats['objective_participations']} objectives")
    fig.suptitle(title, color=TEXT, fontsize=10, fontweight="bold", y=0.98)

    for ax in axes:
        ax.set_facecolor(PANEL)
        ax.tick_params(colors=TEXT, labelsize=8)
        for spine in ["top", "right"]:
            ax.spines[spine].set_visible(False)
        for spine in ["bottom", "left"]:
            ax.spines[spine].set_color(GRID)
        ax.yaxis.label.set_color(TEXT)
        ax.xaxis.label.set_color(TEXT)
        ax.grid(axis="y", color=GRID, linewidth=0.5, alpha=0.7)

    # CS per minute
    avg_cs = sum(cs_bars) / len(cs_bars) if cs_bars else 0
    axes[0].bar(minutes, cs_bars, color="#4CAF50", alpha=0.85, width=0.8)
    axes[0].axhline(avg_cs, color="#aaffaa", linestyle="--", linewidth=1,
                    label=f"avg {avg_cs:.1f} CS/min")
    axes[0].set_ylabel("CS Gained", fontsize=9)
    axes[0].set_title("CS per Minute", color=SUBTEXT, fontsize=9, pad=3)
    axes[0].legend(labelcolor=TEXT, facecolor=BG, edgecolor=GRID, fontsize=8)

    # Gold per minute
    axes[1].bar(minutes, gold_bars, color="#FFD700", alpha=0.85, width=0.8)
    axes[1].set_ylabel("Gold Earned", fontsize=9)
    axes[1].set_title("Gold per Minute", color=SUBTEXT, fontsize=9, pad=3)

    # Activity timeline
    bar_colors = [ACTIVITY_COLORS.get(a, "#888") for a in activities]
    axes[2].bar(minutes, [1] * len(minutes), color=bar_colors, alpha=0.9, width=0.95)
    axes[2].set_yticks([])
    axes[2].set_xlabel("Game Time (minutes)", fontsize=9)
    axes[2].set_title("Activity per Minute", color=SUBTEXT, fontsize=9, pad=3)

    patches = [mpatches.Patch(color=c, label=l) for l, c in ACTIVITY_COLORS.items()]
    axes[2].legend(handles=patches, loc="upper right", labelcolor=TEXT,
                   facecolor=BG, edgecolor=GRID, fontsize=8, ncol=4)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(output_path, dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close()
    print(f"Saved -> {output_path}")
