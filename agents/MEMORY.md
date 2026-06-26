# MEMORY.md — smartcrate facts & decisions

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

- **2026-06-26 — Adopted OpenSpec for spec-driven development.** Spec-first
  workflow (`/opsx:propose` → review → `/opsx:apply` → `/opsx:archive`); specs
  checked into the repo as the source of truth. Initialized with
  `openspec init --tools claude,cursor`.
- **2026-06-26 — Agent docs centralized under `agents/`.** `AGENTS.md` (rules)
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
