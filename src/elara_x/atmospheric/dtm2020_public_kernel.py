"""Independent public-specification DTM2020 kernel skeleton for Elara X.

This module is Elara X-authored and intentionally contains no CNES/SWAMI source,
translated source, fitted DTM2020 coefficients, or reconstructed restricted
parameter tables.

It implements only public/generic state preparation:
- UTC/location validation;
- longitude normalisation and local solar time;
- day-of-year and annual phase;
- raw operational F10.7/Kp driver state;
- SI output contracts;
- licence-isolated resource readiness.

It MUST NOT claim authoritative DTM2020 numerical output until a later controlled
phase adds an independently authored numerical kernel, an authorised external
parameter resource is activated, and oracle equivalence is accepted.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
import math
from pathlib import Path

from .dtm2020_external_resource import (
    DTM2020ResourceMetadata,
    DTM2020ResourceStatus,
    resolve_dtm2020_external_resource,
)

DTM2020_PUBLIC_KERNEL_MARKER = "ELARA_X_ATMO_M16_8R_DTM2020_PUBLIC_KERNEL_v1"

PUBLIC_SPEC_LABEL = "DTM2020-compatible public-specification kernel framework"
ACCEPTED_NUMERICAL_LABEL = "DTM2020 operational-compatible native implementation"

PARTIAL_SPECIES = ("H", "He", "O", "N2", "O2")
PUBLIC_HOSTED_ALTITUDE_RANGE_KM = (120.0, 1500.0)


class DTM2020KernelStatus(str, Enum):
    PUBLIC_SPEC_READY = "PUBLIC_SPEC_READY"
    RESOURCE_REQUIRED = "RESOURCE_REQUIRED"
    RESOURCE_AVAILABLE_KERNEL_NOT_ACTIVATED = "RESOURCE_AVAILABLE_KERNEL_NOT_ACTIVATED"


class DTM2020KernelError(RuntimeError):
    pass


class DTM2020ResourceRequiredError(DTM2020KernelError):
    pass


class DTM2020NumericalKernelNotActivatedError(DTM2020KernelError):
    pass


@dataclass(frozen=True)
class DTM2020OperationalDrivers:
    """Raw public operational drivers; no guessed internal normalisation."""

    f107_daily_sfu: float
    f107_81day_mean_sfu: float
    kp_3h_delayed: float
    kp_24h_mean: float


@dataclass(frozen=True)
class DTM2020Input:
    utc: datetime
    altitude_km: float
    latitude_deg: float
    longitude_deg: float
    drivers: DTM2020OperationalDrivers


@dataclass(frozen=True)
class DTM2020PreparedState:
    utc: datetime
    altitude_km: float
    latitude_deg: float
    longitude_deg: float
    local_solar_time_hours: float
    day_of_year: int
    annual_phase_rad: float
    drivers: DTM2020OperationalDrivers
    resource_status: str
    implementation_label: str


@dataclass(frozen=True)
class DTM2020Output:
    """SI-normalised future output contract.

    Fields are deliberately not populated by M16.8R.
    """

    total_mass_density_kg_m3: float
    temperature_K: float
    exospheric_temperature_K: float
    partial_mass_density_kg_m3: dict[str, float]


def _finite(value: float, name: str) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def normalise_longitude_deg(longitude_deg: float) -> float:
    value = _finite(longitude_deg, "longitude_deg")
    normalised = ((value + 180.0) % 360.0) - 180.0
    if normalised == -180.0 and value > 0.0:
        return 180.0
    return normalised


def ensure_utc(value: datetime) -> datetime:
    if not isinstance(value, datetime):
        raise TypeError("utc must be a datetime")
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("utc must be timezone-aware")
    return value.astimezone(timezone.utc)


def local_solar_time_hours(utc: datetime, longitude_deg: float) -> float:
    dt = ensure_utc(utc)
    lon = normalise_longitude_deg(longitude_deg)
    decimal_utc = (
        dt.hour
        + dt.minute / 60.0
        + dt.second / 3600.0
        + dt.microsecond / 3_600_000_000.0
    )
    return (decimal_utc + lon / 15.0) % 24.0


def day_of_year(utc: datetime) -> int:
    return ensure_utc(utc).timetuple().tm_yday


def annual_phase_rad(utc: datetime) -> float:
    """Generic periodic phase only; not a fitted DTM coefficient/basis value."""
    dt = ensure_utc(utc)
    days_in_year = 366 if (
        dt.year % 4 == 0 and (dt.year % 100 != 0 or dt.year % 400 == 0)
    ) else 365
    fractional_day = (
        dt.hour / 24.0
        + dt.minute / 1440.0
        + dt.second / 86400.0
        + dt.microsecond / 86_400_000_000.0
    )
    return 2.0 * math.pi * ((day_of_year(dt) - 1) + fractional_day) / days_in_year


def validate_drivers(drivers: DTM2020OperationalDrivers) -> DTM2020OperationalDrivers:
    f107 = _finite(drivers.f107_daily_sfu, "f107_daily_sfu")
    fbar = _finite(drivers.f107_81day_mean_sfu, "f107_81day_mean_sfu")
    kp3 = _finite(drivers.kp_3h_delayed, "kp_3h_delayed")
    kp24 = _finite(drivers.kp_24h_mean, "kp_24h_mean")

    if f107 <= 0.0 or fbar <= 0.0:
        raise ValueError("F10.7 values must be positive")
    for value, name in ((kp3, "kp_3h_delayed"), (kp24, "kp_24h_mean")):
        if value < 0.0 or value > 9.0:
            raise ValueError(f"{name} must be within [0, 9]")

    return DTM2020OperationalDrivers(f107, fbar, kp3, kp24)


def validate_input(model_input: DTM2020Input) -> DTM2020Input:
    utc = ensure_utc(model_input.utc)
    altitude = _finite(model_input.altitude_km, "altitude_km")
    latitude = _finite(model_input.latitude_deg, "latitude_deg")
    longitude = normalise_longitude_deg(model_input.longitude_deg)
    drivers = validate_drivers(model_input.drivers)

    lo, hi = PUBLIC_HOSTED_ALTITUDE_RANGE_KM
    if altitude < lo or altitude > hi:
        raise ValueError(f"altitude_km must be within public hosted range [{lo}, {hi}]")
    if latitude < -90.0 or latitude > 90.0:
        raise ValueError("latitude_deg must be within [-90, 90]")

    return DTM2020Input(
        utc=utc,
        altitude_km=altitude,
        latitude_deg=latitude,
        longitude_deg=longitude,
        drivers=drivers,
    )


def g_per_cm3_to_kg_per_m3(value: float) -> float:
    return _finite(value, "density_g_cm3") * 1000.0


class DTM2020PublicSpecKernel:
    """Non-authoritative public-specification kernel framework."""

    def __init__(
        self,
        *,
        project_root: str | Path,
        explicit_resource_path: str | Path | None = None,
        resource_env: dict[str, str] | None = None,
    ) -> None:
        self.project_root = Path(project_root).expanduser().resolve()
        self.explicit_resource_path = explicit_resource_path
        self.resource_env = resource_env

    def resource_metadata(self) -> DTM2020ResourceMetadata:
        return resolve_dtm2020_external_resource(
            project_root=self.project_root,
            explicit_path=self.explicit_resource_path,
            env=self.resource_env,
        )

    def status(self) -> DTM2020KernelStatus:
        meta = self.resource_metadata()
        if meta.status == DTM2020ResourceStatus.RESOURCE_REQUIRED.value:
            return DTM2020KernelStatus.RESOURCE_REQUIRED
        if meta.status == DTM2020ResourceStatus.AVAILABLE.value:
            return DTM2020KernelStatus.RESOURCE_AVAILABLE_KERNEL_NOT_ACTIVATED
        return DTM2020KernelStatus.RESOURCE_REQUIRED

    def prepare_state(self, model_input: DTM2020Input) -> DTM2020PreparedState:
        clean = validate_input(model_input)
        meta = self.resource_metadata()
        return DTM2020PreparedState(
            utc=clean.utc,
            altitude_km=clean.altitude_km,
            latitude_deg=clean.latitude_deg,
            longitude_deg=clean.longitude_deg,
            local_solar_time_hours=local_solar_time_hours(clean.utc, clean.longitude_deg),
            day_of_year=day_of_year(clean.utc),
            annual_phase_rad=annual_phase_rad(clean.utc),
            drivers=clean.drivers,
            resource_status=meta.status,
            implementation_label=PUBLIC_SPEC_LABEL,
        )

    def evaluate(self, model_input: DTM2020Input) -> DTM2020Output:
        """Refuse numerical output until later resource/parser/kernel/oracle phases."""
        _ = self.prepare_state(model_input)
        meta = self.resource_metadata()
        if meta.status != DTM2020ResourceStatus.AVAILABLE.value:
            raise DTM2020ResourceRequiredError(
                "DTM2020 numerical evaluation requires an authorised external parameter resource"
            )
        raise DTM2020NumericalKernelNotActivatedError(
            "M16.8R provides only the independent public-specification kernel framework; "
            "authoritative DTM2020 numerical evaluation is not activated"
        )
