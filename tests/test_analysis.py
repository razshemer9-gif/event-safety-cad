"""Tests for the deterministic safety-analysis core."""

from pathlib import Path

import pytest

from generator import analyze, build_dxf, load_standards
from generator.models import Event, EventPlan, ExitSpec, Side, Stage, Venue

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def std():
    return load_standards()


def _plan(**overrides) -> EventPlan:
    base = dict(
        event=Event(name="Test", crowd_profile="standing", expected_attendance=1000),
        venue=Venue(width_m=50, depth_m=40),
    )
    base.update(overrides)
    return EventPlan(**base)


def test_usable_area_excludes_stage(std):
    plan = _plan(stage=Stage(width_m=10, depth_m=5))
    report = analyze(plan, std)
    assert report.venue_area_m2 == pytest.approx(2000)
    assert report.usable_area_m2 == pytest.approx(2000 - 50)


def test_area_derived_occupancy(std):
    # No declared attendance -> derived from usable area / area-per-person.
    plan = _plan(event=Event(name="X", crowd_profile="standing"))
    report = analyze(plan, std)
    # 2000 m² @ 0.5 m²/person = 4000
    assert report.design_occupancy == 4000
    assert report.occupancy_basis == "area-derived"


def test_exit_count_scales_with_occupancy(std):
    assert std.required_exit_count(40) == 1
    assert std.required_exit_count(400) == 2
    assert std.required_exit_count(900) == 3
    assert std.required_exit_count(50000) == 6


def test_exit_width_snaps_to_unit_and_floor(std):
    # tiny crowd still gets at least the per-exit minimum clear width
    assert std.required_exit_width_total(10) == pytest.approx(std.min_exit_clear_width)
    # larger crowd snaps up to the 0.55 m unit module
    w = std.required_exit_width_total(1000)
    assert w >= 1000 * 0.0077
    assert round((w / 0.55) % 1, 6) == 0  # multiple of the unit width


def test_auto_placed_exits_satisfy_requirement(std):
    plan = _plan()  # 1000 occupants -> 3 exits required
    report = analyze(plan, std)
    assert report.provided_exits >= report.required_exits
    assert report.provided_exit_width_total_m + 1e-6 >= report.required_exit_width_total_m
    assert report.compliant


def test_explicit_narrow_exit_flagged(std):
    plan = _plan(exits=[
        ExitSpec(side=Side.SOUTH, offset_m=10, width_m=0.5),  # too narrow
    ])
    report = analyze(plan, std)
    codes = {f.code: f.ok for f in report.findings}
    assert codes["EGRESS-MIN-WIDTH"] is False
    assert not report.compliant


def test_build_dxf_writes_file(std, tmp_path):
    plan = _plan(stage=Stage(width_m=12, depth_m=6))
    report = analyze(plan, std)
    out = build_dxf(plan, report, tmp_path / "plan.dxf")
    assert out.exists()
    assert out.stat().st_size > 0


def test_example_event_loads_and_is_compliant(std):
    from generator import load_event
    plan = load_event(ROOT / "examples" / "summer_festival.yaml")
    report = analyze(plan, std)
    assert report.design_occupancy == 1500
    assert report.compliant
