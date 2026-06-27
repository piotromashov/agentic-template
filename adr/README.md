# Architecture Decision Records (ADRs)

Durable architectural decisions for PROJECT_NAME. These persist **across** OpenSpec
changes — unlike a change's `openspec/changes/<id>/adr.md` manifest, which is just
the per-change review marker. The `adr` step of the intent-driven workflow writes
records here.

## Conventions

- **Filename:** `NNNN-kebab-title.md`, where `NNNN` is a 4-digit sequence one
  greater than the highest existing number (monotonic across the whole repo,
  never reused). Example: `0001-use-sqlite-for-local-store.md`.
- **Immutable once accepted.** Never edit an accepted ADR — not its status, body,
  or date. To revisit a decision, write a **new** ADR whose `Status` is
  `accepted, supersedes ADR-NNNN` and whose `Supersedes:` field names the prior
  one. The old file stays frozen as history.
- **What's "in force":** walk the `Supersedes:` links. An ADR is in force if it's
  accepted and no later ADR supersedes it. Only in-force ADRs constrain new
  designs; superseded ones are historical context.
- **Bar for an ADR:** a long-term architectural commitment (pattern, technology,
  boundary, contract) that affects future changes — not a tactical implementation
  detail. If nothing meets the bar in a change, record none.
- **Format:** title, `Status`, `Date`, optional `Supersedes`, then MADR-short
  sections: Context, Decision, Consequences. See the
  `architectural-decision-records` skill (`.claude/skills/`) for templates.
