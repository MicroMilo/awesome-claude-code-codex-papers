from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_script(script: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script), *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def test_catalog_is_valid() -> None:
    result = run_script("validate.py")
    assert result.returncode == 0, result.stderr


def test_generated_readme_is_current() -> None:
    result = run_script("build_readme.py", "--check")
    assert result.returncode == 0, result.stderr
