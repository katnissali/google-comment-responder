#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path


BUILD_METADATA_RE = re.compile(r"^[0-9A-Za-z.-]+$")


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_manifest(plugin_dir: Path) -> dict:
    manifest_path = plugin_dir / ".codex-plugin" / "plugin.json"
    if not manifest_path.exists():
        fail(f"missing manifest: {manifest_path}")
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {manifest_path}: {exc}")


def validate_plugin(plugin_dir: Path, manifest: dict) -> None:
    name = manifest.get("name")
    if not isinstance(name, str) or not name:
        fail("manifest must contain a non-empty string name")
    if plugin_dir.name != name:
        fail(f"plugin folder name {plugin_dir.name!r} must match manifest name {name!r}")
    if not isinstance(manifest.get("version"), str) or not manifest["version"]:
        fail("manifest must contain a non-empty string version")

    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        fail("manifest must contain an interface object")
    for key in ["displayName", "developerName", "shortDescription", "longDescription", "category"]:
        if not isinstance(interface.get(key), str) or not interface[key].strip():
            fail(f"manifest interface.{key} must be a non-empty string")
    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
        fail("manifest interface.defaultPrompt must contain 1 to 3 prompts")
    if any(not isinstance(prompt, str) or not prompt.strip() for prompt in prompts):
        fail("every default prompt must be a non-empty string")

    skills_value = manifest.get("skills")
    if not isinstance(skills_value, str):
        fail("manifest must contain a string skills path")
    skills_path = (plugin_dir / skills_value).resolve()
    if not skills_path.exists() or not skills_path.is_dir():
        fail(f"skills directory does not exist: {skills_path}")

    for asset_key in ["composerIcon", "logo"]:
        asset_value = interface.get(asset_key)
        if not isinstance(asset_value, str) or not asset_value:
            fail(f"manifest interface.{asset_key} must be a string path")
        asset_path = (plugin_dir / asset_value).resolve()
        if not asset_path.exists():
            fail(f"asset does not exist: {asset_path}")


def with_build_metadata(version: str, build_metadata: str | None) -> str:
    if not build_metadata:
        return version
    if not BUILD_METADATA_RE.fullmatch(build_metadata):
        fail("build metadata may only contain ASCII letters, digits, dots, and hyphens")
    base_version = version.split("+", 1)[0]
    return f"{base_version}+{build_metadata}"


def scan_forbidden(root: Path, forbidden_terms: list[str]) -> list[tuple[Path, str]]:
    matches: list[tuple[Path, str]] = []
    lowered_terms = [(term, term.lower()) for term in forbidden_terms if term]
    if not lowered_terms:
        return matches

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        text = path.read_bytes().decode("utf-8", errors="ignore").lower()
        for original, lowered in lowered_terms:
            if lowered in text:
                matches.append((path.relative_to(root), original))
    return matches


def zip_directory(source_dir: Path, zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source_dir.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(source_dir.parent))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate and package a Codex plugin.")
    parser.add_argument("--plugin-dir", default="plugins/google-comment-responder")
    parser.add_argument("--out", default="dist")
    parser.add_argument("--build-metadata", help="SemVer build metadata to append in the packaged ZIP only.")
    parser.add_argument("--metadata-json", help="Optional path to write package metadata JSON.")
    parser.add_argument("--forbidden", action="append", default=[], help="Forbidden string to reject.")
    args = parser.parse_args()

    plugin_dir = Path(args.plugin_dir).resolve()
    if not plugin_dir.exists():
        fail(f"plugin directory does not exist: {plugin_dir}")

    manifest = load_manifest(plugin_dir)
    validate_plugin(plugin_dir, manifest)

    forbidden_matches = scan_forbidden(plugin_dir, args.forbidden)
    if forbidden_matches:
        formatted = ", ".join(f"{path} contains {term!r}" for path, term in forbidden_matches)
        fail(f"forbidden text found: {formatted}")

    packaged_version = with_build_metadata(manifest["version"], args.build_metadata)
    output_dir = Path(args.out).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    zip_path = output_dir / f"{manifest['name']}-{packaged_version}.zip"

    with tempfile.TemporaryDirectory(prefix="plugin-package-") as tmp:
        tmp_root = Path(tmp)
        copied_plugin = tmp_root / manifest["name"]
        shutil.copytree(plugin_dir, copied_plugin)
        copied_manifest_path = copied_plugin / ".codex-plugin" / "plugin.json"
        copied_manifest = load_manifest(copied_plugin)
        copied_manifest["version"] = packaged_version
        copied_manifest_path.write_text(json.dumps(copied_manifest, indent=2) + "\n", encoding="utf-8")

        forbidden_matches = scan_forbidden(copied_plugin, args.forbidden)
        if forbidden_matches:
            formatted = ", ".join(f"{path} contains {term!r}" for path, term in forbidden_matches)
            fail(f"forbidden text found after packaging metadata update: {formatted}")

        zip_directory(copied_plugin, zip_path)

    metadata = {
        "plugin": manifest["name"],
        "version": packaged_version,
        "zip": str(zip_path),
        "zip_name": zip_path.name,
        "sha256": sha256(zip_path),
    }
    if args.metadata_json:
        metadata_path = Path(args.metadata_json)
        metadata_path.parent.mkdir(parents=True, exist_ok=True)
        metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
