"""
Rendering for match insights.
Map overlays use PIL; charts use matplotlib.
"""

import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from .path_renderer import GAME_X_MAX, GAME_X_MIN, game_to_pixel


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
    # log1p(x*9)/log(10) maps [0,1] → [0,1] with a log curve; *9 sets the curve shape
    # so that mid-range values (lane CS) stay visible even when objective spikes hit 1.0
    grid = np.log1p(grid * 9) / math.log(10)
    if grid.max() > 0:
        grid /= grid.max()

    # Custom colormap: cyan (low/faint) → violet → orange → yellow (high/hot)
    # Cyan at the low end contrasts clearly with the dark map background so
    # even faint XP areas are discernible, unlike plasma's near-black purple start.
    from matplotlib.colors import LinearSegmentedColormap
    colormap = LinearSegmentedColormap.from_list(
        "xp_heatmap",
        [(0.0, "#00E5FF"),   # cyan   — low XP, distinct from map greens/darks
         (0.4, "#CC44FF"),   # violet — mid
         (0.7, "#FF6600"),   # orange
         (1.0, "#FFEE00")],  # yellow — high XP
    )
    rgba = colormap(grid)  # float array shape (gh, gw, 4)

    # Alpha: floor of 0.20 for above-threshold cells so faint areas remain visible;
    # threshold lowered to 0.05 to expose more of the sparse XP regions.
    threshold = 0.05
    min_alpha = 0.20
    max_alpha = 0.88
    # Linearly remap grid intensity from [threshold, 1] to [min_alpha, max_alpha]
    alpha_mask = np.where(
        grid > threshold,
        min_alpha + np.clip((grid - threshold) / (1 - threshold), 0, 1) * (max_alpha - min_alpha),
        0,
    )
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
    """Numbered fight circles with death markers and connector lines.

    Each fight gets a sequential number drawn at the circle centre.
    Circle size encodes kill count (cube-root scaled).
    Each death in a cluster is shown as an X mark coloured by team:
      blue X = a blue-team player died here
      red  X = a red-team player died here
    Faint white lines connect the cluster centre to each death mark so the
    spatial relationship between deaths in the same fight is clear.
    """
    base = Image.open(map_path).convert("RGBA")
    img_w, img_h = base.size
    overlay = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    draw    = ImageDraw.Draw(overlay)

    base_r   = _game_units_to_px(350, img_w)
    font_num = _load_font(max(18, img_w // 220))

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

        x_arm = max(5, r // 6)  # half-width of each X stroke
        line_w = max(2, r // 18)

        for kill in cluster["members"]:
            kx, ky = game_to_pixel(kill["x"], kill["y"], img_w, img_h)

            # Faint white connector line from cluster centre to death location
            draw.line([(cx, cy), (kx, ky)], fill=(255, 255, 255, 55),
                      width=max(1, line_w // 2))

            # X mark — blue if a blue player died, red if a red player died
            if 1 <= kill["victim"] <= 5:
                x_color = (120, 170, 255, 230)
            else:
                x_color = (255, 100, 100, 230)
            draw.line([(kx - x_arm, ky - x_arm), (kx + x_arm, ky + x_arm)],
                      fill=x_color, width=line_w)
            draw.line([(kx + x_arm, ky - x_arm), (kx - x_arm, ky + x_arm)],
                      fill=x_color, width=line_w)

    # Composite circles + lines before drawing text (text always on top)
    result     = Image.alpha_composite(base, overlay)
    label_draw = ImageDraw.Draw(result)

    # Number labels at circle centres
    for ci, cluster in enumerate(sorted_clusters, 1):
        cx, cy = game_to_pixel(cluster["centroid"][0], cluster["centroid"][1], img_w, img_h)
        r      = int(base_r * (cluster["size"] ** (1 / 3)))
        bbox   = label_draw.textbbox((0, 0), str(ci), font=font_num)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        _draw_outlined_text(label_draw, (cx - tw // 2, cy - th // 2), str(ci), font_num)

    _save(result, output_path, downscale)


# ── lane aggression ───────────────────────────────────────────────────────────

def render_lane_aggression(map_path, aggression_info, output_path, downscale=4):
    """Laning-phase position density map with aggression score annotation.

    Purpose: shows where the player spent the first 15 minutes. The orange/amber
    density cloud reveals movement patterns and zone control; the avg-position
    marker summarises overall lane presence. The aggression score (0–100) measures
    how far forward the player was positioned relative to the two bases:
      0  = camped under own tower
      50 = neutral / river
      100 = always at enemy tower

    Density is built with a numpy accumulation grid (same technique as the XP
    heatmap) so even sparse position data produces a legible cloud.
    """
    base = Image.open(map_path).convert("RGBA")
    img_w, img_h = base.size

    laning_positions = aggression_info.get("laning_positions", [])

    if laning_positions:
        # ── numpy density grid ──────────────────────────────────────────────
        # Work at quarter resolution for speed; upscale the overlay at the end
        GRID_DIV = 4
        gw, gh   = img_w // GRID_DIV, img_h // GRID_DIV
        grid     = np.zeros((gh, gw), dtype=np.float32)

        # Each sample contributes to a ~500-unit radius patch in the grid
        blob_r = max(3, _game_units_to_px(500, img_w) // GRID_DIV)

        for x, y in laning_positions:
            px, py = game_to_pixel(x, y, img_w, img_h)
            gx, gy = px // GRID_DIV, py // GRID_DIV
            x0, x1 = max(0, gx - blob_r), min(gw, gx + blob_r + 1)
            y0, y1 = max(0, gy - blob_r), min(gh, gy + blob_r + 1)
            grid[y0:y1, x0:x1] += 1.0

        # Normalise to [0,1] then blur so nearby samples merge into smooth zones
        norm_img = Image.fromarray(
            (np.clip(grid / (grid.max() + 1e-9), 0, 1) * 255).astype(np.uint8), "L"
        )
        norm_img = norm_img.filter(ImageFilter.GaussianBlur(radius=max(2, blob_r)))
        grid     = np.asarray(norm_img, dtype=np.float32) / 255.0

        # Custom colormap: gold (sparse) → amber → red-orange (dense)
        # Gold at the low end contrasts with the map's greens so faint laning
        # zones stay legible; the warm shift toward red marks heavily-occupied areas.
        from matplotlib.colors import LinearSegmentedColormap
        agg_cmap = LinearSegmentedColormap.from_list(
            "aggression",
            [(0.0, "#FFD700"),   # gold       — low density, distinct from map
             (0.5, "#FF8C00"),   # amber      — mid density
             (1.0, "#FF2200")],  # red-orange — high density
        )
        threshold = 0.03
        min_alpha = 0.20
        max_alpha = 0.82
        alpha_float    = np.where(
            grid > threshold,
            min_alpha + np.clip((grid - threshold) / (1 - threshold), 0, 1) * (max_alpha - min_alpha),
            0,
        )
        rgba_f         = agg_cmap(grid)
        rgba_f[..., 3] = alpha_float
        rgba           = (rgba_f * 255).astype(np.uint8)

        overlay = Image.fromarray(rgba, "RGBA").resize((img_w, img_h), Image.LANCZOS)
        result  = Image.alpha_composite(base, overlay)
    else:
        result = base.copy()

    # ── average-position marker ──────────────────────────────────────────────
    markers = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    mdraw   = ImageDraw.Draw(markers)
    ax_px, ay_px = game_to_pixel(
        aggression_info["avg_pos"][0], aggression_info["avg_pos"][1], img_w, img_h
    )
    mr = max(20, img_w // 180)
    # Outer glow
    mdraw.ellipse([ax_px - mr - 10, ay_px - mr - 10, ax_px + mr + 10, ay_px + mr + 10],
                  fill=(255, 165, 0, 70))
    # Main dot with white ring
    mdraw.ellipse([ax_px - mr, ay_px - mr, ax_px + mr, ay_px + mr],
                  fill=(255, 165, 0, 240), outline=(255, 255, 255, 255),
                  width=max(3, mr // 5))
    result = Image.alpha_composite(result, markers)

    # ── annotation overlay ───────────────────────────────────────────────────
    # Font sizes are specified at full render resolution; they read correctly
    # after downscale (e.g. img_w // 90 = 91px at 8192 → ~23px at 2048 output).
    fdraw    = ImageDraw.Draw(result)
    font_med = _load_font(max(15, img_w // 90))
    font_sm  = _load_font(max(11, img_w // 130))

    score       = aggression_info["score"]
    description = aggression_info["description"]
    lane        = aggression_info["lane"]

    bx    = img_w // 40
    by    = img_w // 30
    bar_w = img_w // 5
    bar_h = max(12, img_w // 100)

    # Gauge background track
    fdraw.rectangle([bx, by, bx + bar_w, by + bar_h], fill=(20, 20, 20, 200))
    fill_w    = int(bar_w * score / 100)
    bar_color = ((30, 100, 255, 220)  if score < 44
                 else (50, 200, 90, 220) if score < 58
                 else (255, 130, 30, 220))
    fdraw.rectangle([bx, by, bx + fill_w, by + bar_h], fill=bar_color)

    # "Defensive < ... > Aggressive" axis labels above the bar
    axis_y = by - max(16, img_w // 220) - 4
    _draw_outlined_text(fdraw, (bx, axis_y),
                        "Defensive <", font_sm, fill=(100, 150, 255))
    agg_label = "> Aggressive"
    aw = fdraw.textbbox((0, 0), agg_label, font=font_sm)[2]
    _draw_outlined_text(fdraw, (bx + bar_w - aw, axis_y),
                        agg_label, font_sm, fill=(255, 130, 50))

    # Labels below the gauge
    label_y = by + bar_h + max(4, img_w // 700)
    _draw_outlined_text(
        fdraw, (bx, label_y),
        f"{lane} Lane  |  Aggression {score}/100  —  {description}",
        font_med
    )
    _draw_outlined_text(
        fdraw, (bx, label_y + max(18, img_w // 90)),
        "Orange = first-15-min positions  |  Circle = avg position",
        font_sm, fill=(200, 200, 200)
    )

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

    # Marker styles: combat events (upper half) and objective events (lower half)
    # towers and objectives are merged — both counted as map objectives
    EVENT_STYLES = {
        "kills":      dict(marker="^", color="#44ff88", s=80,  zorder=5, label="Kill"),
        "deaths":     dict(marker="X", color="#ff4444", s=80,  zorder=5, label="Death"),
        "assists":    dict(marker="D", color="#44ddff", s=40,  zorder=4, label="Assist"),
        "objectives": dict(marker="*", color="#FFD700", s=140, zorder=5, label="Objective"),
    }

    game_end = stats["duration_min"]
    minutes  = [r["minute"]      for r in per_minute]
    cs_bars  = [r["cs_gained"]   for r in per_minute]
    gd_bars  = [r["gold_gained"] for r in per_minute]

    # ── figure / grid layout ─────────────────────────────────────────────────
    fig = plt.figure(figsize=(18, 10), facecolor=BG)
    gs  = GridSpec(4, 2, figure=fig,
                   width_ratios=[5, 1],
                   height_ratios=[0.4, 3.0, 0.9, 3.0],
                   hspace=0.04, wspace=0.04,
                   left=0.05, right=0.98, top=0.93, bottom=0.06)

    ax_strip  = fig.add_subplot(gs[0, 0])
    ax_cs     = fig.add_subplot(gs[1, 0], sharex=ax_strip)
    ax_center = fig.add_subplot(gs[2, 0], sharex=ax_strip)
    ax_gold   = fig.add_subplot(gs[3, 0], sharex=ax_strip)
    ax_info   = fig.add_subplot(gs[:, 1])

    for ax in (ax_cs, ax_strip, ax_center, ax_gold):
        ax.set_facecolor(PANEL)
        ax.tick_params(colors=TEXT, labelsize=8)
        for spine in ["top", "right"]:
            ax.spines[spine].set_visible(False)
        for spine in ["bottom", "left"]:
            ax.spines[spine].set_color(GRID_C)

    # ── row 0: activity colour strip (top) ───────────────────────────────────
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
    ax_strip.legend(handles=patches,
                    bbox_to_anchor=(1.0, 0.5), loc="center right",
                    labelcolor=TEXT, facecolor=BG, edgecolor="none",
                    fontsize=7, ncol=2, borderpad=0.5, handlelength=1,
                    handletextpad=0.5)

    # ── row 1: CS per minute (bars up) ───────────────────────────────────────
    avg_cs = sum(cs_bars) / len(cs_bars) if cs_bars else 0
    ax_cs.bar(minutes, cs_bars, color="#4CAF50", alpha=0.85, width=0.8)
    ax_cs.axhline(avg_cs, color="#aaffaa", linestyle="--", linewidth=1,
                  label=f"avg {avg_cs:.1f} CS/min")
    ax_cs.set_ylabel("CS / min", color=TEXT, fontsize=9)
    ax_cs.grid(axis="y", color=GRID_C, linewidth=0.5, alpha=0.7)
    ax_cs.spines["bottom"].set_visible(False)
    ax_cs.tick_params(bottom=False, labelbottom=False)
    ax_cs.legend(loc="upper left", labelcolor=TEXT, facecolor=BG,
                 edgecolor=GRID_C, fontsize=7, markerscale=0.9)

    # ── row 2: centre event band ──────────────────────────────────────────────
    ax_center.set_yticks([])
    ax_center.set_xlim(ax_strip.get_xlim())
    ax_center.set_ylim(-1.3, 1.3)
    ax_center.spines["top"].set_visible(False)
    ax_center.spines["bottom"].set_visible(False)
    ax_center.spines["left"].set_visible(False)
    ax_center.tick_params(bottom=False, labelbottom=False)
    ax_center.axhline(0, color=ACCENT, linewidth=1.0, alpha=0.4, zorder=2)

    # Y positions within ax_center's [-1.3, 1.3] axis; 0 is the centre line (ACCENT colour).
    # Combat events sit above centre, death/objective markers below.
    # towers and objectives are merged — collect both time lists under "objectives"
    CENTER_Y = {
        "kills":       0.90,
        "assists":     0.45,
        "deaths":     -0.45,
        "objectives": -0.90,
    }
    if events_at_time:
        center_handles = []
        for key, y_pos in CENTER_Y.items():
            style = EVENT_STYLES.get(key)
            if style is None:
                continue
            # merge towers into objectives
            times = list(events_at_time.get(key, []))
            if key == "objectives":
                times = sorted(times + list(events_at_time.get("towers", [])))
            if times:
                h = ax_center.scatter(times, [y_pos] * len(times),
                                      marker=style["marker"], color=style["color"],
                                      s=style["s"], zorder=style["zorder"],
                                      label=style["label"])
                center_handles.append(h)
        if center_handles:
            ax_center.legend(handles=center_handles,
                             bbox_to_anchor=(1.0, 0.5), loc="center right",
                             labelcolor=TEXT, facecolor=BG, edgecolor=GRID_C,
                             fontsize=7, ncol=1, markerscale=0.9,
                             borderpad=0.5, handletextpad=0.5)

    # ── row 3: gold per minute (bars down) ───────────────────────────────────
    ax_gold.bar(minutes, gd_bars, color="#FFD700", alpha=0.85, width=0.8)
    ax_gold.invert_yaxis()
    ax_gold.spines["top"].set_visible(False)
    ax_gold.set_ylabel("Gold / min", color=TEXT, fontsize=9)
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
