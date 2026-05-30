# Event file format

An event file is a YAML (or JSON) document with up to four top-level keys:
`event`, `venue`, `stage` (optional), and `exits` (optional). All lengths are
in **metres**.

```yaml
event:
  name: "Summer Festival 2026"   # required
  type: concert                  # free-text label (default: general)
  crowd_profile: standing        # key under standards.occupancy.area_per_person_m2
  expected_attendance: 1500      # optional; omit to derive from usable area

venue:
  width_m: 60                    # required, east-west extent
  depth_m: 45                    # required, north-south extent

stage:                           # optional
  width_m: 16
  depth_m: 8
  position: [22, 37]             # optional [x, y] of bottom-left corner;
                                 # omitted -> centred against the north edge

exits:                           # optional; omitted -> auto-placed
  - { side: south, offset_m: 15, width_m: 3.0, label: "MAIN" }
  - { side: west,  offset_m: 22, width_m: 1.65 }
```

## Fields

### `event`
| Field | Required | Notes |
|-------|----------|-------|
| `name` | yes | Used in the report and output filename. |
| `type` | no | Free-text (`concert`, `conference`, …). |
| `crowd_profile` | no | One of the keys in `standards.occupancy.area_per_person_m2` (`standing`, `standing_dense`, `seated_loose`, `seated_dense`, `exhibition`, …). Defaults to the standards' `default_profile`. |
| `expected_attendance` | no | Declared headcount. If omitted, occupancy is derived from usable area ÷ area-per-person. If declared above area capacity, the `OCC-CAPACITY` finding fails. |

### `venue`
`width_m` × `depth_m` rectangle. The venue origin (0, 0) is the south-west
corner; +x runs east, +y runs north.

### `stage` (optional)
Rectangle placed inside the venue. `position` is the bottom-left corner; if
omitted, the stage is centred against the north (far) edge. A crowd barrier is
drawn automatically in front of it using the standards' setback.

### `exits` (optional)
Each exit sits on one `side` (`north`/`south`/`east`/`west`), at `offset_m`
measured from the venue origin along that side, with an optional `width_m`
(defaults to the per-exit width needed to meet the egress requirement) and
`label`. **If you omit `exits` entirely**, the analyzer auto-places enough
exits of adequate width to satisfy the egress requirement, spreading them
across the audience-facing sides.

## Running

```bash
python -m generator examples/summer_festival.yaml          # report + DXF
python -m generator examples/summer_festival.yaml --json   # machine-readable
python -m generator examples/summer_festival.yaml --no-dxf # analysis only
python -m generator examples/summer_festival.yaml -o output/plan.dxf
python -m generator examples/summer_festival.yaml -s standards/israel.yaml
```

The process exits `0` when compliant and `1` when not, so it can gate scripts.
