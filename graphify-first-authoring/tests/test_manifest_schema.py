"""Schema check for this molecule's manifest.json (T007, FR-001).

Validates the molecule's manifest against spaex Spec 014's canonical
``molecule-manifest.v4.schema.json`` using the repo's existing ``jsonschema``
dependency, without pulling in any spaex CLI machinery.
"""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema

_ATOM_DIR = Path(__file__).resolve().parent.parent
_MOLECULE_MANIFEST = _ATOM_DIR / "manifest.json"
_SCHEMA = Path(__file__).resolve().parent / "molecule-manifest.v4.schema.json"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_manifest_conforms_to_v4_schema() -> None:
    schema = _load_json(_SCHEMA)
    manifest = _load_json(_MOLECULE_MANIFEST)
    jsonschema.validate(instance=manifest, schema=schema)


def test_manifest_declares_expected_identity() -> None:
    manifest = _load_json(_MOLECULE_MANIFEST)
    assert manifest["id"] == "com.github.haexmas.atoms.graphify-first-authoring"
    assert manifest["spaex_version"] == "4"
    assert manifest["atoms"]["constitution"] == ["constitution.md"]


def test_contributed_constitution_file_exists() -> None:
    manifest = _load_json(_MOLECULE_MANIFEST)
    rel = manifest["atoms"]["constitution"][0]
    assert (_MOLECULE_MANIFEST.parent / rel).is_file()
