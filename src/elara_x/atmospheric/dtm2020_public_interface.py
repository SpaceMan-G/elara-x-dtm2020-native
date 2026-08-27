"""Independent public-interface adapter and generic basis primitives for DTM2020.

Elara X-authored. Contains no CNES/SWAMI source, translated source, fitted
DTM2020 coefficients, coefficient ordering, or restricted parameter data.

This module implements:
- conversion of the M16.8R prepared public state into the published operational
  DTM interface shape: day, f(2), fbar(2), akp(4), altitude, local-time angle,
  latitude radians, longitude radians;
- generic independently authored trigonometric and associated-Legendre
  primitives suitable for later public environmental-basis work.

It does NOT implement fitted DTM2020 parameterisation and does NOT produce
authoritative DTM2020 density or temperature.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

from .dtm2020_public_kernel import (
    DTM2020Input,
    DTM2020PreparedState,
    DTM2020PublicSpecKernel,
    ensure_utc,
    validate_input,
)

DTM2020_PUBLIC_INTERFACE_MARKER = "ELARA_X_ATMO_M17_0R_DTM2020_PUBLIC_INTERFACE_v1"


@dataclass(frozen=True)
class DTM2020OperationalInterface:
    """Published operational input-vector shape, represented immutably."""

    day: float
    f: tuple[float, float]
    fbar: tuple[float, float]
    akp: tuple[float, float, float, float]
    alti_km: float
    hl_rad: float
    alat_rad: float
    xlon_rad: float


def local_solar_time_to_radians(hours: float) -> float:
    value = float(hours)
    if not math.isfinite(value):
        raise ValueError("local solar time must be finite")
    return 2.0 * math.pi * ((value % 24.0) / 24.0)


def prepared_state_to_operational_interface(
    state: DTM2020PreparedState,
) -> DTM2020OperationalInterface:
    """Map Elara public state to the published DTM operational call shape.

    The raw driver values are not normalised or transformed here. M16.8R already
    binds their semantic roles:
    - f107_daily_sfu: instantaneous F10.7 value prepared for the published t-24h slot
    - f107_81day_mean_sfu: 81-day mean F10.7
    - kp_3h_delayed: 3-hour delayed Kp
    - kp_24h_mean: previous-24-hour mean Kp
    """
    return DTM2020OperationalInterface(
        day=float(state.day_of_year),
        f=(float(state.drivers.f107_daily_sfu), 0.0),
        fbar=(float(state.drivers.f107_81day_mean_sfu), 0.0),
        akp=(
            float(state.drivers.kp_3h_delayed),
            0.0,
            float(state.drivers.kp_24h_mean),
            0.0,
        ),
        alti_km=float(state.altitude_km),
        hl_rad=local_solar_time_to_radians(state.local_solar_time_hours),
        alat_rad=math.radians(float(state.latitude_deg)),
        xlon_rad=math.radians(float(state.longitude_deg)),
    )


def input_to_operational_interface(
    model_input: DTM2020Input,
    *,
    kernel: DTM2020PublicSpecKernel,
) -> DTM2020OperationalInterface:
    """Validate/prepare through the frozen public kernel then adapt to interface."""
    clean = validate_input(model_input)
    state = kernel.prepare_state(clean)
    return prepared_state_to_operational_interface(state)


def cosine_harmonic(order: int, angle_rad: float) -> float:
    if int(order) != order or order < 0:
        raise ValueError("order must be a non-negative integer")
    angle = float(angle_rad)
    if not math.isfinite(angle):
        raise ValueError("angle_rad must be finite")
    return math.cos(int(order) * angle)


def sine_harmonic(order: int, angle_rad: float) -> float:
    if int(order) != order or order < 0:
        raise ValueError("order must be a non-negative integer")
    angle = float(angle_rad)
    if not math.isfinite(angle):
        raise ValueError("angle_rad must be finite")
    return math.sin(int(order) * angle)


def associated_legendre(degree: int, order: int, x: float) -> float:
    """Unnormalised associated Legendre P_l^m(x), Condon-Shortley convention.

    Standard independent recurrence; no DTM coefficient ordering is encoded.
    """
    if int(degree) != degree or int(order) != order:
        raise ValueError("degree and order must be integers")
    degree = int(degree)
    order = int(order)
    x = float(x)

    if degree < 0:
        raise ValueError("degree must be non-negative")
    if order < 0 or order > degree:
        raise ValueError("order must satisfy 0 <= order <= degree")
    if not math.isfinite(x) or x < -1.0 or x > 1.0:
        raise ValueError("x must be finite and within [-1, 1]")

    pmm = 1.0
    if order > 0:
        somx2 = math.sqrt(max(0.0, (1.0 - x) * (1.0 + x)))
        fact = 1.0
        for _ in range(1, order + 1):
            pmm *= -fact * somx2
            fact += 2.0

    if degree == order:
        return pmm

    pmmp1 = x * (2 * order + 1) * pmm
    if degree == order + 1:
        return pmmp1

    p_prev2 = pmm
    p_prev1 = pmmp1
    for ell in range(order + 2, degree + 1):
        pll = (
            (2 * ell - 1) * x * p_prev1
            - (ell + order - 1) * p_prev2
        ) / (ell - order)
        p_prev2, p_prev1 = p_prev1, pll
    return p_prev1


def real_spherical_basis_cos(
    degree: int,
    order: int,
    latitude_rad: float,
    phase_rad: float,
) -> float:
    """Generic real cosine spherical-harmonic basis primitive."""
    lat = float(latitude_rad)
    phase = float(phase_rad)
    if not math.isfinite(lat) or not math.isfinite(phase):
        raise ValueError("angles must be finite")
    return associated_legendre(degree, order, math.sin(lat)) * cosine_harmonic(order, phase)


def real_spherical_basis_sin(
    degree: int,
    order: int,
    latitude_rad: float,
    phase_rad: float,
) -> float:
    """Generic real sine spherical-harmonic basis primitive."""
    lat = float(latitude_rad)
    phase = float(phase_rad)
    if not math.isfinite(lat) or not math.isfinite(phase):
        raise ValueError("angles must be finite")
    return associated_legendre(degree, order, math.sin(lat)) * sine_harmonic(order, phase)
