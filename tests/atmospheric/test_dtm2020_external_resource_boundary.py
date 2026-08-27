from __future__ import annotations

import hashlib
import os
from pathlib import Path
import tempfile
import unittest

from elara_x.atmospheric.dtm2020_external_resource import (
    CANONICAL_RESOURCE_NAMES,
    DTM2020ResourceStatus,
    candidate_paths,
    inspect_resource,
    publication_safe_metadata,
    resolve_dtm2020_external_resource,
)


class DTM2020ExternalResourceBoundaryTests(unittest.TestCase):
    def test_missing_resource_returns_controlled_required_state(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "project"
            project.mkdir()
            env = {"HOME": td}
            meta = resolve_dtm2020_external_resource(project_root=project, env=env)
            self.assertEqual(meta.status, DTM2020ResourceStatus.RESOURCE_REQUIRED.value)
            self.assertIsNone(meta.sha256)
            self.assertFalse(meta.content_logged)
            self.assertFalse(meta.copied_into_project)
            self.assertFalse(meta.downloaded_by_elara_x)

    def test_external_resource_metadata_only(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            project = root / "project"
            external = root / "external"
            project.mkdir()
            external.mkdir()
            resource = external / CANONICAL_RESOURCE_NAMES[0]
            payload = b"fixture-only-not-an-official-resource\n"
            resource.write_bytes(payload)

            meta = inspect_resource(resource, project_root=project)
            self.assertEqual(meta.status, DTM2020ResourceStatus.AVAILABLE.value)
            self.assertEqual(meta.size_bytes, len(payload))
            self.assertEqual(meta.sha256, hashlib.sha256(payload).hexdigest())
            safe = publication_safe_metadata(meta)
            self.assertNotIn("contents", safe)
            self.assertNotIn("payload", safe)
            self.assertFalse(safe["content_logged"])
            self.assertFalse(safe["copied_into_project"])
            self.assertFalse(safe["downloaded_by_elara_x"])

    def test_resource_inside_project_is_prohibited(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "project"
            project.mkdir()
            resource = project / CANONICAL_RESOURCE_NAMES[0]
            resource.write_bytes(b"fixture")
            meta = inspect_resource(resource, project_root=project)
            self.assertEqual(
                meta.status,
                DTM2020ResourceStatus.INSIDE_PROJECT_PROHIBITED.value,
            )
            self.assertIsNone(meta.sha256)

    def test_wrong_resource_name_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            project = root / "project"
            project.mkdir()
            resource = root / "not_the_dtm_resource.dat"
            resource.write_bytes(b"fixture")
            meta = inspect_resource(resource, project_root=project)
            self.assertEqual(meta.status, DTM2020ResourceStatus.INVALID_NAME.value)

    def test_environment_file_path_resolves_external_resource(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            project = root / "project"
            external = root / "licensed"
            project.mkdir()
            external.mkdir()
            resource = external / CANONICAL_RESOURCE_NAMES[0]
            resource.write_bytes(b"fixture")

            env = {"ELARA_X_DTM2020_RESOURCE": str(resource)}
            meta = resolve_dtm2020_external_resource(project_root=project, env=env)
            self.assertEqual(meta.status, DTM2020ResourceStatus.AVAILABLE.value)
            self.assertEqual(meta.source, "env:ELARA_X_DTM2020_RESOURCE")

    def test_environment_directory_path_resolves_external_resource(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            project = root / "project"
            external = root / "licensed"
            project.mkdir()
            external.mkdir()
            resource = external / CANONICAL_RESOURCE_NAMES[1]
            resource.write_bytes(b"fixture")

            env = {"ELARA_X_DTM2020_RESOURCE_DIR": str(external)}
            meta = resolve_dtm2020_external_resource(project_root=project, env=env)
            self.assertEqual(meta.status, DTM2020ResourceStatus.AVAILABLE.value)
            self.assertTrue(meta.source.startswith("env:"))

    def test_resolver_performs_no_copy(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            project = root / "project"
            external = root / "external"
            project.mkdir()
            external.mkdir()
            resource = external / CANONICAL_RESOURCE_NAMES[0]
            resource.write_bytes(b"fixture")
            before = sorted(str(p.relative_to(project)) for p in project.rglob("*"))
            meta = resolve_dtm2020_external_resource(
                project_root=project,
                explicit_path=resource,
                env={},
            )
            after = sorted(str(p.relative_to(project)) for p in project.rglob("*"))
            self.assertEqual(meta.status, DTM2020ResourceStatus.AVAILABLE.value)
            self.assertEqual(before, after)

    def test_candidate_paths_never_default_inside_project(self):
        paths = candidate_paths(env={})
        for path, _source in paths:
            self.assertIn("licensed_resources", str(path))
            self.assertNotIn("Impulse_V2", str(path))


if __name__ == "__main__":
    unittest.main(verbosity=2)
