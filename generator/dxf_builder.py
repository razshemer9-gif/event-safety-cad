"""Render an analyzed event plan to a DXF CAD drawing using ezdxf.

The drawing is organised into named layers so it can be toggled/styled in any
CAD application:

    VENUE        venue boundary
    STAGE        stage footprint
    BARRIER      front-of-stage crowd barrier
    EXITS        exit openings, direction arrows and labels
    MEDICAL      first-aid stations
    FIRE         fire extinguishers
    ANNOTATION   title block, legend, compliance summary
"""

from __future__ import annotations

from pathlib import Path

import ezdxf
from ezdxf.enums import TextEntityAlignment

from .models import EventPlan, SafetyReport, Side

# layer name -> ACI colour index
_LAYERS = {
    "VENUE": 7,        # white/black
    "STAGE": 8,        # grey
    "BARRIER": 1,      # red
    "EXITS": 3,        # green
    "MEDICAL": 5,      # blue
    "FIRE": 1,         # red
    "ANNOTATION": 7,
}

_EXIT_MARK = 1.5       # size of the exit opening mark / arrow (m)
_SYMBOL_R = 0.6        # radius of medical / fire symbols (m)


def _setup_layers(doc) -> None:
    for name, color in _LAYERS.items():
        if name not in doc.layers:
            doc.layers.add(name, color=color)


def _exit_point(plan: EventPlan, side: Side, offset: float) -> tuple[float, float]:
    """Centre point of an exit on the venue perimeter (venue origin at 0,0)."""
    w, d = plan.venue.width_m, plan.venue.depth_m
    if side == Side.SOUTH:
        return (offset, 0.0)
    if side == Side.NORTH:
        return (offset, d)
    if side == Side.WEST:
        return (0.0, offset)
    return (w, offset)  # EAST


def _outward(side: Side) -> tuple[float, float]:
    return {
        Side.SOUTH: (0.0, -1.0),
        Side.NORTH: (0.0, 1.0),
        Side.WEST: (-1.0, 0.0),
        Side.EAST: (1.0, 0.0),
    }[side]


def _along(side: Side) -> tuple[float, float]:
    """Unit vector running ALONG the wall the exit sits on."""
    return {
        Side.SOUTH: (1.0, 0.0),
        Side.NORTH: (1.0, 0.0),
        Side.WEST: (0.0, 1.0),
        Side.EAST: (0.0, 1.0),
    }[side]


def _draw_venue(msp, plan: EventPlan) -> None:
    w, d = plan.venue.width_m, plan.venue.depth_m
    msp.add_lwpolyline(
        [(0, 0), (w, 0), (w, d), (0, d)],
        close=True,
        dxfattribs={"layer": "VENUE"},
    )


def _draw_stage(msp, plan: EventPlan) -> tuple[float, float, float, float] | None:
    if not plan.stage:
        return None
    s = plan.stage
    if s.position is not None:
        x, y = s.position
    else:  # centre against the north (far) edge
        x = (plan.venue.width_m - s.width_m) / 2
        y = plan.venue.depth_m - s.depth_m
    msp.add_lwpolyline(
        [(x, y), (x + s.width_m, y), (x + s.width_m, y + s.depth_m), (x, y + s.depth_m)],
        close=True,
        dxfattribs={"layer": "STAGE"},
    )
    msp.add_text(
        "STAGE", height=1.0, dxfattribs={"layer": "STAGE"}
    ).set_placement(
        (x + s.width_m / 2, y + s.depth_m / 2), align=TextEntityAlignment.MIDDLE_CENTER
    )
    return (x, y, s.width_m, s.depth_m)


def _draw_barrier(msp, plan: EventPlan, stage_box, std_setback: float) -> None:
    """Crowd barrier line parallel to the front (audience side) of the stage."""
    if stage_box is None:
        return
    x, y, sw, sd = stage_box
    by = y - std_setback
    if by <= 0:
        return
    msp.add_line(
        (x - 1.0, by), (x + sw + 1.0, by), dxfattribs={"layer": "BARRIER"}
    )
    msp.add_text(
        "CROWD BARRIER", height=0.7, dxfattribs={"layer": "BARRIER"}
    ).set_placement((x + sw / 2, by - 1.0), align=TextEntityAlignment.MIDDLE_CENTER)


def _draw_exit(msp, plan: EventPlan, exit_) -> None:
    cx, cy = _exit_point(plan, exit_.side, exit_.offset_m)
    ax, ay = _along(exit_.side)
    ox, oy = _outward(exit_.side)
    half = exit_.width_m / 2

    # Opening: a thick green segment across the wall.
    p1 = (cx - ax * half, cy - ay * half)
    p2 = (cx + ax * half, cy + ay * half)
    msp.add_line(p1, p2, dxfattribs={"layer": "EXITS", "lineweight": 50})

    # Direction arrow pointing outward.
    tip = (cx + ox * _EXIT_MARK, cy + oy * _EXIT_MARK)
    msp.add_line((cx, cy), tip, dxfattribs={"layer": "EXITS"})
    # simple arrowhead
    msp.add_line(tip, (tip[0] - ox * 0.5 - ax * 0.4, tip[1] - oy * 0.5 - ay * 0.4),
                 dxfattribs={"layer": "EXITS"})
    msp.add_line(tip, (tip[0] - ox * 0.5 + ax * 0.4, tip[1] - oy * 0.5 + ay * 0.4),
                 dxfattribs={"layer": "EXITS"})

    label = f"{exit_.label} ({exit_.width_m:.2f}m)"
    lx, ly = cx + ox * (_EXIT_MARK + 1.2), cy + oy * (_EXIT_MARK + 1.2)
    msp.add_text(label, height=0.7, dxfattribs={"layer": "EXITS"}).set_placement(
        (lx, ly), align=TextEntityAlignment.MIDDLE_CENTER
    )


def _draw_symbol(msp, x: float, y: float, layer: str, glyph: str) -> None:
    msp.add_circle((x, y), _SYMBOL_R, dxfattribs={"layer": layer})
    msp.add_text(glyph, height=0.8, dxfattribs={"layer": layer}).set_placement(
        (x, y), align=TextEntityAlignment.MIDDLE_CENTER
    )


def _scatter(plan: EventPlan, n: int, margin: float) -> list[tuple[float, float]]:
    """Spread n points along the inner perimeter of the venue (clockwise)."""
    if n <= 0:
        return []
    w, d = plan.venue.width_m, plan.venue.depth_m
    perim = [
        (margin, margin), (w - margin, margin),
        (w - margin, d - margin), (margin, d - margin),
    ]
    # interpolate along the rectangle perimeter
    edges = [(perim[i], perim[(i + 1) % 4]) for i in range(4)]
    lengths = [((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5 for a, b in edges]
    total = sum(lengths)
    pts = []
    for k in range(n):
        t = (total * (k + 0.5) / n)
        for (a, b), L in zip(edges, lengths):
            if t <= L or L == 0:
                f = (t / L) if L else 0
                pts.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
                break
            t -= L
    return pts


def _draw_annotation(msp, plan: EventPlan, report: SafetyReport) -> None:
    """Title and compliance summary placed below the venue."""
    y = -6.0
    line_h = 1.4
    status = "COMPLIANT" if report.compliant else "NON-COMPLIANT — REVIEW"
    lines = [
        f"EVENT SAFETY PLAN — {report.event_name}",
        f"Status: {status}",
        f"Venue: {plan.venue.width_m:.1f} x {plan.venue.depth_m:.1f} m  "
        f"(usable {report.usable_area_m2:.0f} m2)",
        f"Design occupancy: {report.design_occupancy}  ({report.occupancy_basis})",
        f"Exits: {report.provided_exits} provided / {report.required_exits} required, "
        f"width {report.provided_exit_width_total_m:.2f}/{report.required_exit_width_total_m:.2f} m",
        f"First aid: {report.first_aid_stations}   Ambulances: {report.ambulances}   "
        f"Extinguishers: {report.extinguishers}   Toilets: {report.toilets}",
        "NOTE: model output — verify against current Israeli regulations & safety consultant.",
    ]
    msp.add_text(lines[0], height=1.6, dxfattribs={"layer": "ANNOTATION"}).set_placement(
        (0, y), align=TextEntityAlignment.LEFT
    )
    for i, text in enumerate(lines[1:], start=1):
        msp.add_text(text, height=0.9, dxfattribs={"layer": "ANNOTATION"}).set_placement(
            (0, y - i * line_h), align=TextEntityAlignment.LEFT
        )


def build_dxf(plan: EventPlan, report: SafetyReport, out_path: str | Path,
              std_setback: float = 1.5) -> Path:
    """Build the DXF drawing and write it to `out_path`. Returns the path."""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    doc = ezdxf.new("R2010", setup=True)
    doc.units = ezdxf.units.M
    _setup_layers(doc)
    msp = doc.modelspace()

    _draw_venue(msp, plan)
    stage_box = _draw_stage(msp, plan)
    _draw_barrier(msp, plan, stage_box, std_setback)

    for ex in report.placed_exits:
        _draw_exit(msp, plan, ex)

    for x, y in _scatter(plan, report.first_aid_stations, margin=3.0):
        _draw_symbol(msp, x, y, "MEDICAL", "+")
    for x, y in _scatter(plan, report.extinguishers, margin=1.5):
        _draw_symbol(msp, x, y, "FIRE", "F")

    _draw_annotation(msp, plan, report)

    doc.saveas(out_path)
    return out_path
