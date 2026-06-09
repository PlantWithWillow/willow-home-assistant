from __future__ import annotations

import zipfile

from scripts import build_release


def test_build_zip_creates_hacs_release_artifact(tmp_path) -> None:
    artifact_path = build_release.build_zip("1.1.1", tmp_path)

    assert artifact_path == tmp_path / "willow-home-assistant.zip"
    assert artifact_path.exists()

    with zipfile.ZipFile(artifact_path) as artifact:
        names = set(artifact.namelist())

    assert "manifest.json" in names
    assert "sensor.py" in names
    assert all("__pycache__" not in name for name in names)
    assert all(not name.endswith(".pyc") for name in names)
