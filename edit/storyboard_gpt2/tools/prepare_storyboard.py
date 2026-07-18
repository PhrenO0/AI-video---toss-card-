import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


FRAME_SIZE = (1080, 1920)
THUMB_SIZE = (360, 640)
SHEET_SIZE = (1488, 2688)


def prepare_all(raw_dir: Path, final_dir: Path, sheet_path: Path) -> None:
    names = [f"S{index:02}.png" for index in range(1, 14)]
    missing = [name for name in names if not (raw_dir / name).is_file()]
    if missing:
        raise ValueError(f"missing frames: {', '.join(missing)}")

    final_dir.mkdir(parents=True, exist_ok=True)
    prepared: list[tuple[str, Image.Image]] = []
    for name in names:
        with Image.open(raw_dir / name) as source:
            frame = ImageOps.fit(
                source.convert("RGB"),
                FRAME_SIZE,
                Image.Resampling.LANCZOS,
            )
            frame.save(final_dir / name, format="PNG", optimize=True)
            prepared.append((name, frame.copy()))

    sheet = Image.new("RGB", SHEET_SIZE, (18, 22, 28))
    draw = ImageDraw.Draw(sheet)
    for index, (name, frame) in enumerate(prepared):
        column = index % 4
        row = index // 4
        x = 24 + column * 366
        y = 24 + row * 666
        thumb = ImageOps.fit(frame, THUMB_SIZE, Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x, y + 22))
        draw.text((x, y), name.removesuffix(".png"), fill=(240, 244, 250))

    sheet_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(sheet_path, format="PNG", optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", required=True, type=Path)
    parser.add_argument("--final", required=True, type=Path)
    parser.add_argument("--sheet", required=True, type=Path)
    args = parser.parse_args()
    prepare_all(args.raw, args.final, args.sheet)


if __name__ == "__main__":
    main()
