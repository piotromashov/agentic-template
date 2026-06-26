# AGENTS.md — smartcrate operating manual

> The rules for AI agents (Claude Code, Cursor) working in this repo: *how we
> work*, conventions, and safety. Keep it **lean**. This file does **not**
> restate *what the system does* — that lives in `openspec/specs/` (the source
> of truth). When the two disagree, the spec wins; fix this file.
>
> Companion: [`MEMORY.md`](MEMORY.md) holds durable *facts and decisions*
> (operational/infra facts, decision log, project state). Rules here; facts there.

---

## What smartcrate is

<!-- FILL IN: one or two sentences. What does smartcrate do, for whom?
     e.g. "smartcrate is a CLI that ... " or "a web app that ..." -->
_TODO — one-paragraph description._

**Status:** greenfield. No code yet. Stack: _TODO (language, framework, runtime)._

---

## How we work here: spec-driven development with OpenSpec

This project is built **spec-first**. We agree on *what* to build before we
write code. The unit of work is a **change**, not a commit.

The loop (run these in your IDE as slash commands):

1. **`/opsx:propose "<idea>"`** — generates a change folder under
   `openspec/changes/<id>/` with `proposal.md` (why + what), `specs/` (the
   requirement deltas), `design.md` (technical decisions), `tasks.md`
   (implementation checklist). **No code yet.**
2. **Review the intent.** Read the proposal and spec deltas. Refine until the
   requirements are right. This is where misalignment gets caught cheaply.
3. **`/opsx:apply`** — implement the tasks against the approved change.
4. **`/opsx:archive`** — merge the spec deltas into `openspec/specs/` and move
   the change into `openspec/changes/archive/`.

Supporting commands: `/opsx:explore` (investigate before proposing),
`/opsx:sync` (reconcile specs with reality).

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

- Default branch: `main`. (Run `git init` — the repo isn't versioned yet.)
- **Commit specs and code together.** OpenSpec is built on specs being checked
  in alongside the code they describe.
- Why-focused commit messages. One coherent change per commit.
- Don't commit secrets. Add a `.gitignore` before the first commit.

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
5. **Don't hand-edit `.claude/` or `.cursor/`.** Those are OpenSpec-generated
   slash commands and skills; regenerate with `openspec update`.
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
