# AGENTS.md — PROJECT_NAME

> **Pointer file** for agent harnesses that read a root `AGENTS.md` (Codex,
> OpenCode, and others). Claude Code reads [`CLAUDE.md`](CLAUDE.md), which
> points to the same place. The operating manual lives in
> [`agents/`](agents/). Read it before doing any work in this repo.

- **[`agents/AGENTS.md`](agents/AGENTS.md)** — the rules: how we work
  (spec-driven development with OpenSpec), conventions, build/run/test, git
  workflow, and safety rules. **Start here.**
- **[`agents/MEMORY.md`](agents/MEMORY.md)** — durable facts and decisions:
  operational/infra facts, decision log, project state.
- **[`agents/ORCHESTRATOR.md`](agents/ORCHESTRATOR.md)** — the coordinator's
  playbook for an orchestrated run in Orca (plan → review → gate → execute).
  **When the user tells you to act as the coordinator** (or to coordinate or
  orchestrate a piece of work), read this file in full first and follow it
  end to end, without being asked to read it. Otherwise ignore it.
- **`openspec/specs/`** — the source of truth for *what the system does and
  why* (requirements). When specs and the docs above disagree, the spec wins.

No implementation without an approved OpenSpec change. See `agents/AGENTS.md`.
