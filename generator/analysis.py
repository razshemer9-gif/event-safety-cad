"""Safety analysis: turn an :class:`EventPlan` plus :class:`Standards` into a
:class:`SafetyReport`.

This is the deterministic, rules-based core. (The "AI" layer envisioned in the
README is expected to sit *on top* of this — e.g. proposing layouts or
explaining findings in natural language — while this module remains the
auditable source of truth for the numbers.)
"""

from __future__ import annotations

from .models import EventPlan, Finding, PlacedExit, SafetyReport, Side
from .standards import Standards


def _usable_area(plan: EventPlan) -> float:
    """Venue area minus the footprint of the stage (crowd cannot stand on it)."""
    area = plan.venue.area_m2
    if plan.stage:
        area -= plan.stage.width_m * plan.stage.depth_m
    return max(area, 0.0)


def _auto_place_exits(plan: EventPlan, count: int, width: float) -> list[PlacedExit]:
    """Distribute `count` exits around the venue perimeter, avoiding the stage
    side. Exits are spread evenly along each chosen side.

    Placement order favours the audience-facing sides: south first, then the
    east/west sides, then north (typically the stage side) only if needed.
    """
    w, d = plan.venue.width_m, plan.venue.depth_m
    sides_in_order = [
        (Side.SOUTH, w),
        (Side.WEST, d),
        (Side.EAST, d),
        (Side.NORTH, w),
    ]

    # How many exits per side: round-robin so they spread out.
    per_side: dict[Side, int] = {s: 0 for s, _ in sides_in_order}
    i = 0
    while sum(per_side.values()) < count:
        side = sides_in_order[i % len(sides_in_order)][0]
        per_side[side] += 1
        i += 1

    placed: list[PlacedExit] = []
    n = 0
    for side, length in sides_in_order:
        k = per_side[side]
        if k == 0:
            continue
        # Even spacing: centres at length*(j+1)/(k+1)
        for j in range(k):
            offset = length * (j + 1) / (k + 1)
            n += 1
            placed.append(
                PlacedExit(
                    side=side,
                    offset_m=round(offset, 3),
                    width_m=width,
                    label=f"E{n}",
                )
            )
    return placed


def _resolve_exits(plan: EventPlan, required_exits: int, unit_width: float,
                   std: Standards) -> list[PlacedExit]:
    """Use the planner's explicit exits if given; otherwise auto-place enough to
    satisfy the requirement."""
    if plan.exits:
        placed = []
        for idx, ex in enumerate(plan.exits, start=1):
            placed.append(
                PlacedExit(
                    side=ex.side,
                    offset_m=ex.offset_m,
                    width_m=ex.width_m or max(unit_width, std.min_exit_clear_width),
                    label=ex.label or f"E{idx}",
                )
            )
        return placed
    width = max(unit_width, std.min_exit_clear_width)
    return _auto_place_exits(plan, required_exits, round(width, 3))


def analyze(plan: EventPlan, std: Standards) -> SafetyReport:
    """Compute the full safety report for an event plan."""
    profile = plan.event.crowd_profile
    usable = _usable_area(plan)

    # --- occupancy ---------------------------------------------------------
    area_capacity = std.occupancy_from_area(usable, profile)
    if plan.event.expected_attendance is not None:
        design_occ = plan.event.expected_attendance
        basis = "declared"
    else:
        design_occ = area_capacity
        basis = "area-derived"

    # --- egress requirements ----------------------------------------------
    required_exits = std.required_exit_count(design_occ)
    required_width = std.required_exit_width_total(design_occ)
    # Width distributed across the required number of exits (>= per-exit min).
    per_exit_width = max(required_width / max(required_exits, 1), std.min_exit_clear_width)

    placed = _resolve_exits(plan, required_exits, per_exit_width, std)
    provided_width = sum(e.width_m for e in placed)

    # --- ancillary provision ----------------------------------------------
    first_aid = std.first_aid_stations(design_occ)
    ambulances = std.ambulances(design_occ)
    extinguishers = std.extinguishers(plan.venue.area_m2)
    toilets = std.toilets(design_occ)

    # --- findings ----------------------------------------------------------
    findings: list[Finding] = []

    findings.append(Finding(
        code="OCC-CAPACITY",
        ok=design_occ <= area_capacity or basis == "area-derived",
        message=(
            f"Design occupancy {design_occ} vs area capacity {area_capacity} "
            f"({usable:.0f} m² @ {std.area_per_person(profile):.2f} m²/person)."
            + ("" if design_occ <= area_capacity
               else " Declared attendance EXCEEDS area capacity.")
        ),
    ))

    findings.append(Finding(
        code="EGRESS-COUNT",
        ok=len(placed) >= required_exits,
        message=f"Exits provided {len(placed)} / required {required_exits}.",
    ))

    findings.append(Finding(
        code="EGRESS-WIDTH",
        ok=provided_width + 1e-6 >= required_width,
        message=(
            f"Total exit width {provided_width:.2f} m / "
            f"required {required_width:.2f} m."
        ),
    ))

    narrow = [e.label for e in placed if e.width_m + 1e-6 < std.min_exit_clear_width]
    findings.append(Finding(
        code="EGRESS-MIN-WIDTH",
        ok=not narrow,
        message=(
            f"All exits meet the {std.min_exit_clear_width:.2f} m minimum clear width."
            if not narrow else
            f"Exits below minimum clear width: {', '.join(narrow)}."
        ),
    ))

    has_main = any(e.width_m + 1e-6 >= std.min_main_exit_width for e in placed)
    findings.append(Finding(
        code="EGRESS-MAIN",
        ok=has_main,
        message=(
            f"At least one main exit ≥ {std.min_main_exit_width:.2f} m present."
            if has_main else
            f"No exit reaches the {std.min_main_exit_width:.2f} m main-exit minimum."
        ),
    ))

    return SafetyReport(
        event_name=plan.event.name,
        venue_area_m2=round(plan.venue.area_m2, 2),
        usable_area_m2=round(usable, 2),
        design_occupancy=design_occ,
        occupancy_basis=basis,
        required_exits=required_exits,
        required_exit_width_total_m=round(required_width, 2),
        provided_exits=len(placed),
        provided_exit_width_total_m=round(provided_width, 2),
        placed_exits=placed,
        first_aid_stations=first_aid,
        ambulances=ambulances,
        extinguishers=extinguishers,
        toilets=toilets,
        findings=findings,
    )
