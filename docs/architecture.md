# Architecture

`event-safety-cad` turns a small, human-readable description of an event into
(1) a deterministic **safety report** and (2) a **DXF CAD drawing** of the
proposed layout, checked against a data-driven set of Israeli safety standards.

## Pipeline

```
 event.yaml ──load_event──▶ EventPlan ─┐
                                       ├─ analyze() ─▶ SafetyReport ─▶ build_dxf() ─▶ plan.dxf
 standards/israel.yaml ─load_standards─┘                         └─▶ printed/JSON report
```

| Stage        | Module                  | Responsibility |
|--------------|-------------------------|----------------|
| Parse input  | `generator/models.py`   | Validate the event/venue/stage/exits (pydantic). |
| Load rules   | `generator/standards.py`| Typed accessor over `standards/israel.yaml`. |
| Analyse      | `generator/analysis.py` | Occupancy, egress, medical, fire, sanitation + findings. |
| Draw         | `generator/dxf_builder.py` | Render layered DXF via `ezdxf`. |
| Orchestrate  | `generator/cli.py`      | CLI, report printing, exit codes. |

## Design principles

- **Standards as data.** All regulatory numbers live in `standards/israel.yaml`,
  not in code, so a safety reviewer can audit and tune them without touching
  Python. Swap in a different jurisdiction by passing `--standards`.
- **Deterministic core, AI on top.** `analyze()` is pure and auditable — it is
  the source of truth for the numbers. The "AI" layer envisioned in the README
  (natural-language layout proposals, explanations) is intended to sit *above*
  this core and feed it structured `EventPlan`s, never to bypass it.
- **CAD-friendly output.** Geometry is organised into named layers
  (`VENUE`, `STAGE`, `BARRIER`, `EXITS`, `MEDICAL`, `FIRE`, `ANNOTATION`)
  so it drops cleanly into AutoCAD / QCAD / LibreCAD.
- **Fail loud.** The CLI exits non-zero when a plan is non-compliant, so it can
  gate a CI check or an approval script.

## ⚠️ Regulatory disclaimer

The values in `standards/israel.yaml` are a **baseline model** of common
Israeli event-safety practice, not a verified copy of the current regulations.
Every value carries a `ref` to reconcile against the authoritative source.
Output is decision support for a licensed safety consultant (יועץ בטיחות) — not
a substitute for one.

## Roadmap (next steps)

- Travel-distance & aisle checks computed from real geometry (currently
  reported as standards but not yet spatially verified).
- PDF/PNG export for non-CAD stakeholders.
- AI layout assistant that proposes stage/exit positions from a brief.
- Additional jurisdictions under `standards/`.
