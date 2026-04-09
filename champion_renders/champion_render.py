"""
champion_render — builds the base 1920x1080 image for match visualizations.

Pipeline:
    default_images  →  resized_images  →  renders

Panel layout:
    timeline  (0, 0,     1920, 432)  — top 40%, filled by caller
    bottom    (0, 432,   1920, 1080) — champion floats bottom-right
"""

import pathlib
from PIL import Image

# -------------------------------------------------
# Paths
# -------------------------------------------------
BASE_DIR         = pathlib.Path(__file__).parent
_DEFAULT_DIR     = BASE_DIR / "champion_pngs" / "default_images"
_RESIZED_DIR     = BASE_DIR / "champion_pngs" / "resized_images"
_RENDERS_DIR     = BASE_DIR / "renders"
_BG_PATH         = BASE_DIR / "bg_image.png"

# -------------------------------------------------
# Canvas config
# -------------------------------------------------
CANVAS_W = 1920
CANVAS_H = 1080

TIMELINE_H = int(CANVAS_H * 0.40)  # 432
FRAME_WIDTH  = int(CANVAS_W * 0.30)   # 576
FRAME_HEIGHT = int(CANVAS_H * 0.60)   # 648

# tweak this (0.0 = center, 0.15 = slightly lower, 0.25 = aggressive)
VERTICAL_BIAS = 0.12

# -------------------------------------------------
# Background (optional)
# -------------------------------------------------
_BG: Image.Image | None = (
    Image.open(_BG_PATH).convert("RGBA").resize((CANVAS_W, CANVAS_H), Image.LANCZOS)
    if _BG_PATH.exists() else None
)

# -------------------------------------------------
# Stage 1 → 2: Normalize image (aspect-fit + biased center)
# -------------------------------------------------
def normalize_image(input_path: pathlib.Path, output_path: pathlib.Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(input_path) as img:
        img = img.convert("RGBA")

        # --- preserve aspect ratio ---
        scale = min(FRAME_WIDTH / img.width, FRAME_HEIGHT / img.height)
        new_w = int(img.width * scale)
        new_h = int(img.height * scale)

        resized = img.resize((new_w, new_h), Image.LANCZOS)

        canvas = Image.new("RGBA", (FRAME_WIDTH, FRAME_HEIGHT), (0, 0, 0, 0))

        # --- horizontal center ---
        x = (FRAME_WIDTH - new_w) // 2

        # --- vertical biased center ---
        base_y = (FRAME_HEIGHT - new_h) // 2
        bias_shift = int((FRAME_HEIGHT - new_h) * VERTICAL_BIAS)
        y = base_y + bias_shift

        canvas.paste(resized, (x, y))
        canvas.save(output_path)


def get_or_create_resized(champion: str) -> pathlib.Path:
    input_path = _DEFAULT_DIR / f"{champion.lower()}.png"
    output_path = _RESIZED_DIR / f"{champion.lower()}.png"

    if not input_path.exists():
        available = [p.stem for p in _DEFAULT_DIR.glob("*.png")]
        raise ValueError(
            f"No default image for {champion!r}. Available: {available}"
        )

    if not output_path.exists():
        normalize_image(input_path, output_path)

    return output_path

# -------------------------------------------------
# Stage 3: Build base render
# -------------------------------------------------
def new_base_img(champion: str) -> Image.Image:
    resized_path = get_or_create_resized(champion)

    canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (255, 255, 255, 255))

    if _BG:
        canvas.alpha_composite(_BG)

    champ_img = Image.open(resized_path).convert("RGBA")

    # bottom-right placement of frame
    x = CANVAS_W - FRAME_WIDTH
    y = CANVAS_H - FRAME_HEIGHT

    canvas.alpha_composite(champ_img, dest=(x, y))

    return canvas

# -------------------------------------------------
# Final cache
# -------------------------------------------------
def get_or_create(champion: str) -> Image.Image:
    _RENDERS_DIR.mkdir(exist_ok=True)
    out_path = _RENDERS_DIR / f"{champion.lower()}.png"

    if out_path.exists():
        return Image.open(out_path).convert("RGBA")

    img = new_base_img(champion)
    return img

# -------------------------------------------------
# Entry
# -------------------------------------------------
if __name__ == "__main__":
    img = get_or_create("Amumu")
    img = get_or_create("Ahri")
    img = get_or_create("Viego")



from dataclasses import dataclass

@dataclass(frozen=True)
class Rect:
    x: int
    y: int
    width: int
    height: int

    @property
    def right(self) -> int:
        return self.x + self.width

    @property
    def bottom(self) -> int:
        return self.y + self.height


@dataclass(frozen=True)
class TemplateMetaData:
    canvas_width: int
    canvas_height: int

    timeline: Rect        # top 40%
    champion_frame: Rect  # bottom-right frame (occupied)
    left_panel: Rect      # space left of champion


# -------------------------------------------------
# Public accessor
# -------------------------------------------------
def get_template_metadata() -> TemplateMetaData:
    """
    Returns layout metadata for the template.

    Spaces:
        - timeline: full width, top 40%
        - left_panel: area left of champion in bottom section
    """

    timeline = Rect(
        x=0,
        y=0,
        width=CANVAS_W,
        height=TIMELINE_H
    )

    champion_frame = Rect(
        x=CANVAS_W - FRAME_WIDTH,
        y=CANVAS_H - FRAME_HEIGHT,
        width=FRAME_WIDTH,
        height=FRAME_HEIGHT
    )

    left_panel = Rect(
        x=0,
        y=TIMELINE_H,
        width=champion_frame.x,   # everything left of champ
        height=FRAME_HEIGHT
    )

    return TemplateMetaData(
        canvas_width=CANVAS_W,
        canvas_height=CANVAS_H,
        timeline=timeline,
        champion_frame=champion_frame,
        left_panel=left_panel
    )