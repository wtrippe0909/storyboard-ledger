"""Regression tests for storyboard_to_prompts.py (stdlib unittest, no dependencies).

Run from the repo root:  python3 -m unittest discover -s tests
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import storyboard_to_prompts as sp  # noqa: E402

HEADER = "| Panel ID | Framing & Angle | Movement | Visual Action & Blocking | Audio | Duration | Transition |"
DIVIDER = "|---|---|---|---|---|---|---|"


def table(*rows: str) -> str:
    return "\n".join([HEADER, DIVIDER, *rows])


def parse(md: str):
    return sp.parse_storyboard_markdown(md)


class CameraExpansionTests(unittest.TestCase):
    def test_cu_kept_when_mcu_also_present(self):
        out = sp.expand_camera_tags("MCU", "CU STATIC")
        self.assertIn(sp.CAMERA_EXPANSIONS["MCU"], out)
        self.assertIn(sp.CAMERA_EXPANSIONS["CU"], out)

    def test_ws_kept_when_vws_also_present(self):
        out = sp.expand_camera_tags("VWS", "WS")
        self.assertIn(sp.CAMERA_EXPANSIONS["VWS"], out)
        self.assertIn(sp.CAMERA_EXPANSIONS["WS"], out)

    def test_multiword_tag_still_suppresses_its_own_prefix(self):
        out = sp.expand_camera_tags("MS", "DOLLY IN")
        self.assertIn(sp.CAMERA_EXPANSIONS["DOLLY IN"], out)
        self.assertNotIn(sp.CAMERA_EXPANSIONS["DOLLY"], out)

        out = sp.expand_camera_tags("WS", "ZOOM IN then ZOOM OUT")
        self.assertIn(sp.CAMERA_EXPANSIONS["ZOOM IN"], out)
        self.assertIn(sp.CAMERA_EXPANSIONS["ZOOM OUT"], out)
        self.assertNotIn(sp.CAMERA_EXPANSIONS["ZOOM"], out)

    def test_speed_modifier_and_fallback_unchanged(self):
        self.assertEqual(
            sp.expand_camera_tags("CU", "FAST PUSH IN"),
            ", ".join([sp.CAMERA_EXPANSIONS["PUSH IN"], sp.CAMERA_EXPANSIONS["CU"],
                       "high velocity motion"]),
        )
        self.assertEqual(sp.expand_camera_tags("`odd`", "spiral"), "odd, spiral")


class MultiTableTests(unittest.TestCase):
    MD = "\n".join([
        table("| SC01-P01 | MCU | STATIC | Subject: Ana | SFX | 2s | CUT |"),
        "",
        table("| SC01-P02 | WS | PAN | Subject: Bo | - | 3s | CUT |"),
    ])

    def test_second_table_header_is_not_a_panel(self):
        ids = [p["panel_id"] for p in parse(self.MD)]
        self.assertEqual(ids, ["SC01-P01", "SC01-P02"])

    def test_strict_accepts_valid_multi_table_file(self):
        self.assertEqual(sp.validate_markdown(self.MD), [])

    def test_strict_checks_every_header(self):
        bad = "\n".join([table("| SC01-P01 | MCU | STATIC | Subject: Ana | SFX | 2s | CUT |"), "",
                         "| Panel ID | Framing | Movement | Visual | Audio | Duration |", DIVIDER,
                         "| SC01-P02 | WS | PAN | Subject: Bo | - | 3s | CUT |"])
        errors = sp.validate_markdown(bad)
        self.assertTrue(any("transition" in e for e in errors), errors)


class SourceLineTests(unittest.TestCase):
    def test_trailing_and_separating_blank_lines_excluded(self):
        md = table(
            "| SC01-P01 | MCU | STATIC | Subject: Ana | SFX | 2s | CUT |",
            "",
            "| SC01-P02 | WS | PAN | Subject: Bo | - | 3s | CUT |",
        ) + "\n\n\n"
        lines = {p["panel_id"]: p["source_lines"] for p in parse(md)}
        self.assertEqual(lines, {"SC01-P01": "3", "SC01-P02": "5"})

    def test_wrapped_row_spans_its_continuation_lines(self):
        # Multi-line relayed format: wrapped cell content on non-pipe lines.
        md = "\n".join([HEADER, DIVIDER,
                        "| SC04-P01 | WS | PUSH IN | Subject: Marcus",
                        "Action: turns sharply",
                        "Focal Point: eyes | SFX: siren | 1.5s | CUT |",
                        ""])
        [panel] = parse(md)
        self.assertEqual(panel["source_lines"], "3-5")
        self.assertEqual(panel["action"], "turns sharply")
        self.assertEqual(panel["focal_point"], "eyes")


if __name__ == "__main__":
    unittest.main()
