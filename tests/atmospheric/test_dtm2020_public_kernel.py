from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import math
import tempfile
import unittest

from elara_x.atmospheric.dtm2020_external_resource import CANONICAL_RESOURCE_NAMES
from elara_x.atmospheric.dtm2020_public_kernel import (
    DTM2020Input,
    DTM2020NumericalKernelNotActivatedError,
    DTM2020OperationalDrivers,
    DTM2020PublicSpecKernel,
    DTM2020ResourceRequiredError,
    PUBLIC_SPEC_LABEL,
    annual_phase_rad,
    day_of_year,
    g_per_cm3_to_kg_per_m3,
    local_solar_time_hours,
    normalise_longitude_deg,
    validate_input,
)


def sample_input(**overrides):
    drivers = DTM2020OperationalDrivers(
        f107_daily_sfu=150.0,
        f107_81day_mean_sfu=145.0,
        kp_3h_delayed=4.0,
        kp_24h_mean=3.0,
    )
    values = dict(
        utc=datetime(2024, 2, 29, 12, 0, tzinfo=timezone.utc),
        altitude_km=400.0,
        latitude_deg=10.0,
        longitude_deg=30.0,
        drivers=drivers,
    )
    values.update(overrides)
    return DTM2020Input(**values)


class DTM2020PublicKernelTests(unittest.TestCase):
    def test_local_solar_time(self):
        utc = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
        self.assertAlmostEqual(local_solar_time_hours(utc, 30.0), 14.0)
        self.assertAlmostEqual(local_solar_time_hours(utc, -45.0), 9.0)

    def test_longitude_normalisation(self):
        self.assertAlmostEqual(normalise_longitude_deg(190.0), -170.0)
        self.assertAlmostEqual(normalise_longitude_deg(-190.0), 170.0)

    def test_leap_year_day_of_year(self):
        utc = datetime(2024, 2, 29, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(day_of_year(utc), 60)

    def test_annual_phase_is_finite(self):
        self.assertTrue(math.isfinite(annual_phase_rad(sample_input().utc)))

    def test_driver_values_retained_without_guessed_normalisation(self):
        clean = validate_input(sample_input())
        self.assertEqual(clean.drivers.f107_daily_sfu, 150.0)
        self.assertEqual(clean.drivers.f107_81day_mean_sfu, 145.0)
        self.assertEqual(clean.drivers.kp_3h_delayed, 4.0)
        self.assertEqual(clean.drivers.kp_24h_mean, 3.0)

    def test_invalid_altitude_rejected(self):
        with self.assertRaises(ValueError):
            validate_input(sample_input(altitude_km=100.0))

    def test_invalid_latitude_rejected(self):
        with self.assertRaises(ValueError):
            validate_input(sample_input(latitude_deg=91.0))

    def test_invalid_kp_rejected(self):
        bad = DTM2020OperationalDrivers(150.0, 145.0, 9.5, 3.0)
        with self.assertRaises(ValueError):
            validate_input(sample_input(drivers=bad))

    def test_naive_datetime_rejected(self):
        with self.assertRaises(ValueError):
            validate_input(sample_input(utc=datetime(2024, 1, 1, 0, 0)))

    def test_density_unit_conversion(self):
        self.assertAlmostEqual(g_per_cm3_to_kg_per_m3(1.0e-12), 1.0e-9)

    def test_prepare_state_without_resource_is_allowed_but_non_authoritative(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "project"
            project.mkdir()
            kernel = DTM2020PublicSpecKernel(project_root=project, resource_env={})
            state = kernel.prepare_state(sample_input())
            self.assertEqual(state.implementation_label, PUBLIC_SPEC_LABEL)
            self.assertEqual(state.resource_status, "RESOURCE_REQUIRED")
            self.assertAlmostEqual(state.local_solar_time_hours, 14.0)

    def test_evaluate_without_resource_refuses(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "project"
            project.mkdir()
            kernel = DTM2020PublicSpecKernel(project_root=project, resource_env={})
            with self.assertRaises(DTM2020ResourceRequiredError):
                kernel.evaluate(sample_input())

    def test_evaluate_with_external_fixture_still_refuses_numerical_claim(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            project = root / "project"
            external = root / "external"
            project.mkdir()
            external.mkdir()
            resource = external / CANONICAL_RESOURCE_NAMES[0]
            resource.write_bytes(b"fixture-only-not-official-coefficients")
            kernel = DTM2020PublicSpecKernel(
                project_root=project,
                explicit_resource_path=resource,
                resource_env={},
            )
            with self.assertRaises(DTM2020NumericalKernelNotActivatedError):
                kernel.evaluate(sample_input())


if __name__ == "__main__":
    unittest.main(verbosity=2)
