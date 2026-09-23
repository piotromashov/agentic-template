# Examples

Four walkthroughs, from the simplest to the full pipeline. Each shows **what
you say**, **what the agent does**, and **what you check**. Agent replies and
file contents are illustrative: yours will differ in wording, not in shape.

| Example | Flow | Use it when |
|---|---|---|
| [1. Add a feature, spec-first](#1-add-a-feature-spec-first) | OpenSpec, one agent | You want a new behaviour and you're driving |
| [2. Hand off a chore to three agents](#2-hand-off-a-chore-to-three-agents) | Orchestration | The work is bigger or riskier than you want to babysit, and doesn't change behaviour |
| [3. Orchestrate a feature](#3-orchestrate-a-feature) | Orchestration + OpenSpec | A behaviour change that deserves a reviewed plan |
| [4. Plan and review without Orca](#4-plan-and-review-without-orca) | `plan` + `review-plan` by hand | You want the second opinion without the pipeline |

The running project in all four is a small greeting CLI, built from zero.

---

## 1. Add a feature, spec-first

**Tool:** Claude Code (or Codex, OpenCode, Cursor) opened in the repo.

### You say

> I want a small CLI that greets the user by name. Propose it.

### The agent grills you first

Before writing anything, the `grill-me` skill asks one question per open
decision. For example:

> 1. Which language and runtime? *(recommended: Node.js, since OpenSpec already needs it)*
> 2. What happens with no name? Error, or a default like "friend"?
> 3. Should names with accents and emoji print unchanged?
> 4. Is `--help` in scope?

Answer them. Anything you settle here becomes part of the spec, so nobody
guesses later.

### It writes a change

```
openspec/changes/add-greeting-cli/
├── proposal.md                  ← why, what changes, which capabilities
├── specs/greeting/spec.md       ← the behaviour, as scenarios
├── design.md                    ← how it's built, with a C4 diagram
├── adr.md                       ← which architecture decisions were reviewed or made
└── tasks.md                     ← the implementation checklist
```

The spec is the part to read closely. It looks like this:

```markdown
## ADDED Requirements

### Requirement: Greet by name
The CLI greets the person whose name it is given.

#### Scenario: A name is given
- GIVEN the CLI is installed
- WHEN the user runs `greet Ana`
- THEN it prints `Hello, Ana!`

#### Scenario: No name is given
- GIVEN the CLI is installed
- WHEN the user runs `greet` with no arguments
- THEN it prints `Hello, friend!`
```

If the change makes a lasting architectural choice (say, "Node.js, no
dependencies"), it also writes `adr/0001-….md`.

### You review the intent

Read `proposal.md` and the scenarios, not code. Ask for changes in plain words:

> Add a scenario: names with accents print unchanged.

When it's right, let the agent commit the proposal and merge it to `main`. The
agent asks before committing, because the rules require your OK. The proposal
has to be on `main` before anyone implements it.

### You say

> Apply it.

The agent works through `tasks.md`, ticking items as it goes, and runs the
tests. It stops and asks if something in the spec turns out to be impossible
instead of improvising.

### You review, merge, and say

> Archive it.

The scenarios move into `openspec/specs/greeting/spec.md`. From now on that
file describes what the CLI does, and the next change to greetings starts from
it.

---

## 2. Hand off a chore to three agents

**Tool:** [Orca](https://www.onorca.dev/), with Claude in the main tab and
Codex available. First time? Do the
[orchestration setup](how-it-works.md#orchestration-setup) once.

The ask here doesn't change what the CLI does, so no OpenSpec change is needed.

### You say, in Orca's main tab

> Read `agents/ORCHESTRATOR.md` and act as the coordinator for: set up CI that
> runs the tests on every pull request.

### The coordinator plans with you

It reads the repo first, then asks only what it couldn't find out:

> 1. GitHub Actions? *(recommended: yes, the repo is on GitHub)*
> 2. Which Node versions: only the current LTS, or LTS and the one before?
> 3. Should a red build block merging, or only warn?
> 4. May the executor commit on its own branch? *(push and merge stay with you)*

Then it writes the plan packet outside the repo:

```
~/repos/plans/2026-09-23-setup-ci/
├── ANALYSIS.md       ← what it found: test command, Node version, no CI yet
├── PLAN.md           ← the steps, each with how to verify it and how to undo it
├── MISSION.md        ← the prompt the executor will get, self-contained
└── REVIEW-BRIEF.md   ← where the plan is weakest, for the reviewer
```

`MISSION.md` ends with the block the coordinator uses to launch the executor:

```
## Ejecución (orquestador)
modelo: claude-sonnet-5
esfuerzo: medium
motivo: one workflow file, clear verification
alcance: .github/workflows/, package.json scripts
fuera de alcance: application code, branch protection settings
verificación: actionlint passes; every script the workflow calls exists and passes locally
reporte: /Users/ana/repos/plans/2026-09-23-setup-ci/EXECUTION.md
```

### Codex attacks the plan

The coordinator sends the packet to Codex with the `review-plan` skill, which
checks the claims read-only and writes `REVIEW.md`:

> **Verdict: REVISE.** One blocking finding.
>
> **BLOCKING — the verification can't fail.** "The workflow file exists and is
> valid YAML" passes even if the tests never run. *Failure scenario:* the
> workflow calls `npm run test:ci`, which doesn't exist; the check still
> passes, and CI is red on the first pull request. *Fix:* also run every
> script the workflow calls, locally.

The coordinator doesn't just accept everything. It answers each finding in
`PLAN.md`:

| # | Objection | Decision | Reason |
|---|---|---|---|
| 1 | Verification can't fail (BLOCKING) | accepted | Verification now runs every script the workflow calls |

### You approve at the gate

The coordinator shows you a short summary and waits:

> **setup-ci** with `claude-sonnet-5`. Risks: the first real CI run only
> happens when you push; branch protection is not set (out of scope).
> Rejected findings: none. Authorizations: commit on `exec-setup-ci`, no push.
> **aprobar / cambiar / cancelar?**

> aprobar

### The executor builds it

Claude starts in a new worktree on branch `exec-setup-ci`, follows
`MISSION.md`, commits there, and writes `EXECUTION.md`: what it did, the files
it touched, the verification result, anything it couldn't finish.

### You finish

Read `EXECUTION.md` and the diff, merge `exec-setup-ci`, and push. The first
pull request after that is the real test of the workflow. The coordinator
never pushes or merges.

---

## 3. Orchestrate a feature

Same pipeline as example 2, but the ask changes behaviour, so OpenSpec is part
of it:

> Read `agents/ORCHESTRATOR.md` and act as the coordinator for: let users pick
> the greeting language with `--lang es|en`.

The coordinator checks `openspec/changes/` and `main` first:

- **No change exists yet.** The first mission is to *propose* it. The executor
  writes `openspec/changes/add-lang-flag/` on its branch; you review the intent
  exactly as in example 1 and merge it. Then the coordinator runs a second
  mission that *applies* it.
- **The change is already on `main`.** The mission is simply to apply
  `add-lang-flag`, and the executor follows `tasks.md`.

Either way, after you merge the implementation, say *"archive
add-lang-flag"* from `main`, and the new scenarios become part of
`openspec/specs/greeting/spec.md`.

---

## 4. Plan and review without Orca

The two skills work in any session, so you get the second opinion without the
pipeline.

1. **Plan, in Claude Code:**

   > Use the `plan` skill for: migrate the CLI from CommonJS to ES modules.

   It grills you and writes the packet to `~/repos/plans/<date>-<slug>/`.

2. **Review, in Codex:**

   > Use the `review-plan` skill on `~/repos/plans/2026-09-23-esm-migration/`.

   It writes `REVIEW.md` next to the plan.

3. **Reconcile, back in Claude Code:**

   > Read `REVIEW.md` and answer each finding in `PLAN.md`.

4. **Execute:** open a fresh session and paste `MISSION.md`. It was written to
   work with no other context.

---

## Good first asks

- *"Propose a feature that …"* runs the OpenSpec loop.
- *"Explore how we could …"* thinks it through before anything is proposed.
- *"What changes are in flight?"* lists open changes.
- *"Read `agents/ORCHESTRATOR.md` and act as the coordinator for: …"* starts a
  three-agent run.
- *"Use the `plan` skill for: …"* writes a plan you can hand to anyone.
