"""
Rendering for match insights.
Map overlays use PIL; charts use matplotlib.
"""

import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from path_renderer import GAME_X_MAX, GAME_X_MIN, game_to_pixel


# ── shared helpers ────────────────────────────────────────────────────────────

def _save(img, output_path, downscale):
    if downscale > 1:
        w, h = img.size
        out_w, out_h = w // downscale, h // downscale
        img = img.resize((out_w, out_h), Image.LANCZOS)
        print(f"Downscaled {w}x{h} -> {out_w}x{out_h}")
    img.convert("RGB").save(output_path, optimize=True)
    print(f"Saved -> {output_path}")


def _game_units_to_px(units, img_w):
    """Convert game units to pixels given the image width."""
    return int(units / (GAME_X_MAX - GAME_X_MIN) * img_w)


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


# ── XP gain heatmap ───────────────────────────────────────────────────────────

def render_xp_heatmap(map_path, xp_locations, output_path, downscale=4):
    """High-contrast XP heatmap using numpy accumulation and the plasma colormap.

    Builds a density grid from all weighted XP samples, applies log normalization
    (so mid-intensity areas stay visible even if objectives create extreme spikes),
    then maps through matplotlib's plasma colormap for a vivid yellow→orange→purple
    gradient. Areas with no XP remain fully transparent.
    """
    import matplotlib.cm as cm

    base = Image.open(map_path).convert("RGBA")
    img_w, img_h = base.size

    if not xp_locations:
        _save(base, output_path, downscale)
        return

    # Work at reduced grid resolution for speed; each cell covers ~GRID_DIV px
    GRID_DIV = 4
    gw, gh   = img_w // GRID_DIV, img_h // GRID_DIV
    grid     = np.zeros((gh, gw), dtype=np.float32)
    blob_r   = max(2, _game_units_to_px(400, img_w) // GRID_DIV)  # radius in grid cells

    for x, y, xp in xp_locations:
        px, py = game_to_pixel(x, y, img_w, img_h)
        gx, gy = px // GRID_DIV, py // GRID_DIV
        # Spread each sample into a small square region so adjacent samples merge smoothly
        x0, x1 = max(0, gx - blob_r), min(gw, gx + blob_r + 1)
        y0, y1 = max(0, gy - blob_r), min(gh, gy + blob_r + 1)
        grid[y0:y1, x0:x1] += xp

    # Gaussian blur at grid scale (fast; PIL auto-selects kernel from radius)
    overlay_tmp = Image.fromarray(
        (np.clip(grid / (grid.max() + 1e-9), 0, 1) * 255).astype(np.uint8), "L"
    )
    overlay_tmp = overlay_tmp.filter(ImageFilter.GaussianBlur(radius=max(2, blob_r)))
    grid = np.asarray(overlay_tmp, dtype=np.float32) / 255.0

    # Log normalization: compresses outlier spikes so lane farming stays visible
    grid = np.log1p(grid * 9) / math.log(10)  # maps [0,1] → [0,1] with log curve
    if grid.max() > 0:
        grid /= grid.max()

    # Map through plasma colormap (0=dark purple, 1=bright yellow)
    colormap = cm.get_cmap("plasma")
    rgba     = colormap(grid)  # float array shape (gh, gw, 4)

    # Only show cells above a visibility threshold; scale alpha to [0, 0.88]
    threshold    = 0.08
    alpha_mask   = np.where(grid > threshold,
                            np.clip((grid - threshold) / (1 - threshold), 0, 1) * 0.88, 0)
    rgba[..., 3] = alpha_mask

    overlay_small = Image.fromarray((rgba * 255).astype(np.uint8), "RGBA")
    overlay       = overlay_small.resize((img_w, img_h), Image.LANCZOS)

    result = Image.alpha_composite(base, overlay)

    # Small colorbar legend: "Low XP → High XP"
    _draw_xp_colorbar(result, colormap)
    _save(result, output_path, downscale)


def _draw_xp_colorbar(img, colormap):
    """Draw a slim 'Low XP → High XP' colorbar at the bottom-right corner."""
    draw  = ImageDraw.Draw(img)
    img_w, img_h = img.size
    bar_w = img_w // 8
    bar_h = max(14, img_h // 70)
    margin = img_w // 55
    x0 = img_w - bar_w - margin
    y0 = img_h - bar_h - margin * 3

    # Draw gradient strip one pixel column at a time
    for i in range(bar_w):
        r, g, b, _ = colormap(i / bar_w)
        draw.rectangle([x0 + i, y0, x0 + i + 1, y0 + bar_h],
                       fill=(int(r * 255), int(g * 255), int(b * 255), 210))

    font = _load_font(max(10, bar_h - 2))
    draw.text((x0,                    y0 + bar_h + 3), "Low XP",  font=font, fill=(200, 200, 200, 230))
    draw.text((x0 + bar_w - bar_h * 4, y0 + bar_h + 3), "High XP", font=font, fill=(255, 230, 80,  230))


# ── team fight clusters ───────────────────────────────────────────────────────

def render_teamfight_clusters(map_path, clusters, output_path, downscale=4):
    """Numbered fight circles with a legend panel.

    Each fight gets a sequential number drawn at the circle centre.
    Circle size encodes kill count (cube-root scaled — explained in the legend).
    Kill dots inside each circle are coloured by the team that took the kill:
      blue dot = a blue-team player died here
      red  dot = a red-team player died here
    A legend panel in the corner lists every fight: # | time | kills | winner.
    """
    base = Image.open(map_path).convert("RGBA")
    img_w, img_h = base.size
    overlay = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    draw    = ImageDraw.Draw(overlay)

    base_r   = _game_units_to_px(350, img_w)
    font_num = _load_font(max(18, img_w // 220))
    font_leg = _load_font(max(11, img_w // 340))

    # Chronological order for consistent numbering
    sorted_clusters = sorted(clusters, key=lambda c: c["members"][0]["time"])

    # Draw circles smallest-first so larger ones always appear on top
    for cluster in sorted(sorted_clusters, key=lambda c: c["size"]):
        cx, cy = game_to_pixel(cluster["centroid"][0], cluster["centroid"][1], img_w, img_h)
        size   = cluster["size"]
        r      = int(base_r * (size ** (1 / 3)))  # cube-root so 10 kills ≈ 2× radius of 1 kill

        if cluster["winner"] == "blue":
            fill_rgb, outline_rgb = (30, 120, 255), (140, 200, 255)
        elif cluster["winner"] == "red":
            fill_rgb, outline_rgb = (210, 45, 45), (255, 130, 110)
        else:
            fill_rgb, outline_rgb = (140, 140, 140), (210, 210, 210)

        # Team fights (4+ kills) are fully filled; skirmishes are semi-transparent
        fill_alpha = 160 if size >= 4 else 55

        # Soft glow ring
        draw.ellipse([cx - r - 8, cy - r - 8, cx + r + 8, cy + r + 8],
                     fill=(*fill_rgb, 30))
        # Main circle
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     fill=(*fill_rgb, fill_alpha),
                     outline=(*outline_rgb, 230),
                     width=max(2, r // 10))

        # Individual kill dots coloured by which team lost the player
        dot_r = max(4, r // 5)
        for kill in cluster["members"]:
            kx, ky = game_to_pixel(kill["x"], kill["y"], img_w, img_h)
            # Blue dot = blue team player died here; red dot = red team player died here
            if 1 <= kill["victim"] <= 5:
                dot_fill = (100, 160, 255, 220)
            else:
                dot_fill = (255, 100, 100, 220)
            draw.ellipse([kx - dot_r, ky - dot_r, kx + dot_r, ky + dot_r], fill=dot_fill)

    # Composite circles before drawing text (text always rendered on top)
    result     = Image.alpha_composite(base, overlay)
    label_draw = ImageDraw.Draw(result)

    # Number labels at circle centres
    for ci, cluster in enumerate(sorted_clusters, 1):
        cx, cy = game_to_pixel(cluster["centroid"][0], cluster["centroid"][1], img_w, img_h)
        r      = int(base_r * (cluster["size"] ** (1 / 3)))
        bbox   = label_draw.textbbox((0, 0), str(ci), font=font_num)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        _draw_outlined_text(label_draw, (cx - tw // 2, cy - th // 2), str(ci), font_num)

    # Legend panel
    _draw_fights_legend(label_draw, sorted_clusters, img_w, img_h, font_leg)
    _save(result, output_path, downscale)


def _draw_fights_legend(draw, clusters, img_w, img_h, font):
    """Semi-transparent legend panel listing every fight with number/time/kills/winner."""
    pad     = img_w // 60
    line_h  = max(22, img_w // 290)
    col_w   = img_w // 4

    # Panel height: 2 header lines + one row per fight
    n_rows    = len(clusters)
    panel_h   = (n_rows + 2) * line_h + pad * 2
    panel_x   = pad
    panel_y   = img_h - panel_h - pad

    draw.rectangle([panel_x, panel_y, panel_x + col_w, img_h - pad],
                   fill=(0, 0, 0, 165))

    _draw_outlined_text(draw, (panel_x + 6, panel_y + 4),
                        "#   TYPE  TIME    ×KILLS  WINNER",
                        font, fill=(180, 210, 255), outline=(0, 0, 0))
    _draw_outlined_text(draw, (panel_x + 6, panel_y + 4 + line_h),
                        "Circle size = kill count (cube-root scale)",
                        font, fill=(130, 130, 130), outline=(0, 0, 0))

    for i, cluster in enumerate(clusters):
        mins = int(cluster["start_min"])
        secs = int((cluster["start_min"] - mins) * 60)
        kind   = "TF " if cluster["size"] >= 4 else "SK "  # Team Fight vs Skirmish
        winner = cluster["winner"].capitalize()

        if cluster["winner"] == "blue":
            fill = (120, 170, 255)
        elif cluster["winner"] == "red":
            fill = (255, 110, 110)
        else:
            fill = (180, 180, 180)

        row_y = panel_y + 4 + (i + 2) * line_h
        _draw_outlined_text(draw, (panel_x + 6, row_y),
                            f"#{i+1:<2}  {kind}  {mins}:{secs:02d}    ×{cluster['size']:<2}  {winner}",
                            font, fill=fill, outline=(0, 0, 0))


# ── lane aggression ───────────────────────────────────────────────────────────

def render_lane_aggression(map_path, aggression_info, output_path, downscale=4):
    """Laning-phase position density map with aggression score annotation.

    Purpose: shows where the player spent the first 15 minutes. The orange
    density cloud reveals movement patterns; the avg-position marker summarises
    overall lane presence. The aggression score (0–100) measures how far forward
    the player was positioned relative to the two bases:
      0  = camped under own tower
      50 = neutral / river
      100 = always at enemy tower
    """
    base = Image.open(map_path).convert("RGBA")
    img_w, img_h = base.size

    # Density cloud of laning positions
    heat  = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    hdraw = ImageDraw.Draw(heat)
    dot_r = max(3, img_w // 800)

    for x, y in aggression_info["laning_positions"]:
        px, py = game_to_pixel(x, y, img_w, img_h)
        hdraw.ellipse([px - dot_r, py - dot_r, px + dot_r, py + dot_r],
                      fill=(255, 165, 0, 55))

    heat   = heat.filter(ImageFilter.GaussianBlur(radius=dot_r * 3))
    result = Image.alpha_composite(base, heat)

    # Average-position marker (orange circle with white border)
    markers = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    mdraw   = ImageDraw.Draw(markers)
    ax_px, ay_px = game_to_pixel(
        aggression_info["avg_pos"][0], aggression_info["avg_pos"][1], img_w, img_h
    )
    mr = max(14, img_w // 240)
    mdraw.ellipse([ax_px - mr - 6, ay_px - mr - 6, ax_px + mr + 6, ay_px + mr + 6],
                  fill=(255, 165, 0, 60))
    mdraw.ellipse([ax_px - mr, ay_px - mr, ax_px + mr, ay_px + mr],
                  fill=(255, 165, 0, 230), outline=(255, 255, 255, 255),
                  width=max(2, mr // 5))
    result = Image.alpha_composite(result, markers)

    # Annotation overlay
    fdraw    = ImageDraw.Draw(result)
    font_med = _load_font(max(15, img_w // 260))
    font_sm  = _load_font(max(11, img_w // 370))

    score       = aggression_info["score"]
    description = aggression_info["description"]
    lane        = aggression_info["lane"]

    # Horizontal score gauge bar (top-left corner)
    bx, by = img_w // 40, img_w // 40
    bar_w  = img_w // 5
    bar_h  = max(12, img_w // 190)

    fdraw.rectangle([bx, by, bx + bar_w, by + bar_h], fill=(20, 20, 20, 200))
    fill_w     = int(bar_w * score / 100)
    bar_color  = ((30, 100, 255, 220) if score < 44
                  else (50, 200, 90, 220) if score < 58
                  else (255, 100, 30, 220))
    fdraw.rectangle([bx, by, bx + fill_w, by + bar_h], fill=bar_color)

    # Labels below the gauge
    _draw_outlined_text(
        fdraw, (bx, by + bar_h + 4),
        f"{lane} Lane  |  Aggression {score}/100  —  {description}",
        font_med
    )
    _draw_outlined_text(
        fdraw, (bx, by + bar_h + 4 + max(18, img_w // 220)),
        "Orange cloud = first-15-min positions  |  Circle = average position",
        font_sm, fill=(200, 200, 200)
    )
    # Defensive / Aggressive axis labels
    _draw_outlined_text(fdraw, (bx, by - max(14, img_w // 300) - 2),
                        "Defensive ◀", font_sm, fill=(100, 150, 255))
    aggressive_label = "▶ Aggressive"
    bbox = fdraw.textbbox((0, 0), aggressive_label, font=font_sm)
    label_w = bbox[2] - bbox[0]
    _draw_outlined_text(fdraw, (bx + bar_w - label_w, by - max(14, img_w // 300) - 2),
                        aggressive_label, font_sm, fill=(255, 120, 50))

    _save(result, output_path, downscale)


# ── activity chart ────────────────────────────────────────────────────────────

def render_activity_chart(stats, per_minute, champion_name, output_path,
                           events_at_time=None, per_15s=None):
    """Dark-theme activity chart with a timeline-centred layout.

    Layout (top → bottom):
      CS per minute  — bar chart
      Event timeline — exact-timestamp markers for kills, deaths, assists,
                       towers, objectives, recalls
      Activity strip — 15s-resolution colour bands (Farming/Fighting/Base/Roaming)
      Gold per minute — bar chart

    A stats summary panel occupies the right-hand column.

    Parameters
    ----------
    events_at_time : dict returned by insights.player_event_times() — enables
                     exact sub-minute event markers on the timeline row.
    per_15s : list from insights.per_15s_breakdown() — 4× resolution activity strip.
              Falls back to per_minute activity if not provided.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.gridspec import GridSpec

    # ── colour palette ────────────────────────────────────────────────────────
    ACTIVITY_COLORS = {
        "Farming":  "#4CAF50",
        "Fighting": "#F44336",
        "Base":     "#2196F3",
        "Roaming":  "#FF9800",
    }
    BG     = "#1a1a2e"
    PANEL  = "#16213e"
    GRID_C = "#2a2a4a"
    TEXT   = "#e0e0e0"
    SUB    = "#aaaaaa"
    ACCENT = "#7ecfff"

    # Marker styles for each event type on the timeline row (scatter() uses 's' not 'ms')
    EVENT_STYLES = {
        "kills":      dict(marker="^", color="#44ff88", s=80,  zorder=5, label="Kill"),
        "deaths":     dict(marker="X", color="#ff4444", s=80,  zorder=5, label="Death"),
        "assists":    dict(marker="D", color="#44ddff", s=40,  zorder=4, label="Assist"),
        "towers":     dict(marker="v", color="#FFD700", s=80,  zorder=5, label="Tower"),
        "objectives": dict(marker="*", color="#ffffff", s=140, zorder=5, label="Objective"),
        "recalls":    dict(marker="o", color="#cc88ff", s=55,  zorder=4, label="Recall"),
    }
    # Vertical stagger so overlapping events don't pile on the same y
    Y_LEVELS = {
        "kills":       0.65,
        "deaths":     -0.65,
        "assists":     0.35,
        "towers":      0.65,
        "objectives":  0.65,
        "recalls":    -0.35,
    }

    game_end = stats["duration_min"]
    minutes  = [r["minute"]      for r in per_minute]
    cs_bars  = [r["cs_gained"]   for r in per_minute]
    gd_bars  = [r["gold_gained"] for r in per_minute]

    # ── figure / grid layout ─────────────────────────────────────────────────
    fig = plt.figure(figsize=(18, 10), facecolor=BG)
    gs  = GridSpec(4, 2, figure=fig,
                   width_ratios=[5, 1],
                   height_ratios=[2.5, 1.5, 0.35, 2.5],
                   hspace=0.06, wspace=0.04,
                   left=0.05, right=0.98, top=0.93, bottom=0.06)

    ax_cs     = fig.add_subplot(gs[0, 0])
    ax_events = fig.add_subplot(gs[1, 0], sharex=ax_cs)
    ax_strip  = fig.add_subplot(gs[2, 0], sharex=ax_cs)
    ax_gold   = fig.add_subplot(gs[3, 0], sharex=ax_cs)
    ax_info   = fig.add_subplot(gs[:, 1])

    for ax in (ax_cs, ax_events, ax_strip, ax_gold):
        ax.set_facecolor(PANEL)
        ax.tick_params(colors=TEXT, labelsize=8)
        for spine in ["top", "right"]:
            ax.spines[spine].set_visible(False)
        for spine in ["bottom", "left"]:
            ax.spines[spine].set_color(GRID_C)

    # ── row 0: CS per minute ─────────────────────────────────────────────────
    avg_cs = sum(cs_bars) / len(cs_bars) if cs_bars else 0
    ax_cs.bar(minutes, cs_bars, color="#4CAF50", alpha=0.85, width=0.8)
    ax_cs.axhline(avg_cs, color="#aaffaa", linestyle="--", linewidth=1,
                  label=f"avg {avg_cs:.1f} CS/min")
    ax_cs.set_ylabel("CS / min", color=TEXT, fontsize=9)
    ax_cs.set_title("CS per Minute", color=SUB, fontsize=9, pad=3)
    ax_cs.legend(labelcolor=TEXT, facecolor=BG, edgecolor=GRID_C, fontsize=8)
    ax_cs.grid(axis="y", color=GRID_C, linewidth=0.5, alpha=0.7)
    ax_cs.tick_params(labelbottom=False)

    # ── row 1: event timeline ────────────────────────────────────────────────
    ax_events.axhline(0, color=ACCENT, linewidth=1.5, alpha=0.5, zorder=2)
    ax_events.set_xlim(-0.5, game_end + 0.5)
    ax_events.set_ylim(-1.3, 1.3)
    ax_events.set_yticks([])
    ax_events.spines["left"].set_visible(False)
    ax_events.tick_params(labelbottom=False)

    if events_at_time:
        for key, style in EVENT_STYLES.items():
            times = events_at_time.get(key, [])
            if not times:
                continue
            y_base = Y_LEVELS[key]
            ax_events.scatter(times, [y_base] * len(times),
                              **{k: v for k, v in style.items() if k != "label"},
                              label=style["label"])
            for t in times:
                ax_events.axvline(t, color=style["color"], alpha=0.12, linewidth=0.9, zorder=1)

    handles, labels_ = ax_events.get_legend_handles_labels()
    if handles:
        ax_events.legend(handles, labels_, loc="upper right",
                         labelcolor=TEXT, facecolor=BG, edgecolor=GRID_C,
                         fontsize=7, ncol=min(6, len(handles)), markerscale=0.9)
    ax_events.set_title("Event Timeline", color=SUB, fontsize=9, pad=3)

    # ── row 2: activity colour strip ─────────────────────────────────────────
    ax_strip.set_yticks([])
    for sp in ax_strip.spines.values():
        sp.set_visible(False)
    ax_strip.tick_params(labelbottom=False)

    # Use 15s buckets if available, else fall back to 60s per-minute data
    strip_data = (per_15s if per_15s
                  else [{"time_min": r["minute"], "activity": r["activity"]} for r in per_minute])
    if strip_data:
        dt = (strip_data[1]["time_min"] - strip_data[0]["time_min"]) if len(strip_data) > 1 else 1
        for entry in strip_data:
            color = ACTIVITY_COLORS.get(entry["activity"], "#888")
            ax_strip.barh(0, dt, left=entry["time_min"], height=1, color=color, alpha=0.92)

    patches = [mpatches.Patch(color=c, label=l) for l, c in ACTIVITY_COLORS.items()]
    ax_strip.legend(handles=patches, loc="center right", labelcolor=TEXT,
                    facecolor=BG, edgecolor="none", fontsize=7, ncol=4,
                    borderpad=0.3, handlelength=1)

    # ── row 3: gold per minute ────────────────────────────────────────────────
    ax_gold.bar(minutes, gd_bars, color="#FFD700", alpha=0.85, width=0.8)
    ax_gold.set_ylabel("Gold / min", color=TEXT, fontsize=9)
    ax_gold.set_title("Gold per Minute", color=SUB, fontsize=9, pad=3)
    ax_gold.set_xlabel("Game Time (minutes)", color=TEXT, fontsize=9)
    ax_gold.grid(axis="y", color=GRID_C, linewidth=0.5, alpha=0.7)

    # ── right column: stats panel ─────────────────────────────────────────────
    ax_info.set_facecolor("#0d1117")
    for sp in ax_info.spines.values():
        sp.set_color(GRID_C)
    ax_info.set_xticks([])
    ax_info.set_yticks([])

    mins_int = int(stats["duration_min"])
    secs_int = int(stats["duration_sec"] % 60)
    kda_str  = f"{stats['kills']}/{stats['deaths']}/{stats['assists']}"

    # Each tuple: (text, y_axis_fraction, color, fontsize, weight)
    info_lines = [
        (champion_name,                          0.97, "#ffffff",  12, "bold"),
        (f"Duration  {mins_int}:{secs_int:02d}", 0.91, TEXT,        9, "normal"),
        ("",                                     0.87, TEXT,        4, "normal"),
        ("— Combat —",                           0.85, ACCENT,      8, "bold"),
        (f"KDA     {kda_str}",                   0.80, TEXT,        9, "normal"),
        (f"Ratio   {stats['kda']:.2f}",          0.75, TEXT,        9, "normal"),
    ]

    y = 0.70
    if stats.get("first_kill_min") is not None:
        info_lines.append((f"1st kill   {stats['first_kill_min']}m", y, TEXT, 9, "normal"))
        y -= 0.05
    if stats.get("first_death_min") is not None:
        info_lines.append((f"1st death  {stats['first_death_min']}m", y, TEXT, 9, "normal"))
        y -= 0.05

    y -= 0.02
    info_lines += [
        ("— Farm & Gold —",                             y,        ACCENT, 8, "bold"),
        (f"CS      {stats['total_cs']} ({stats['cs_per_min']}/min)", y - 0.05, TEXT, 9, "normal"),
        (f"Gold    {stats['gold_earned']:,}",           y - 0.10, TEXT,   9, "normal"),
        (f"G/min   {int(stats['gold_per_min'])}",       y - 0.15, TEXT,   9, "normal"),
        ("— Map Impact —",                              y - 0.21, ACCENT, 8, "bold"),
        (f"Towers  {stats['tower_participations']}",    y - 0.26, TEXT,   9, "normal"),
        (f"Objs    {stats['objective_participations']}", y - 0.31, TEXT,  9, "normal"),
        (f"Recalls {stats['recalls']}",                 y - 0.36, TEXT,   9, "normal"),
    ]

    for text, yf, color, size, weight in info_lines:
        ax_info.text(0.08, yf, text,
                     transform=ax_info.transAxes,
                     color=color, fontsize=size, fontweight=weight,
                     va="top", ha="left")

    fig.suptitle(f"{champion_name} — Activity Analysis",
                 color=TEXT, fontsize=11, fontweight="bold", y=0.97)

    plt.savefig(output_path, dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close()
    print(f"Saved -> {output_path}")
