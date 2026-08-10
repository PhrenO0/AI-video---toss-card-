import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


FRAME_SIZE = (1080, 1920)
THUMB_SIZE = (360, 640)
AUXILIARY_NAMES = ("S03A.png", "S03B.png", "S05A.png", "S05B.png")
LEGACY_SHEET_SIZE = (1488, 2688)
EXTENDED_SHEET_SIZE = (1488, 3354)


def prepare_all(
    raw_dir: Path,
    final_dir: Path,
    sheet_path: Path,
    auxiliary_raw_dir: Path | None = None,
    auxiliary_final_dir: Path | None = None,
) -> None:
    if (auxiliary_raw_dir is None) != (auxiliary_final_dir is None):
        raise ValueError("auxiliary raw and final directories must be supplied together")

    names = [f"S{index:02}.png" for index in range(1, 14)]
    missing = [name for name in names if not (raw_dir / name).is_file()]
    if missing:
        raise ValueError(f"missing frames: {', '.join(missing)}")
    if auxiliary_raw_dir is not None:
        missing = [
            name for name in AUXILIARY_NAMES if not (auxiliary_raw_dir / name).is_file()
        ]
        if missing:
            raise ValueError(f"missing auxiliary frames: {', '.join(missing)}")

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

    auxiliary_prepared: list[tuple[str, Image.Image]] = []
    if auxiliary_raw_dir is not None and auxiliary_final_dir is not None:
        auxiliary_final_dir.mkdir(parents=True, exist_ok=True)
        for name in AUXILIARY_NAMES:
            with Image.open(auxiliary_raw_dir / name) as source:
                frame = ImageOps.fit(
                    source.convert("RGB"),
                    FRAME_SIZE,
                    Image.Resampling.LANCZOS,
                )
                frame.save(auxiliary_final_dir / name, format="PNG", optimize=True)
                auxiliary_prepared.append((name, frame.copy()))

    sheet_size = EXTENDED_SHEET_SIZE if auxiliary_prepared else LEGACY_SHEET_SIZE
    sheet = Image.new("RGB", sheet_size, (18, 22, 28))
    draw = ImageDraw.Draw(sheet)
    for index, (name, frame) in enumerate(prepared):
        column = index % 4
        row = index // 4
        x = 24 + column * 366
        y = 24 + row * 666
        thumb = ImageOps.fit(frame, THUMB_SIZE, Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x, y + 22))
        draw.text((x, y), name.removesuffix(".png"), fill=(240, 244, 250))

    for index, (name, frame) in enumerate(auxiliary_prepared):
        x = 24 + index * 366
        y = 2688
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
    parser.add_argument("--aux-raw", type=Path)
    parser.add_argument("--aux-final", type=Path)
    args = parser.parse_args()
    prepare_all(args.raw, args.final, args.sheet, args.aux_raw, args.aux_final)


if __name__ == "__main__":
    main()
