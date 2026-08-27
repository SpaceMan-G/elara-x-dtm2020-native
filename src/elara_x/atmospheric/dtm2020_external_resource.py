"""Licence-isolated external-resource resolver for DTM2020.

Elara X does not distribute, copy, download, translate, embed, or log the
contents of the CNES/SWAMI-controlled DTM2020 parameter resource.

This module only:
- discovers an externally supplied authorised resource;
- validates that it remains outside the Elara X project tree;
- records metadata (resolved path, size, SHA-256, provenance label);
- returns controlled availability states.

It performs no network operation and no DTM2020 numerical calculation.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
import hashlib
import os
from pathlib import Path
from typing import Iterable

DTM2020_EXTERNAL_RESOURCE_MARKER = "ELARA_X_ATMO_M16_7R_DTM2020_EXTERNAL_RESOURCE_v1"

CANONICAL_RESOURCE_NAMES = (
    "DTM_2020_F107_Kp",
    "DTM_2020_F107_Kp.dat",
)

ENV_RESOURCE_FILE = "ELARA_X_DTM2020_RESOURCE"
ENV_RESOURCE_DIR = "ELARA_X_DTM2020_RESOURCE_DIR"


class DTM2020ResourceStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    RESOURCE_REQUIRED = "RESOURCE_REQUIRED"
    INVALID_PATH = "INVALID_PATH"
    INVALID_NAME = "INVALID_NAME"
    INSIDE_PROJECT_PROHIBITED = "INSIDE_PROJECT_PROHIBITED"
    NOT_A_REGULAR_FILE = "NOT_A_REGULAR_FILE"


@dataclass(frozen=True)
class DTM2020ResourceMetadata:
    status: str
    path: str | None
    size_bytes: int | None
    sha256: str | None
    provenance: str
    source: str | None
    content_logged: bool = False
    copied_into_project: bool = False
    downloaded_by_elara_x: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _is_within(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def default_external_resource_dirs() -> tuple[Path, ...]:
    """Return external-only user locations; never a project-relative path."""
    home = Path.home()
    return (
        home / "Library" / "Application Support" / "ElaraX" / "licensed_resources" / "dtm2020",
        home / ".local" / "share" / "ElaraX" / "licensed_resources" / "dtm2020",
    )


def candidate_paths(
    *,
    explicit_path: str | os.PathLike[str] | None = None,
    env: dict[str, str] | None = None,
) -> tuple[tuple[Path, str], ...]:
    env = dict(os.environ if env is None else env)
    rows: list[tuple[Path, str]] = []

    if explicit_path:
        rows.append((Path(explicit_path).expanduser(), "explicit"))

    file_env = (env.get(ENV_RESOURCE_FILE) or "").strip()
    if file_env:
        rows.append((Path(file_env).expanduser(), f"env:{ENV_RESOURCE_FILE}"))

    dir_env = (env.get(ENV_RESOURCE_DIR) or "").strip()
    if dir_env:
        base = Path(dir_env).expanduser()
        for name in CANONICAL_RESOURCE_NAMES:
            rows.append((base / name, f"env:{ENV_RESOURCE_DIR}"))

    for base in default_external_resource_dirs():
        for name in CANONICAL_RESOURCE_NAMES:
            rows.append((base / name, "default_external_user_store"))

    # Stable de-duplication without resolving missing paths.
    seen: set[str] = set()
    unique: list[tuple[Path, str]] = []
    for path, source in rows:
        key = str(path)
        if key not in seen:
            seen.add(key)
            unique.append((path, source))
    return tuple(unique)


def inspect_resource(
    path: str | os.PathLike[str],
    *,
    project_root: str | os.PathLike[str],
    source: str = "explicit",
    provenance: str = "USER_SUPPLIED_AUTHORISED_EXTERNAL_RESOURCE",
) -> DTM2020ResourceMetadata:
    """Inspect metadata only. Resource contents are never returned or logged."""
    project = Path(project_root).expanduser().resolve()
    raw = Path(path).expanduser()

    try:
        resolved = raw.resolve(strict=True)
    except (FileNotFoundError, OSError):
        return DTM2020ResourceMetadata(
            status=DTM2020ResourceStatus.INVALID_PATH.value,
            path=str(raw),
            size_bytes=None,
            sha256=None,
            provenance=provenance,
            source=source,
        )

    if _is_within(resolved, project):
        return DTM2020ResourceMetadata(
            status=DTM2020ResourceStatus.INSIDE_PROJECT_PROHIBITED.value,
            path=str(resolved),
            size_bytes=None,
            sha256=None,
            provenance=provenance,
            source=source,
        )

    if resolved.name not in CANONICAL_RESOURCE_NAMES:
        return DTM2020ResourceMetadata(
            status=DTM2020ResourceStatus.INVALID_NAME.value,
            path=str(resolved),
            size_bytes=None,
            sha256=None,
            provenance=provenance,
            source=source,
        )

    if not resolved.is_file():
        return DTM2020ResourceMetadata(
            status=DTM2020ResourceStatus.NOT_A_REGULAR_FILE.value,
            path=str(resolved),
            size_bytes=None,
            sha256=None,
            provenance=provenance,
            source=source,
        )

    stat = resolved.stat()
    return DTM2020ResourceMetadata(
        status=DTM2020ResourceStatus.AVAILABLE.value,
        path=str(resolved),
        size_bytes=stat.st_size,
        sha256=_sha256(resolved),
        provenance=provenance,
        source=source,
    )


def resolve_dtm2020_external_resource(
    *,
    project_root: str | os.PathLike[str],
    explicit_path: str | os.PathLike[str] | None = None,
    env: dict[str, str] | None = None,
    provenance: str = "USER_SUPPLIED_AUTHORISED_EXTERNAL_RESOURCE",
) -> DTM2020ResourceMetadata:
    """Resolve the first valid external resource without copying or downloading."""
    first_invalid: DTM2020ResourceMetadata | None = None
    for path, source in candidate_paths(explicit_path=explicit_path, env=env):
        if not path.exists():
            continue
        meta = inspect_resource(
            path,
            project_root=project_root,
            source=source,
            provenance=provenance,
        )
        if meta.status == DTM2020ResourceStatus.AVAILABLE.value:
            return meta
        if first_invalid is None:
            first_invalid = meta

    if first_invalid is not None:
        return first_invalid

    return DTM2020ResourceMetadata(
        status=DTM2020ResourceStatus.RESOURCE_REQUIRED.value,
        path=None,
        size_bytes=None,
        sha256=None,
        provenance=provenance,
        source=None,
    )


def publication_safe_metadata(metadata: DTM2020ResourceMetadata) -> dict:
    """Return metadata safe for provenance manifests; never resource contents."""
    return metadata.to_dict()
