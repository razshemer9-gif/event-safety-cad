# event-safety-cad

AI-powered Event Safety Planning and DXF Generation according to Israeli regulations.

Given a short description of an event (venue size, stage, expected crowd), this
tool computes the life-safety requirements — occupancy, exits, first-aid, fire
provision — against a data-driven model of Israeli event-safety standards, and
renders a layered **DXF** site plan you can open in any CAD application.

> ⚠️ **Disclaimer.** The standards values shipped here are a *baseline model* of
> common Israeli practice, **not** a verified copy of the current regulations.
> Output is decision support for a licensed safety consultant (יועץ בטיחות), not
> a substitute for one. See [`standards/israel.yaml`](standards/israel.yaml).

## Quick start

```bash
# 1. install dependencies
pip install -r requirements.txt        # or: pip install -e .

# 2. generate a plan from the bundled example
python -m generator examples/summer_festival.yaml
```

This prints a safety report and writes `output/summer-festival-2026.dxf`.

```
=== Event Safety Report: Summer Festival 2026 ===
Venue area        : 2700 m² (usable 2572 m²)
Design occupancy  : 1500 (declared)
Exits             : 4/4   width 11.55/11.55 m
First-aid stations: 2
...
Overall: COMPLIANT
```

## How it works

```
event.yaml  +  standards/israel.yaml  ─▶  analyze()  ─▶  report  +  DXF drawing
```

- **`standards/`** — machine-readable safety parameters (occupancy, egress,
  medical, fire). Edit the YAML to tune rules without touching code.
- **`generator/`** — the Python package: input models, standards loader,
  deterministic analysis engine, and the `ezdxf` drawing builder.
- **`examples/`** — sample event files.
- **`output/`** — generated DXF artifacts (git-ignored).
- **`docs/`** — [architecture](docs/architecture.md) and the
  [event file format](docs/event-file-format.md).

## Repository layout

```
event-safety-cad/
├── standards/israel.yaml        # the safety rules (data, not code)
├── generator/                   # models, standards, analysis, dxf_builder, cli
├── examples/summer_festival.yaml
├── output/                      # generated .dxf (ignored)
├── docs/
└── tests/
```

## Usage

```bash
python -m generator <event.yaml> [options]

  -s, --standards PATH   use a different standards file
  -o, --output PATH      output DXF path (default: output/<event-name>.dxf)
      --no-dxf           run the analysis only
      --json             print the report as JSON
```

The CLI exits `0` when the plan is compliant and `1` when not, so it can gate a
CI check or approval script.

## Development

```bash
pip install -e ".[dev]"
pytest
```

## Roadmap

- Spatial travel-distance & aisle-width verification from real geometry.
- PDF/PNG export for non-CAD stakeholders.
- AI layout assistant that proposes stage/exit positions from a brief.
- Additional jurisdictions under `standards/`.
