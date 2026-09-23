# AGENTS.md — PROJECT_NAME operating manual

> The rules for AI agents (Claude Code, Cursor, Codex, OpenCode) working in
> this repo: *how we work*, conventions, and safety. Keep it **lean**. This file does **not**
> restate *what the system does* — that lives in `openspec/specs/` (the source
> of truth). When the two disagree, the spec wins; fix this file.
>
> Companion: [`MEMORY.md`](MEMORY.md) holds durable *facts and decisions*
> (operational/infra facts, decision log, project state). Rules here; facts there.

---

## What PROJECT_NAME is

<!-- FILL IN: one or two sentences. What does PROJECT_NAME do, for whom?
     e.g. "PROJECT_NAME is a CLI that ... " or "a web app that ..." -->
_TODO — one-paragraph description._

**Status:** greenfield. No code yet. Stack: _TODO (language, framework, runtime)._

---

## How we work here: spec-driven development with OpenSpec

This project is built **spec-first**. We agree on *what* to build before we
write code. The unit of work is a **change**, not a commit.

We use the **`intent-driven`** OpenSpec schema (`openspec/config.yaml`), whose
artifact chain is **proposal → specs → design → adr → tasks**. Each artifact has
a bound skill (via `config.yaml` `rules`, surfaced in `openspec instructions`):

| Artifact | Bound skill | What it adds |
| --- | --- | --- |
| `proposal` | `grill-me` | interrogate the plan, one question per decision branch, before specs |
| `specs` | `gherkin-authoring` | GIVEN/WHEN/THEN scenarios inside the `### Requirement:` / `#### Scenario:` wrapper |
| `design` | `c4-diagrams` | C4 (context/container/component) diagrams in ASCII or Mermaid |
| `adr` | `architectural-decision-records` | durable decisions recorded in top-level `adr/` (immutable, supersession-linked) |

The loop (run these in your IDE as slash commands):

1. **`/opsx:new "<id>"`** or **`/opsx:propose "<idea>"`** — scaffold a change
   under `openspec/changes/<id>/` and generate artifacts through the chain above.
   **No code yet.** Use **`/opsx:explore`** first to investigate.
2. **Review the intent.** Read the proposal, specs, design, and ADRs. Refine
   until right. This is where misalignment gets caught cheaply. Step through
   artifacts incrementally with **`/opsx:continue`**.
3. **`/opsx:apply`** — implement the tasks against the approved change.
   **`/opsx:verify`** checks the implementation matches the artifacts before
   archive. **`/opsx:bulk-apply`** applies multiple changes in parallel worktrees.
4. **`/opsx:archive`** — merge the spec deltas into `openspec/specs/` and move
   the change into `openspec/changes/archive/`. (Repo-level ADRs in `adr/` are
   **not** archived — they persist.)

Supporting command: **`/opsx:sync`** (reconcile specs with reality). The
**`adversarial-authoring`** skill (model-council review via the
`adversarial-author`/`adversarial-reviewer` subagents) can harden any artifact.

CLI for checking state (terminal, any time):

```bash
openspec list              # active changes
openspec list --specs      # current capabilities
openspec show <id>         # read a change
openspec validate --all    # check specs/changes for structural issues
```

---

## Conventions

<!-- FILL IN as the codebase grows. Examples to replace:
- Language/formatter (e.g. Prettier, Black, gofmt) and how to run it
- Naming, module boundaries, directory structure
- Error-handling and logging patterns
- Test layout and minimum coverage expectations -->

- Keep this section short and concrete; prefer a linter/formatter config over
  prose rules where possible.

---

## Build / run / test

<!-- FILL IN once the stack is chosen. Agents should be able to verify work
     end-to-end from these commands. Keep them current. -->

```bash
# install:   TODO
# run:       TODO
# test:      TODO
# lint:      TODO
```

**Verification discipline:** a task in a change's `tasks.md` is only "done"
when it's been run/tested, not just written. If you can't verify a behavior
end-to-end, say so.

---

## Git workflow

- Default branch: `main`.
- **Commit specs and code together.** OpenSpec is built on specs being checked
  in alongside the code they describe.
- Why-focused commit messages. One coherent change per commit.
- **No co-author trailers.** Never add `Co-Authored-By:` (Claude or anyone
  else) or "Generated with" lines to commits or PR descriptions.
- Don't commit secrets. Keep `.gitignore` current.

### Git discipline (the gates)

Every OpenSpec state change must **cross `main` before the next lifecycle phase
depends on it.** Full detail lives in the `openspec-git-discipline` skill; the
gates in brief:

- **Propose/continue** may be drafted on a branch, but the proposal must be
  **committed and merged to `main` before `apply` starts.**
- **Apply** may run from `main`, a branch, or a worktree **only if that exact
  proposal is already on `main`.** Before apply: `git status --short`, confirm no
  uncommitted proposal files, confirm the proposal reached `main`.
- **Archive** runs **only from `main`, after implementation is merged back.**
- **Never auto-commit, branch, or merge** without explicit user approval. After
  propose and after archive, *ask* the user to commit; offer a PR branch.

---

## Safety rules (hard stops)

1. **No implementation without an approved change.** If asked to build
   something with no change folder, create the proposal first
   (`/opsx:propose`) and get it reviewed. Don't jump to code.
2. **Never edit live specs directly.** Requirements in
   `openspec/specs/<capability>/spec.md` change only via deltas in a change
   folder, then `/opsx:archive`. Editing them by hand breaks the audit trail.
3. **One change folder per coherent unit of work.** Keep changes focused.
4. **Validate before applying and before archiving** (`openspec validate`).
   Archive when done so specs stay current and the changes dir stays clean.
5. **Don't hand-edit OpenSpec-*generated* files under `.claude/`/`.cursor/`.**
   The `opsx:*` commands and `openspec-*-change` skills are generated; regenerate
   with `openspec update`. **Exception:** the intent-driven framework files are
   intentional, hand-maintained additions and are *not* OpenSpec-generated — the
   skills `grill-me`, `c4-diagrams`, `architectural-decision-records`,
   `gherkin-authoring`, `openspec-git-discipline`, `adversarial-authoring`; the
   agents `adversarial-author`/`adversarial-reviewer`; the `opsx:bulk-apply`
   command. `openspec update` leaves these alone — they are not drift.
6. **Never commit secrets** (`.env`, keys, tokens). If `git status` shows one,
   stop and fix `.gitignore` before committing anything else.
7. **No force-push to `main`.** Rewrite only commits you haven't pushed.
8. **Report tool/verification failures honestly.** A task marked done that
   wasn't run end-to-end is worse than an unfinished one.

---

## Maintenance

- After a meaningful change (new convention, stack decision, command change,
  safety rule), propose the exact edit to this file or to `MEMORY.md` and apply
  it in the same change. Keep both lean.
