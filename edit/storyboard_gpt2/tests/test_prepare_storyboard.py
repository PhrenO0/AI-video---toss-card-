import importlib.util
from pathlib import Path

from PIL import Image


MODULE_PATH = Path(__file__).parents[1] / "tools" / "prepare_storyboard.py"
SPEC = importlib.util.spec_from_file_location("prepare_storyboard", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)
prepare_all = MODULE.prepare_all


def test_prepare_all_outputs_13_portrait_frames_and_contact_sheet(
    tmp_path: Path,
) -> None:
    raw = tmp_path / "raw"
    final = tmp_path / "final"
    raw.mkdir()
    for index in range(1, 14):
        Image.new("RGB", (1200, 1600), (index * 10, 20, 30)).save(
            raw / f"S{index:02}.png"
        )

    sheet = tmp_path / "contact-sheet.png"
    prepare_all(raw, final, sheet)

    outputs = sorted(final.glob("S*.png"))
    assert len(outputs) == 13
    assert all(Image.open(path).size == (1080, 1920) for path in outputs)
    assert Image.open(sheet).size == (1488, 2688)
