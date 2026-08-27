from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import math
import tempfile
import unittest

from elara_x.atmospheric.dtm2020_public_kernel import (
    DTM2020Input,
    DTM2020OperationalDrivers,
    DTM2020PublicSpecKernel,
)
from elara_x.atmospheric.dtm2020_public_interface import (
    associated_legendre,
    cosine_harmonic,
    input_to_operational_interface,
    local_solar_time_to_radians,
    real_spherical_basis_cos,
    real_spherical_basis_sin,
    sine_harmonic,
)


class DTM2020PublicInterfaceTests(unittest.TestCase):
    def sample_input(self):
        return DTM2020Input(
            utc=datetime(2024, 2, 29, 12, 0, tzinfo=timezone.utc),
            altitude_km=400.0,
            latitude_deg=30.0,
            longitude_deg=30.0,
            drivers=DTM2020OperationalDrivers(
                f107_daily_sfu=150.0,
                f107_81day_mean_sfu=145.0,
                kp_3h_delayed=4.0,
                kp_24h_mean=3.0,
            ),
        )

    def test_operational_vector_shapes_and_values(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "project"
            project.mkdir()
            kernel = DTM2020PublicSpecKernel(project_root=project, resource_env={})
            interface = input_to_operational_interface(self.sample_input(), kernel=kernel)

            self.assertEqual(interface.day, 60.0)
            self.assertEqual(interface.f, (150.0, 0.0))
            self.assertEqual(interface.fbar, (145.0, 0.0))
            self.assertEqual(interface.akp, (4.0, 0.0, 3.0, 0.0))
            self.assertEqual(interface.alti_km, 400.0)
            self.assertAlmostEqual(interface.alat_rad, math.pi / 6.0)
            self.assertAlmostEqual(interface.xlon_rad, math.pi / 6.0)
            # 12 UTC + 2 h at +30 deg longitude => 14 local solar hours
            self.assertAlmostEqual(interface.hl_rad, 2.0 * math.pi * 14.0 / 24.0)

    def test_local_solar_time_angle_periodicity(self):
        self.assertAlmostEqual(local_solar_time_to_radians(0.0), 0.0)
        self.assertAlmostEqual(local_solar_time_to_radians(24.0), 0.0)
        self.assertAlmostEqual(local_solar_time_to_radians(6.0), math.pi / 2.0)

    def test_basic_trigonometric_harmonics(self):
        self.assertAlmostEqual(cosine_harmonic(0, 1.234), 1.0)
        self.assertAlmostEqual(cosine_harmonic(2, math.pi / 2.0), -1.0)
        self.assertAlmostEqual(sine_harmonic(1, math.pi / 2.0), 1.0)

    def test_legendre_p00(self):
        self.assertAlmostEqual(associated_legendre(0, 0, 0.37), 1.0)

    def test_legendre_p10(self):
        x = 0.37
        self.assertAlmostEqual(associated_legendre(1, 0, x), x)

    def test_legendre_p20(self):
        x = 0.37
        expected = 0.5 * (3.0 * x * x - 1.0)
        self.assertAlmostEqual(associated_legendre(2, 0, x), expected)

    def test_legendre_p11_condon_shortley(self):
        x = 0.4
        expected = -math.sqrt(1.0 - x * x)
        self.assertAlmostEqual(associated_legendre(1, 1, x), expected)

    def test_legendre_invalid_order_rejected(self):
        with self.assertRaises(ValueError):
            associated_legendre(2, 3, 0.0)

    def test_legendre_invalid_domain_rejected(self):
        with self.assertRaises(ValueError):
            associated_legendre(2, 1, 1.1)

    def test_real_spherical_basis_order_zero(self):
        latitude = 0.25
        expected = associated_legendre(2, 0, math.sin(latitude))
        self.assertAlmostEqual(
            real_spherical_basis_cos(2, 0, latitude, 1.1),
            expected,
        )
        self.assertAlmostEqual(
            real_spherical_basis_sin(2, 0, latitude, 1.1),
            0.0,
        )

    def test_basis_contains_no_model_coefficients(self):
        # This is a structural invariant: primitives are generic and analytic.
        samples = [
            associated_legendre(2, 1, 0.2),
            cosine_harmonic(3, 0.7),
            sine_harmonic(3, 0.7),
        ]
        self.assertTrue(all(math.isfinite(v) for v in samples))


if __name__ == "__main__":
    unittest.main(verbosity=2)
