# Project Patterns

> **What this file is.** A catalogue of layout/configuration patterns observed in
> **reference projects (examples only)**. Per the project rules, everything here
> is labelled **"Project Example Only"** and is **NOT a regulatory requirement**.
> Project examples are **never** converted into regulations. For requirements,
> see [`regulatory_database.md`](regulatory_database.md).

## Directory reality check

| Expected by task | Found in repository | Action taken |
|---|---|---|
| `/reference_projects` | **Does not exist** | Used the existing `examples/` directory as the reference-projects location. |
| Reference project files | `examples/summer_festival.yaml` (1 file) | Patterns below are drawn from this single example. |

> If a dedicated `/reference_projects` directory is intended, create it and move
> example event files there; this document can then be regenerated to cover them.

---

## Pattern catalogue

### Source: `examples/summer_festival.yaml`

An open-air standing concert example (L1–25).

| Pattern field (as configured) | Observed value | In-file locator | Classification |
|---|---|---|---|
| `event.type` | `concert` | L6 | **Project Example Only** |
| `event.crowd_profile` | `standing` | L7 | **Project Example Only** |
| `event.expected_attendance` | `1500` | L8 | **Project Example Only** |
| `venue.width_m` × `venue.depth_m` | `60 × 45` m | L11–12 | **Project Example Only** |
| `stage.width_m` × `stage.depth_m` | `16 × 8` m | L15–16 | **Project Example Only** |
| Stage placement | position omitted → centred against north edge | L17 | **Project Example Only** |
| Exit strategy | `exits` omitted → auto-placed by the generator | L19 | **Project Example Only** |

### Commented-out (illustrative) exit layout

The example also shows, **in comments only** (L21–25), a suggested explicit exit
layout. These are *suggestions inside an example*, not requirements:

| Suggested exit (commented) | Value | In-file locator | Classification |
|---|---|---|---|
| Main exit, south | `offset_m: 15, width_m: 3.0, label: "MAIN"` | L22 | **Project Example Only** |
| Second exit, south | `offset_m: 45, width_m: 3.0` | L23 | **Project Example Only** |
| Side exit, west | `offset_m: 22, width_m: 1.65` | L24 | **Project Example Only** |
| Side exit, east | `offset_m: 22, width_m: 1.65` | L25 | **Project Example Only** |

---

## Observations (non-binding)

These are descriptive notes about how the example is *modelled*. They carry **no
regulatory force** and must not be cited as requirements:

- The example chooses the `standing` occupancy profile, which maps to the
  `occupancy.area_per_person_m2.standing` parameter in the standards model.
  *(Whether that parameter itself is valid is unverified — see the regulatory
  database.)*
- The example relies on the generator's **auto-exit placement** rather than
  declaring exits, demonstrating the default path.
- The commented exit widths (`3.0`, `1.65` m) happen to be ≥ the model's main-exit
  minimum, but this is an authoring choice in an example, **not** evidence of a
  rule.

---

## Rules applied

1. ✅ No value in this file was promoted to a regulation.
2. ✅ Every observed pattern is marked **"Project Example Only"**.
3. ✅ No requirements were invented from these examples.
4. ✅ Where the expected `/reference_projects` directory was missing, the
   substitution (`examples/`) is documented above rather than silently assumed.
