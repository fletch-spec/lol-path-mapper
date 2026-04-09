from champion_render import get_or_create, get_template_metadata
from pathlib import Path

def save_template_to(champion_name: str, output_dir: Path, overwrite=False):
    output_dir.mkdir(parents=True, exist_ok=True)

    img = get_or_create(champion_name)

    output_path = output_dir / f"{champion_name.lower()}.png"
    if Path.exists(output_path) & (not overwrite):
        print(f"save_template_to: {output_path} already exists.")
    else:
        img.convert("RGB").save(output_path)

def get_meta_data(): return get_template_metadata()

if __name__ == "__main__":
    save_template_to(
        "Zac",
        Path("C:/dev/league-of-legends/outputs/_temp_output")
    )

    print(get_meta_data().champion_frame)


