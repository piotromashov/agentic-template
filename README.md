# Agentic project template

A starting point for projects built **spec-first** by several AI coding agents
working together: Claude Code, Codex, OpenCode and Cursor. It bundles three
things that fit together but also work on their own:

1. **Spec-driven development with [OpenSpec](https://openspec.dev).** Every
   change starts as a reviewable proposal (intent, specs, design, decisions,
   tasks) before any code is written.
2. **Plan → adversarial review → execute.** One model plans and grills you
   until nothing is left open, a *different* model attacks the plan, and a
   third one executes it from a self-contained mission prompt.
3. **Multi-agent orchestration with Orca.** A coordinator agent runs that loop
   for you: it dispatches the reviewer and the executor into their own
   terminals and worktrees, and stops at a gate for your approval before
   anything is built.

> `PROJECT_NAME` and the `TODO`s are placeholders to replace when you start a
> real project. See [Using this as a template](#using-this-as-a-template).

---

## What's inside

| Framework | What it gives you | Where it lives |
|---|---|---|
| **OpenSpec, `intent-driven` schema** | Artifact chain **proposal → specs → design → adr → tasks**, the `/opsx:*` commands, living specs | `openspec/`, `.claude/commands/opsx/`, `.cursor/` |
| **Bound authoring skills** | One skill per artifact: `grill-me` (proposal), `gherkin-authoring` (specs), `c4-diagrams` (design), `architectural-decision-records` (adr) | `.claude/skills/` |
| **Git discipline** | The gates: a proposal reaches `main` before `apply`; archive only from `main`, after merge | `.claude/skills/openspec-git-discipline/` |
| **Adversarial authoring** | A "model council": an author subagent drafts, a reviewer subagent attacks | `.claude/skills/adversarial-authoring/`, `.claude/agents/` |
| **`plan` / `review-plan`** | Turn an ask into a plan packet another model can execute unattended, then red-team it | `.agents/skills/plan/`, `.agents/skills/review-plan/` |
| **Orchestration** | Playbook for a coordinator agent in Orca: plan, review, human gate, execute, report | [`ORCHESTRATOR.md`](ORCHESTRATOR.md) |
| **Agent entry points** | `CLAUDE.md` (Claude Code) and `AGENTS.md` (Codex, OpenCode, others) both point to the operating manual | `CLAUDE.md`, `AGENTS.md`, `agents/` |
| **No attribution** | Agents don't add `Co-Authored-By` or "Generated with" lines to commits and PRs | `.claude/settings.json`, `agents/AGENTS.md` |

---

## Two ways to work

**Solo, with the OpenSpec loop.** You and one agent, in Claude Code or Cursor:

```
/opsx:propose "<idea>"   →   review   →   /opsx:apply   →   /opsx:archive
   (proposal, specs,                       (implement        (merge specs,
    design, adr, tasks)                     the tasks)         file the change)
```

You review **intent** (a spec delta) instead of reverse-engineering it from a
diff, and the specs become living documentation of what the system is supposed
to do.

**Orchestrated, for bigger or riskier work.** A coordinator plans with you, a
second model reviews the plan, and a third executes it in an isolated worktree.
The next section explains how.

The two combine: a mission can be "apply OpenSpec change `<id>`". The executor
still follows [`agents/AGENTS.md`](agents/AGENTS.md), including the git gates.

---

## Orchestration

### The roles

| Role | Who | Does | Never does |
|---|---|---|---|
| **Human** | you | Answers the planning questions, approves at the gate, merges | — |
| **Coordinator** | Claude (Fable) in Orca's main tab, following `ORCHESTRATOR.md` | Plans with the `plan` skill, dispatches reviewer and executor, reconciles the review, reports | Write product code, push, merge |
| **Reviewer** | Codex, with the `review-plan` skill | Verifies the plan's load-bearing claims read-only, writes a verdict | Edit the plan or any code |
| **Executor** | Claude, with the model and effort the plan picked | Executes `MISSION.md` in its own worktree, verifies, commits | Push, merge, change the plan |

Reviewing with a **different model** is the point: it reads the plan cold and
doesn't share the planner's blind spots.

### The flow

```
 you ──ask──▶ Coordinator ──plan skill──▶ plan packet (~/repos/plans/<date>-<slug>/)
                  ▲                              │
                  │                              ▼
                  │                  Reviewer (Codex, review-plan)
                  └──── REVIEW.md: SHIP | REVISE | RETHINK
                  │
                  │  reconcile (max 2 rounds, then you decide)
                  ▼
            GATE: you approve / change / cancel
                  │ approve
                  ▼
            Executor (Claude, new child worktree) ──▶ EXECUTION.md + commit
                  │
                  ▼  optional: Codex reviews the diff ──▶ REVIEW-diff.md
            Coordinator reports ──▶ you merge
```

### The plan packet

The `plan` skill writes it **outside any repo**, in
`~/repos/plans/<YYYY-MM-DD>-<slug>/`, so plans never mix with the code they
describe.

| File | Written by | Contents |
|---|---|---|
| `ANALYSIS.md` | planner | The evidence: observed facts vs. claims vs. hypotheses, assumptions, rejected alternatives |
| `PLAN.md` | planner | Ordered steps with definition of done, verification and rollback; later, the answer to each review |
| `MISSION.md` | planner | Paste-ready prompt for the executor: objective, decisions already made, authorizations, hard stops, method. Ends with the `## Ejecución (orquestador)` block (model, effort, scope, verification) |
| `REVIEW-BRIEF.md` | planner | Briefing for the attacker: weakest claims first, what was never tested |
| `REVIEW.md` | reviewer | Verdict, verification table, findings `BLOCKING` / `SHOULD-FIX` / `CONSIDER` |
| `EXECUTION.md` | executor | What was done, files touched, verification result, deviations, loose ends |

For small work the executing agent does itself, the skill picks *light mode*
and writes only `PLAN.md`. Under orchestration the packet is always complete.

### Prerequisites

- Orca, with orchestration turned on (Settings → Experimental). Check with
  `orca status --json`.
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) and the
  [Codex CLI](https://github.com/openai/codex), both logged in. Keep Codex up to
  date: an outdated one shows an update dialog that blocks the dispatch.
- A plans directory: `mkdir -p ~/repos/plans`.
- A shell that doesn't prompt on start. With oh-my-zsh, put
  `zstyle ':omz:update' mode disabled` in `~/.zshrc`.

The *Preflight de entorno* section of [`ORCHESTRATOR.md`](ORCHESTRATOR.md)
lists every known way a run gets stuck, and how to recover.

### Running it

1. Open this repo in Orca and start `claude` in the main tab.
2. Tell it:

   > Read `ORCHESTRATOR.md` and act as the coordinator for this: *&lt;your ask&gt;*

3. Answer the planning questions. The `plan` skill reads the repo first and only
   asks what the evidence can't answer: what "done" means, what's out of scope,
   which permissions the work needs, what must never happen.
4. Wait for the review. The coordinator accepts or rejects each finding,
   records why in `PLAN.md`, and runs a second round if a blocking finding is
   still in dispute.
5. **Gate.** It shows you the objective, the model it picked, the main risks,
   the findings it rejected, and the authorizations `MISSION.md` claims. Answer
   `aprobar`, `cambiar` or `cancelar`. Authorizations count only because you
   re-affirm them here: a file cannot grant authority.
6. The executor works in a child worktree named `exec-<slug>` and commits there.
   Read its `EXECUTION.md` and the diff, then **you merge**.

`ORCHESTRATOR.md` is written in Spanish (Rioplatense) because it is the
coordinator's own prompt; the flow is the same in any language.

### Without Orca

The two skills work on their own, in any harness that reads skills:

- **Plan:** in Claude Code, `/plan <your ask>`.
- **Review:** in Codex or another model, *"Use the `review-plan` skill on
  `~/repos/plans/<date>-<slug>/`"*.
- **Execute:** open a fresh session and paste `MISSION.md`.

---

## Getting started

**Prerequisites:** Node.js ≥ 20.19 and at least one AI coding tool (Claude Code,
Codex, OpenCode or Cursor).

```bash
# 1. Install the OpenSpec CLI (once, globally)
npm install -g @fission-ai/openspec@latest

# 2. Clone and enter the repo
git clone <repo-url> PROJECT_NAME && cd PROJECT_NAME

# 3. (If starting fresh) initialize OpenSpec for your tools
#    Already initialized in this repo — skip unless setting up a new project:
# openspec init --tools claude,cursor

# 4. Restart your IDE so the /opsx slash commands load, then:
#    /opsx:propose "your first feature"
```

Handy CLI commands:

```bash
openspec list            # active changes
openspec list --specs    # current capabilities
openspec validate --all  # check specs/changes for issues
```

---

## Project structure

```
PROJECT_NAME/
├── README.md             ← you are here
├── CLAUDE.md             ← pointer to agents/ (Claude Code)
├── AGENTS.md             ← same pointer, for Codex, OpenCode and other harnesses
├── ORCHESTRATOR.md       ← coordinator playbook for Orca orchestration
├── agents/
│   ├── AGENTS.md         ← the rules: workflow, conventions, safety
│   └── MEMORY.md         ← durable facts & decision log
├── openspec/
│   ├── config.yaml       ← active schema (intent-driven) + per-artifact skill rules
│   ├── schemas/          ← the intent-driven schema + artifact templates
│   ├── specs/            ← living specs = WHAT the system does (source of truth)
│   └── changes/          ← in-flight changes; archive/ holds completed ones
├── adr/                  ← durable Architecture Decision Records (immutable)
├── .agents/skills/       ← harness-neutral skills: plan, review-plan
├── .claude/
│   ├── settings.json     ← project settings (commit/PR attribution off)
│   ├── skills/           ← OpenSpec + authoring skills; plan, review-plan link to .agents/
│   ├── commands/opsx/    ← /opsx:* slash commands
│   └── agents/           ← adversarial-author / adversarial-reviewer subagents
├── .cursor/              ← OpenSpec commands + skills for Cursor
├── .gitignore
└── src/                  ← code (created as features are built)
```

Where knowledge lives: **requirements** → `openspec/specs/`; **how we work** →
`agents/AGENTS.md`; **facts & decisions** → `agents/MEMORY.md`; **plans** →
`~/repos/plans/`, outside the repo. When specs and docs disagree, the spec wins.

**Skills layout.** `plan` and `review-plan` live once, in `.agents/skills/`,
which Codex and OpenCode read; `.claude/skills/` has symlinks to them so Claude
Code sees the same files. On Windows, clone with symlinks enabled
(`git config --global core.symlinks true` and Developer Mode on) or the links
check out as plain text files. If you also keep personal copies in
`~/.claude/skills/` or `~/.agents/skills/`, keep a single source of truth so
they don't drift.

---

## Contributing

Changes start as proposals, not pull requests of raw code. Run
`/opsx:propose "<your idea>"`, refine the generated spec delta and tasks, then
`/opsx:apply`. See [`agents/AGENTS.md`](agents/AGENTS.md) for the full workflow
and safety rules.

---

## Using this as a template

1. Replace the **`PROJECT_NAME`** placeholder everywhere (`CLAUDE.md`,
   `AGENTS.md`, `agents/AGENTS.md`, `agents/MEMORY.md`, `adr/README.md`) and
   rewrite the top of this README for your project.
2. Fill in the `TODO` placeholders (description, stack, build/run/test, license).
3. Trim `.gitignore` to your stack.
4. Run `/opsx:propose "your first feature"` — the artifact chain is
   **proposal → specs → design → adr → tasks**.

---

## License

<!-- FILL IN: e.g. MIT. Add a LICENSE file. -->
_TODO_
