"""Input and output data models for an event safety plan.

Input models describe what the planner gives us (the venue, the event, any
fixed elements). Output models describe what the analysis produces (the safety
report). All lengths are in metres, areas in square metres.
"""

from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field, model_validator


class Side(str, Enum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"


# --------------------------------------------------------------------------- #
# Input models
# --------------------------------------------------------------------------- #
class Stage(BaseModel):
    """A performance stage placed inside the venue.

    `position` is the (x, y) of the stage's bottom-left corner relative to the
    venue's bottom-left corner. If omitted the stage is centred against the
    north (far) edge.
    """

    width_m: float = Field(gt=0)
    depth_m: float = Field(gt=0)
    position: Optional[tuple[float, float]] = None


class ExitSpec(BaseModel):
    """An explicitly placed exit. `offset_m` is measured along the given side
    from the venue's origin corner to the centre of the exit."""

    side: Side
    offset_m: float = Field(ge=0)
    width_m: Optional[float] = Field(default=None, gt=0)
    label: Optional[str] = None


class Venue(BaseModel):
    width_m: float = Field(gt=0, description="East-west extent")
    depth_m: float = Field(gt=0, description="North-south extent")

    @property
    def area_m2(self) -> float:
        return self.width_m * self.depth_m


class Event(BaseModel):
    name: str
    type: str = "general"
    # References a key under standards.occupancy.area_per_person_m2
    crowd_profile: Optional[str] = None
    # Explicit headcount; if absent it is derived from usable area.
    expected_attendance: Optional[int] = Field(default=None, ge=0)


class EventPlan(BaseModel):
    """Top-level input document (parsed from an event YAML/JSON file)."""

    event: Event
    venue: Venue
    stage: Optional[Stage] = None
    exits: list[ExitSpec] = Field(default_factory=list)

    @model_validator(mode="after")
    def _check_stage_fits(self) -> "EventPlan":
        if self.stage and self.stage.position is not None:
            x, y = self.stage.position
            if x < 0 or y < 0:
                raise ValueError("stage.position must be non-negative")
            if x + self.stage.width_m > self.venue.width_m + 1e-6:
                raise ValueError("stage exceeds venue width")
            if y + self.stage.depth_m > self.venue.depth_m + 1e-6:
                raise ValueError("stage exceeds venue depth")
        return self


def load_event(path: str | Path) -> EventPlan:
    """Load and validate an event plan from a YAML or JSON file."""
    path = Path(path)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a mapping at the top level")
    return EventPlan.model_validate(data)


# --------------------------------------------------------------------------- #
# Output models
# --------------------------------------------------------------------------- #
class PlacedExit(BaseModel):
    """A resolved exit with concrete geometry, ready to draw."""

    side: Side
    offset_m: float
    width_m: float
    label: str


class Finding(BaseModel):
    """A single compliance check result."""

    code: str
    ok: bool
    message: str


class SafetyReport(BaseModel):
    """Computed life-safety requirements and compliance findings."""

    event_name: str
    venue_area_m2: float
    usable_area_m2: float

    design_occupancy: int
    occupancy_basis: str            # "declared" or "area-derived"

    required_exits: int
    required_exit_width_total_m: float
    provided_exits: int
    provided_exit_width_total_m: float
    placed_exits: list[PlacedExit]

    first_aid_stations: int
    ambulances: int
    extinguishers: int
    toilets: int

    findings: list[Finding]

    @property
    def compliant(self) -> bool:
        return all(f.ok for f in self.findings)
