"""Command-line interface for event-safety-cad.

Usage:
    python -m generator <event.yaml> [options]
    event-safety-cad <event.yaml> [options]    # if installed

Reads an event plan, runs the safety analysis, prints a report, and (unless
--no-dxf) writes a DXF drawing to the output directory.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .analysis import analyze
from .dxf_builder import build_dxf
from .models import load_event
from .standards import load_standards


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="event-safety-cad",
        description="Generate an event safety plan and DXF from an event file.",
    )
    p.add_argument("event", type=Path, help="path to the event YAML/JSON file")
    p.add_argument(
        "-s", "--standards", type=Path, default=None,
        help="path to a standards file (default: bundled Israeli standards)",
    )
    p.add_argument(
        "-o", "--output", type=Path, default=None,
        help="output DXF path (default: output/<event-name>.dxf)",
    )
    p.add_argument("--no-dxf", action="store_true", help="run analysis only, skip DXF")
    p.add_argument("--json", action="store_true", help="print the report as JSON")
    return p


def _slugify(name: str) -> str:
    keep = [c.lower() if c.isalnum() else "-" for c in name.strip()]
    slug = "".join(keep)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-") or "event"


def _print_report(report) -> None:
    print(f"\n=== Event Safety Report: {report.event_name} ===")
    print(f"Venue area        : {report.venue_area_m2:.0f} m² "
          f"(usable {report.usable_area_m2:.0f} m²)")
    print(f"Design occupancy  : {report.design_occupancy} ({report.occupancy_basis})")
    print(f"Exits             : {report.provided_exits}/{report.required_exits} "
          f"  width {report.provided_exit_width_total_m:.2f}/"
          f"{report.required_exit_width_total_m:.2f} m")
    print(f"First-aid stations: {report.first_aid_stations}")
    print(f"Ambulances        : {report.ambulances}")
    print(f"Extinguishers     : {report.extinguishers}")
    print(f"Toilets           : {report.toilets}")
    print("\nFindings:")
    for f in report.findings:
        mark = "PASS" if f.ok else "FAIL"
        print(f"  [{mark}] {f.code}: {f.message}")
    verdict = "COMPLIANT" if report.compliant else "NON-COMPLIANT"
    print(f"\nOverall: {verdict}")


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    try:
        plan = load_event(args.event)
    except Exception as exc:  # noqa: BLE001 - surface a friendly message
        print(f"error: failed to load event '{args.event}': {exc}", file=sys.stderr)
        return 2

    std = load_standards(args.standards)
    report = analyze(plan, std)

    if args.json:
        print(report.model_dump_json(indent=2))
    else:
        _print_report(report)

    if not args.no_dxf:
        out = args.output or (Path("output") / f"{_slugify(report.event_name)}.dxf")
        path = build_dxf(plan, report, out)
        if not args.json:
            print(f"\nDXF written to: {path}")

    # Non-zero exit if the plan is non-compliant, so CI / scripts can gate on it.
    return 0 if report.compliant else 1


if __name__ == "__main__":
    raise SystemExit(main())
