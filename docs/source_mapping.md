# Source Mapping

> Traceability map linking every structured field used by the system back to its
> origin file and verification status. This is the audit index that ties
> [`regulatory_database.md`](regulatory_database.md) (authoritative requirements)
> and [`project_patterns.md`](project_patterns.md) (examples only) to their
> sources.

## Legend

| Status | Meaning |
|---|---|
| 🟥 Source document required for verification | Value exists in a standards file but has no authoritative, paginated source; cannot be verified. |
| 🟦 Project Example Only | Value comes from a reference project/example; never a regulation. |
| ⬜ Missing | Expected input not found in the repository. |

## Directory map

| Path | Role per task | Exists? | Notes |
|---|---|---|---|
| `standards/` | Authoritative source of requirements | ✅ | Contains only `israel.yaml` (a self-declared baseline model). |
| `standards/israel.yaml` | Standards data | ✅ | Unpaginated, non-authoritative. 🟥 |
| `reference_projects/` | Examples only | ⬜ | **Missing.** Substituted by `examples/`. |
| `examples/` | Reference projects (actual location) | ✅ | Contains `summer_festival.yaml`. 🟦 |

---

## Field → source mapping (standards)

Every field below originates from `standards/israel.yaml`. None has a verifiable
page number, so all carry status 🟥.

| Structured field name | Source file | In-file locator | Page number | Status |
|---|---|---|---|---|
| `meta.jurisdiction` | `standards/israel.yaml` | L18 | n/a (metadata) | 🟥 |
| `meta.name` | `standards/israel.yaml` | L19 | n/a (metadata) | 🟥 |
| `meta.version` | `standards/israel.yaml` | L20 | n/a (metadata) | 🟥 |
| `meta.units` | `standards/israel.yaml` | L21 | n/a (metadata) | 🟥 |
| `meta.disclaimer` | `standards/israel.yaml` | L22–24 | n/a (metadata) | 🟥 |
| `occupancy.area_per_person_m2.standing_dense` | `standards/israel.yaml` | L34 | Source document required for verification | 🟥 |
| `occupancy.area_per_person_m2.standing` | `standards/israel.yaml` | L35 | Source document required for verification | 🟥 |
| `occupancy.area_per_person_m2.seated_loose` | `standards/israel.yaml` | L36 | Source document required for verification | 🟥 |
| `occupancy.area_per_person_m2.seated_dense` | `standards/israel.yaml` | L37 | Source document required for verification | 🟥 |
| `occupancy.area_per_person_m2.assembly_concentrated` | `standards/israel.yaml` | L38 | Source document required for verification | 🟥 |
| `occupancy.area_per_person_m2.exhibition` | `standards/israel.yaml` | L39 | Source document required for verification | 🟥 |
| `occupancy.default_profile` | `standards/israel.yaml` | L40 | Source document required for verification | 🟥 |
| `egress.width_per_occupant_m` | `standards/israel.yaml` | L48 | Source document required for verification | 🟥 |
| `egress.unit_width_m` | `standards/israel.yaml` | L49 | Source document required for verification | 🟥 |
| `egress.min_exit_clear_width_m` | `standards/israel.yaml` | L50 | Source document required for verification | 🟥 |
| `egress.min_main_exit_width_m` | `standards/israel.yaml` | L51 | Source document required for verification | 🟥 |
| `egress.min_exits_by_occupancy[0..4]` | `standards/israel.yaml` | L56–60 | Source document required for verification | 🟥 |
| `egress.max_travel_distance_m` | `standards/israel.yaml` | L62 | Source document required for verification | 🟥 |
| `egress.min_aisle_width_m` | `standards/israel.yaml` | L63 | Source document required for verification | 🟥 |
| `medical.first_aid_station_per_occupants` | `standards/israel.yaml` | L70 | Source document required for verification | 🟥 |
| `medical.min_first_aid_stations` | `standards/israel.yaml` | L71 | Source document required for verification | 🟥 |
| `medical.ambulance_required_at_occupants` | `standards/israel.yaml` | L73 | Source document required for verification | 🟥 |
| `medical.ambulance_per_occupants` | `standards/israel.yaml` | L74 | Source document required for verification | 🟥 |
| `fire.extinguisher_max_spacing_m` | `standards/israel.yaml` | L80 | Source document required for verification | 🟥 |
| `fire.extinguisher_per_area_m2` | `standards/israel.yaml` | L81 | Source document required for verification | 🟥 |
| `fire.min_extinguishers` | `standards/israel.yaml` | L82 | Source document required for verification | 🟥 |
| `sanitation.toilets_per_occupants` | `standards/israel.yaml` | L88 | Source document required for verification | 🟥 |
| `sanitation.min_toilets` | `standards/israel.yaml` | L89 | Source document required for verification | 🟥 |
| `stage.front_barrier_setback_m` | `standards/israel.yaml` | L95 | Source document required for verification | 🟥 |
| `stage.side_clearance_m` | `standards/israel.yaml` | L96 | Source document required for verification | 🟥 |

---

## Field → source mapping (reference projects / examples)

These are configuration values from an example, **not** requirements. Status 🟦.

| Field (as configured) | Source file | In-file locator | Status |
|---|---|---|---|
| `event.type = concert` | `examples/summer_festival.yaml` | L6 | 🟦 Project Example Only |
| `event.crowd_profile = standing` | `examples/summer_festival.yaml` | L7 | 🟦 Project Example Only |
| `event.expected_attendance = 1500` | `examples/summer_festival.yaml` | L8 | 🟦 Project Example Only |
| `venue.width_m = 60` | `examples/summer_festival.yaml` | L11 | 🟦 Project Example Only |
| `venue.depth_m = 45` | `examples/summer_festival.yaml` | L12 | 🟦 Project Example Only |
| `stage.width_m = 16` | `examples/summer_festival.yaml` | L15 | 🟦 Project Example Only |
| `stage.depth_m = 8` | `examples/summer_festival.yaml` | L16 | 🟦 Project Example Only |
| Commented exit suggestions | `examples/summer_festival.yaml` | L21–25 | 🟦 Project Example Only |

---

## Named authorities without a document

`standards/israel.yaml` (L10–11) names the following authorities but **no
corresponding source document exists** in the repository. Until provided, no page
number can be cited:

| Named authority | Document present? | Status |
|---|---|---|
| חוק רישוי עסקים (Business Licensing Law) | No | 🟥 Source document required for verification |
| תקנות הבטיחות באירועים תחת כיפת השמיים | No | 🟥 Source document required for verification |
| Fire-service "מבחני אש" guidance | No | 🟥 Source document required for verification |

---

## Summary

- **Standards fields mapped:** 30 (incl. 5 metadata) → all from `standards/israel.yaml`.
- **Verifiable against a paginated authoritative document:** 0.
- **Example fields mapped:** 8 → all from `examples/summer_festival.yaml`, all 🟦.
- **Missing inputs:** `reference_projects/` directory; all three named source documents.

### To reach a verified state
1. Add the actual regulation documents under `standards/` (e.g. PDFs of the named
   laws/regulations).
2. For each 🟥 row, replace *"Source document required for verification"* with the
   real source file name and page number.
3. (Optional) Create `reference_projects/` and relocate example files, then
   regenerate `project_patterns.md`.
