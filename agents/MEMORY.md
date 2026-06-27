# MEMORY.md — PROJECT_NAME facts & decisions

> Durable *facts and decisions* for this repo: operational/infra facts, a
> decision log, and project state. The **rules** live in [`AGENTS.md`](AGENTS.md);
> the **requirements** (what the system does and why) live in `openspec/specs/`.
> Don't duplicate either here — this file is the log, not the law or the spec.
>
> Keep entries dated. Convert relative dates to absolute. Append; don't rewrite
> history.

---

## Project state

- **Status:** greenfield. OpenSpec initialized; no application code yet.
- **Source of truth for requirements:** `openspec/specs/` (currently empty —
  fills as changes are proposed and archived).

---

## Decision log

Newest first. One entry per decision: date, what was decided, why.

- **2026-06-27 — Template baseline: the `intent-driven` OpenSpec framework.**
  This repo ships configured for the `intent-driven` schema
  (`openspec/config.yaml`): artifact chain **proposal → specs → design → adr →
  tasks**, with a skill bound per artifact (proposal→grill-me,
  specs→gherkin-authoring, design→c4-diagrams, adr→architectural-decision-records).
  Skills live in `.claude/skills/`, subagents in `.claude/agents/`; the `opsx:*`
  commands cover propose/explore/new/continue/apply/verify/sync/archive plus
  `bulk-apply`. Git-discipline gates ("cross `main` between phases") live in
  `AGENTS.md` and the `openspec-git-discipline` skill. Repo-level ADRs persist in
  the top-level `adr/` folder (immutable, supersession-linked). Replace this
  entry's specifics with real decisions as your project evolves.
- **2026-06-27 — Agent docs centralized under `agents/`.** `AGENTS.md` (rules)
  and `MEMORY.md` (this file) live in `agents/`; root `CLAUDE.md` is a thin
  pointer. Requirements deliberately kept out of these files — they belong in
  `openspec/specs/` to avoid a second, drifting source of truth.

---

## Operational / infra facts

<!-- FILL IN as they appear. Examples to add later:
- Deploy targets and how to deploy
- Environment variable NAMES (never values)
- CI/CD pipeline notes
- Non-obvious gotchas discovered while building -->

_None yet — greenfield._

---

## Maintenance

- After completing a significant task, append the decision or operational fact
  here (dated). Track: stack decisions, env var names, deploy/infra changes,
  gotchas. Don't record requirements (those go in specs) or restate rules
  (those go in `AGENTS.md`).
