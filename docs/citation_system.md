# Citation System

This project reads regulatory requirements **directly from the source PDF files
in [`/standards`](../standards)**. There is **no YAML/derived regulatory
database** — the previous `standards/israel.yaml` has been deleted and must not
be reintroduced as a source of requirements.

## Hard rules

1. A requirement may exist **only** if it can be cited to a source PDF in
   `/standards`.
2. Every citation record MUST contain all four fields:
   - **`source_pdf_filename`** — the exact PDF in `/standards`.
   - **`page_number`** — the page within that PDF.
   - **`quoted_requirement`** — the verbatim text (no paraphrasing).
   - **`extracted_structured_value`** — the value parsed from the quote.
3. If the page number is unavailable, the `page_number` field is set to the
   exact string: **`Source document required for verification`**.
4. **No** value may come from memory, assumptions, industry defaults, or the
   deleted YAML database. Absent a PDF citation, the requirement does not exist
   and is reported as **`Source document required for verification`**.

## Files

| File | Role |
|---|---|
| `citations/citation_schema.json` | JSON Schema defining a valid citation record. |
| `citations/requirements.json` | The citation ledger — one entry per cited requirement. |
| `docs/regulatory_database.md` | Human-readable view rendered from the ledger. |
| `docs/source_mapping.md` | Audit map of PDFs → citations → verification status. |

## A citation record

```json
{
  "id": "EGRESS-EXIT-COUNT-01",
  "source_pdf_filename": "<file>.pdf",
  "page_number": 12,
  "quoted_requirement": "<verbatim text copied from the PDF>",
  "extracted_structured_value": { "max_occupants": 1000, "exits": 3 },
  "structured_field_name": "egress.min_exits_by_occupancy",
  "verified": true
}
```

`verified` is `true` **only** when the PDF exists in `/standards`, the page
number is a real integer, and the quote is present.

## Workflow to add a requirement

1. Drop the authoritative regulation **PDF** into `/standards`.
2. Locate the requirement; copy its **verbatim** text and note the **page**.
3. Add a citation record to `citations/requirements.json` (validate against
   `citations/citation_schema.json`).
4. Re-render `docs/regulatory_database.md` and re-run the event analysis.

## Current state

> **No PDF source documents are present in `/standards`.**
> `citations/requirements.json` therefore contains **zero** citations. Every
> requirement currently resolves to **`Source document required for
> verification`**. This is the correct, honest state given the available inputs —
> not a gap to be filled with assumed values.
