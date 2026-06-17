#!/usr/bin/env python3
"""Build GitHub release artifacts for the Willow Home Assistant integration."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import tomllib
import zipfile


REPO_ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "willow"
INTEGRATION_DIR = REPO_ROOT / "custom_components" / DOMAIN
MANIFEST_PATH = INTEGRATION_DIR / "manifest.json"
PYPROJECT_PATH = REPO_ROOT / "pyproject.toml"
DIST_DIR = REPO_ROOT / "dist"


EXCLUDED_DIRS = {"__pycache__"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def read_manifest() -> dict[str, object]:
    with MANIFEST_PATH.open(encoding="utf-8") as manifest_file:
        return json.load(manifest_file)


def read_version() -> str:
    with PYPROJECT_PATH.open("rb") as pyproject_file:
        data = tomllib.load(pyproject_file)
    return str(data["project"]["version"])


def iter_integration_files() -> list[Path]:
    files: list[Path] = []

    for path in sorted(INTEGRATION_DIR.rglob("*")):
        if path.is_dir():
            continue
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        if path.suffix in EXCLUDED_SUFFIXES:
            continue

        files.append(path)

    return files


def build_zip(version: str, output_dir: Path) -> Path:
    artifact_path = output_dir / "willow-home-assistant.zip"
    output_dir.mkdir(parents=True, exist_ok=True)

    if artifact_path.exists():
        artifact_path.unlink()

    manifest = read_manifest()
    manifest["version"] = version
    manifest_bytes = json.dumps(manifest, indent=2).encode("utf-8")

    with zipfile.ZipFile(
        artifact_path, "w", compression=zipfile.ZIP_DEFLATED
    ) as release_zip:
        for source_path in iter_integration_files():
            archive_path = source_path.relative_to(INTEGRATION_DIR)
            if archive_path.name == "manifest.json":
                release_zip.writestr(str(archive_path), manifest_bytes)
            else:
                release_zip.write(source_path, archive_path)

    return artifact_path


def clean_output(output_dir: Path) -> None:
    if output_dir.exists():
        shutil.rmtree(output_dir)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build Willow GitHub release artifacts."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DIST_DIR,
        help="Directory where release artifacts are written. Defaults to ./dist.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove the output directory before building.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = args.output_dir.resolve()

    if args.clean:
        clean_output(output_dir)

    version = read_version()
    artifact_path = build_zip(version, output_dir)

    print(f"Built {artifact_path}")


if __name__ == "__main__":
    main()
