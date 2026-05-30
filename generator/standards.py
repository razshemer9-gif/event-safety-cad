"""Loader and typed accessor for the safety-standards data file.

The standards file (see ``standards/israel.yaml``) is intentionally data-driven
so the numbers can be reviewed and updated without touching code. This module
gives the rest of the package a small, typed surface over that raw data.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import yaml

DEFAULT_STANDARDS = Path(__file__).resolve().parent.parent / "standards" / "israel.yaml"


class Standards:
    """Typed convenience wrapper around the raw standards mapping."""

    def __init__(self, data: dict[str, Any]):
        self.data = data

    # -- generic access ---------------------------------------------------- #
    def section(self, name: str) -> dict[str, Any]:
        try:
            return self.data[name]
        except KeyError as exc:  # pragma: no cover - defensive
            raise KeyError(f"standards file missing section '{name}'") from exc

    @property
    def meta(self) -> dict[str, Any]:
        return self.data.get("meta", {})

    # -- occupancy --------------------------------------------------------- #
    def area_per_person(self, profile: str | None) -> float:
        occ = self.section("occupancy")
        table = occ["area_per_person_m2"]
        key = profile or occ.get("default_profile", "standing")
        if key not in table:
            raise KeyError(
                f"unknown crowd profile '{key}'. "
                f"Known profiles: {', '.join(sorted(table))}"
            )
        return float(table[key])

    def occupancy_from_area(self, usable_area_m2: float, profile: str | None) -> int:
        return int(usable_area_m2 // self.area_per_person(profile))

    # -- egress ------------------------------------------------------------ #
    def required_exit_count(self, occupants: int) -> int:
        for tier in self.section("egress")["min_exits_by_occupancy"]:
            cap = tier["max_occupants"]
            if cap is None or occupants <= cap:
                return int(tier["exits"])
        return int(self.section("egress")["min_exits_by_occupancy"][-1]["exits"])

    def required_exit_width_total(self, occupants: int) -> float:
        """Total clear exit width (m) required for the occupant load, snapped up
        to the exit-unit module and clamped to the per-exit minimum."""
        eg = self.section("egress")
        raw = occupants * float(eg["width_per_occupant_m"])
        unit = float(eg["unit_width_m"])
        snapped = math.ceil(raw / unit) * unit if raw > 0 else 0.0
        floor = float(eg["min_exit_clear_width_m"])
        return max(snapped, floor)

    @property
    def min_exit_clear_width(self) -> float:
        return float(self.section("egress")["min_exit_clear_width_m"])

    @property
    def min_main_exit_width(self) -> float:
        return float(self.section("egress")["min_main_exit_width_m"])

    @property
    def max_travel_distance(self) -> float:
        return float(self.section("egress")["max_travel_distance_m"])

    # -- medical ----------------------------------------------------------- #
    def first_aid_stations(self, occupants: int) -> int:
        med = self.section("medical")
        per = med["first_aid_station_per_occupants"]
        return max(med["min_first_aid_stations"], math.ceil(occupants / per))

    def ambulances(self, occupants: int) -> int:
        med = self.section("medical")
        if occupants < med["ambulance_required_at_occupants"]:
            return 0
        return max(1, math.ceil(occupants / med["ambulance_per_occupants"]))

    # -- fire -------------------------------------------------------------- #
    def extinguishers(self, area_m2: float) -> int:
        fire = self.section("fire")
        by_area = math.ceil(area_m2 / fire["extinguisher_per_area_m2"])
        return max(fire["min_extinguishers"], by_area)

    # -- sanitation -------------------------------------------------------- #
    def toilets(self, occupants: int) -> int:
        san = self.section("sanitation")
        return max(san["min_toilets"], math.ceil(occupants / san["toilets_per_occupants"]))


def load_standards(path: str | Path | None = None) -> Standards:
    """Load the standards file (defaults to the bundled Israeli standards)."""
    path = Path(path) if path else DEFAULT_STANDARDS
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a mapping at the top level")
    return Standards(data)
