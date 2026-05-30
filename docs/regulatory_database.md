# Regulatory Database

> **Scope & integrity notice.** This database is built **only** from authoritative
> *standards* files under [`/standards`](../standards). Reference projects are
> **never** used as a source of requirements (see
> [`project_patterns.md`](project_patterns.md)).
>
> **Verification status of this database: UNVERIFIED.**
> The sole standards file present, `standards/israel.yaml`, is a self-declared
> *baseline model* (see its lines 8–14 and 22–24), **not** an authoritative
> regulation document. It contains **no page numbers** and references no source
> document. Therefore, under the project rules, the page-number and authority
> fields for every requirement below are recorded as:
> **"Source document required for verification."**
> The values are reproduced verbatim for traceability; they must **not** be
> treated as confirmed regulatory requirements until reconciled against the
> official Israeli source documents.

## Source inventory

| Source file | Type | Page numbers present? | Authoritative? | Status |
|-------------|------|-----------------------|----------------|--------|
| `standards/israel.yaml` | Machine-readable parameter model | No | No (self-declared baseline) | Source document required for verification |

Cited authorities **named inside** `standards/israel.yaml` (lines 10–11), for which
no document is present in the repository:

- חוק רישוי עסקים (Business Licensing Law) — *document not provided*
- תקנות הבטיחות באירועים תחת כיפת השמיים (open-air event safety regulations) — *document not provided*
- Fire-service "מבחני אש" guidance — *document not provided*

> Because none of these source documents exist in the repository, no page number
> can be cited for any requirement. Each entry is marked accordingly.

---

## How to read each requirement

Every requirement records the four required fields:

- **Structured field name** — the YAML path used by the generator.
- **Requirement text** — the value and its in-file description, verbatim.
- **Source file** — the file the value was read from.
- **Page number** — recorded as *"Source document required for verification"*
  because the source file is unpaginated and non-authoritative.

An additional **In-file locator** (line number) is provided for traceability
within `standards/israel.yaml`; it is a locator, **not** a regulatory page number.

---

## 1. Occupancy load

| Structured field name | Requirement text (verbatim) | Source file | In-file locator | Page number |
|---|---|---|---|---|
| `occupancy.area_per_person_m2.standing_dense` | 0.25 m² per person — "tight standing crowd (front-of-stage)" | `standards/israel.yaml` | L34 | Source document required for verification |
| `occupancy.area_per_person_m2.standing` | 0.50 m² per person — "general standing audience" | `standards/israel.yaml` | L35 | Source document required for verification |
| `occupancy.area_per_person_m2.seated_loose` | 0.65 m² per person — "seated rows with circulation" | `standards/israel.yaml` | L36 | Source document required for verification |
| `occupancy.area_per_person_m2.seated_dense` | 0.45 m² per person — "close-packed seating" | `standards/israel.yaml` | L37 | Source document required for verification |
| `occupancy.area_per_person_m2.assembly_concentrated` | 0.65 m² per person | `standards/israel.yaml` | L38 | Source document required for verification |
| `occupancy.area_per_person_m2.exhibition` | 1.5 m² per person — "booths / exhibition floor" | `standards/israel.yaml` | L39 | Source document required for verification |
| `occupancy.default_profile` | "standing" — default crowd profile when none is given | `standards/israel.yaml` | L40 | Source document required for verification |

## 2. Egress / exits

| Structured field name | Requirement text (verbatim) | Source file | In-file locator | Page number |
|---|---|---|---|---|
| `egress.width_per_occupant_m` | 0.0077 m of exit width per occupant ("≈ 0.77 m per 100 people") | `standards/israel.yaml` | L48 | Source document required for verification |
| `egress.unit_width_m` | 0.55 m — one "exit unit" (lane) module | `standards/israel.yaml` | L49 | Source document required for verification |
| `egress.min_exit_clear_width_m` | 1.10 m — minimum clear width of any single exit | `standards/israel.yaml` | L50 | Source document required for verification |
| `egress.min_main_exit_width_m` | 1.65 m — minimum clear width of the main exit | `standards/israel.yaml` | L51 | Source document required for verification |
| `egress.min_exits_by_occupancy[0]` | ≤ 50 occupants → 1 exit | `standards/israel.yaml` | L56 | Source document required for verification |
| `egress.min_exits_by_occupancy[1]` | ≤ 500 occupants → 2 exits | `standards/israel.yaml` | L57 | Source document required for verification |
| `egress.min_exits_by_occupancy[2]` | ≤ 1000 occupants → 3 exits | `standards/israel.yaml` | L58 | Source document required for verification |
| `egress.min_exits_by_occupancy[3]` | ≤ 2000 occupants → 4 exits | `standards/israel.yaml` | L59 | Source document required for verification |
| `egress.min_exits_by_occupancy[4]` | > 2000 occupants (no upper bound) → 6 exits | `standards/israel.yaml` | L60 | Source document required for verification |
| `egress.max_travel_distance_m` | 45 m — max distance from any point to an exit | `standards/israel.yaml` | L62 | Source document required for verification |
| `egress.min_aisle_width_m` | 1.20 m — minimum clear aisle within the crowd area | `standards/israel.yaml` | L63 | Source document required for verification |

## 3. Medical / first aid

| Structured field name | Requirement text (verbatim) | Source file | In-file locator | Page number |
|---|---|---|---|---|
| `medical.first_aid_station_per_occupants` | 1 first-aid station per 1000 occupants | `standards/israel.yaml` | L70 | Source document required for verification |
| `medical.min_first_aid_stations` | At least 1 first-aid station | `standards/israel.yaml` | L71 | Source document required for verification |
| `medical.ambulance_required_at_occupants` | On-site ambulance required at/above 500 occupants | `standards/israel.yaml` | L73 | Source document required for verification |
| `medical.ambulance_per_occupants` | 1 ambulance per 5000 occupants | `standards/israel.yaml` | L74 | Source document required for verification |

## 4. Fire safety equipment

| Structured field name | Requirement text (verbatim) | Source file | In-file locator | Page number |
|---|---|---|---|---|
| `fire.extinguisher_max_spacing_m` | 15 m — max travel distance to an extinguisher | `standards/israel.yaml` | L80 | Source document required for verification |
| `fire.extinguisher_per_area_m2` | At least one extinguisher per 200 m² of floor area | `standards/israel.yaml` | L81 | Source document required for verification |
| `fire.min_extinguishers` | At least 2 extinguishers | `standards/israel.yaml` | L82 | Source document required for verification |

## 5. Sanitation

| Structured field name | Requirement text (verbatim) | Source file | In-file locator | Page number |
|---|---|---|---|---|
| `sanitation.toilets_per_occupants` | 1 toilet per 100 occupants | `standards/israel.yaml` | L88 | Source document required for verification |
| `sanitation.min_toilets` | At least 2 toilets | `standards/israel.yaml` | L89 | Source document required for verification |

## 6. Stage / barrier setbacks

| Structured field name | Requirement text (verbatim) | Source file | In-file locator | Page number |
|---|---|---|---|---|
| `stage.front_barrier_setback_m` | 1.5 m — gap between stage edge and crowd barrier | `standards/israel.yaml` | L95 | Source document required for verification |
| `stage.side_clearance_m` | 1.0 m — side clearance | `standards/israel.yaml` | L96 | Source document required for verification |

---

## Metadata (from `standards/israel.yaml` `meta:` block, L17–24)

| Structured field name | Value | Source file | In-file locator |
|---|---|---|---|
| `meta.jurisdiction` | "IL" | `standards/israel.yaml` | L18 |
| `meta.name` | "Israel — Event Safety (baseline model)" | `standards/israel.yaml` | L19 |
| `meta.version` | "0.1.0" | `standards/israel.yaml` | L20 |
| `meta.units` | "metric" (metres / m²) | `standards/israel.yaml` | L21 |
| `meta.disclaimer` | "Illustrative baseline values. Reconcile against current Israeli regulations and a licensed safety consultant before operational use." | `standards/israel.yaml` | L22–24 |

---

## Summary

- **27 parameter requirements** were extracted from `standards/israel.yaml`.
- **0 of 27** can currently be verified against an authoritative, paginated
  source document.
- **All 27** are therefore marked **"Source document required for verification"**
  for the page-number / authority field.
- **No requirements were invented**, and **no reference-project values were
  promoted** into this database.

To make this database authoritative, add the actual source documents (e.g. the
named laws/regulations) under `/standards`, then replace each
*"Source document required for verification"* entry with the real source file
and page number.
