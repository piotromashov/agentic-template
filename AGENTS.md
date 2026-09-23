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
- **[`ORCHESTRATOR.md`](ORCHESTRATOR.md)** — only if you are the coordinator of an
  orchestrated run (Orca): the playbook for plan → review → gate → execute.
- **`openspec/specs/`** — the source of truth for *what the system does and
  why* (requirements). When specs and the docs above disagree, the spec wins.

No implementation without an approved OpenSpec change. See `agents/AGENTS.md`.
