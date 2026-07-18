import importlib.util
from pathlib import Path

import pytest
from PIL import Image


MODULE_PATH = Path(__file__).parents[1] / "tools" / "prepare_storyboard.py"
SPEC = importlib.util.spec_from_file_location("prepare_storyboard", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)
prepare_all = MODULE.prepare_all


def make_main_frames(tmp_path: Path) -> Path:
    raw = tmp_path / "raw"
    raw.mkdir()
    for index in range(1, 14):
        Image.new("RGB", (1200, 1600), (index * 10, 20, 30)).save(
            raw / f"S{index:02}.png"
        )
    return raw


def test_prepare_all_keeps_legacy_sheet_without_auxiliary(tmp_path: Path) -> None:
    raw = make_main_frames(tmp_path)
    final = tmp_path / "final"
    sheet = tmp_path / "contact-sheet.png"
    prepare_all(raw, final, sheet)

    outputs = sorted(final.glob("S*.png"))
    assert len(outputs) == 13
    assert all(Image.open(path).size == (1080, 1920) for path in outputs)
    assert Image.open(sheet).size == (1488, 2688)


def test_prepare_all_normalizes_four_auxiliary_frames_and_extends_sheet(
    tmp_path: Path,
) -> None:
    raw = make_main_frames(tmp_path)
    auxiliary_raw = tmp_path / "auxiliary-raw"
    auxiliary_raw.mkdir()
    for name in ("S03A.png", "S03B.png", "S05A.png", "S05B.png"):
        Image.new("RGB", (1600, 1200), (60, 80, 100)).save(auxiliary_raw / name)
    final = tmp_path / "final"
    auxiliary_final = tmp_path / "auxiliary-final"
    sheet = tmp_path / "contact-sheet.png"

    prepare_all(raw, final, sheet, auxiliary_raw, auxiliary_final)

    assert sorted(path.name for path in auxiliary_final.glob("*.png")) == [
        "S03A.png", "S03B.png", "S05A.png", "S05B.png"
    ]
    assert all(
        Image.open(path).size == (1080, 1920)
        for path in auxiliary_final.glob("*.png")
    )
    assert Image.open(sheet).size == (1488, 3354)


def test_prepare_all_rejects_one_sided_auxiliary_configuration(
    tmp_path: Path,
) -> None:
    raw = make_main_frames(tmp_path)
    with pytest.raises(ValueError, match="auxiliary raw and final directories"):
        prepare_all(
            raw,
            tmp_path / "final",
            tmp_path / "contact-sheet.png",
            tmp_path / "auxiliary-raw",
            None,
        )
