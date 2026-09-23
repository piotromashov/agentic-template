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
   for you: it dispatches the reviewer (read-only) and the executor (in its own
   worktree), and stops at a gate for your approval before anything is built.

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

**Harness support.** Claude Code gets everything. Codex and OpenCode get the
entry point (`AGENTS.md`) and the `plan` / `review-plan` skills. Cursor gets the
core OpenSpec commands and skills (`.cursor/`), but not git discipline,
`bulk-apply`, adversarial authoring or `plan` / `review-plan`.

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

**How the two fit.** A plan packet never replaces an OpenSpec change. When an
ask changes what the system does, the orchestrated mission is either:

- **apply** a change whose proposal is already on `main` (`/opsx:apply <id>`), or
- **propose** it: the executor writes the change's artifacts, you merge them to
  `main`, and a second mission applies it.

The executor follows [`agents/AGENTS.md`](agents/AGENTS.md) either way,
including the git gates. After you merge an applied change, run
`/opsx:archive` from `main`.

---

## Orchestration

### Words you'll see

| Term | Meaning |
|---|---|
| **Orca** | The app that hosts the agents. Each agent runs in its own terminal tab, often in its own git worktree |
| **Main tab** | The Orca terminal where you talk to the coordinator |
| **Run** | One orchestrated objective, e.g. "add CSV export". Holds its tasks |
| **Task** | One unit of work inside a Run: a review round, an execution, a fix |
| **Dispatch** | One attempt of an agent at a task, started with `worker-start`. A failed dispatch can be retried |
| **Worker** | The agent (Codex or Claude) that took a dispatch |
| **Child worktree** | A new git worktree plus branch (`exec-<slug>`) created for the executor, so its changes stay isolated until you merge |
| **Gate** | A blocking question on a task. The execution task can't start until you answer it |
| **`worker_done`** | The message a worker sends when it finishes (`succeeded` or `failed`) |

The coordinator runs the `orca orchestration …` commands itself. The full,
current reference is `orca skills get orchestration --full`.

### The roles

| Role | Who | Does | Never does |
|---|---|---|---|
| **Human** | you | Answers the planning questions, approves at the gate, merges | — |
| **Coordinator** | Claude in Orca's main tab (the most capable model you have), following `ORCHESTRATOR.md` | Plans with the `plan` skill, dispatches reviewer and executor, reconciles the review, reports | Write product code or OpenSpec artifacts, commit, push, merge |
| **Reviewer** | Codex, with the `review-plan` skill, in the coordinator's worktree | Verifies the plan's load-bearing claims read-only, writes a verdict | Edit the plan or any code |
| **Executor** | Claude, with the model and effort the plan picked, in a child worktree | Executes `MISSION.md`, verifies, commits on `exec-<slug>` | Push, merge, change the plan |

Reviewing with a **different model** is the point: it reads the plan cold and
doesn't share the planner's blind spots.

### The flow

```
1. PLAN      you ⇄ Coordinator (plan skill)
                 └─▶ plan packet in ~/repos/plans/<date>-<slug>/

2. REVIEW    Coordinator ──packet──▶ Reviewer (Codex, review-plan)
             Coordinator ◀──REVIEW.md── verdict: SHIP | REVISE | RETHINK
             Coordinator answers each finding in PLAN.md
             (a 2nd round if needed; after 2, or on RETHINK, you decide)

3. GATE      Coordinator ──summary──▶ you: aprobar | cambiar | cancelar

4. EXECUTE   Coordinator ──MISSION.md──▶ Executor (Claude, child worktree)
             Executor ──▶ commit on exec-<slug> + EXECUTION.md

5. CHECK     (optional) Reviewer reads the diff ──▶ REVIEW-diff.md

6. CLOSE     Coordinator reports ──▶ you merge (and /opsx:archive if a change was applied)
```

### The plan packet

The `plan` skill writes it **outside any repo**, in
`~/repos/plans/<YYYY-MM-DD>-<slug>/`, so plans never mix with the code they
describe. To use another location, change it in both skills and in
`ORCHESTRATOR.md`.

| File | Written by | Contents |
|---|---|---|
| `ANALYSIS.md` | planner | The evidence: observed facts vs. claims vs. hypotheses, assumptions, rejected alternatives |
| `PLAN.md` | planner | Ordered steps with definition of done, verification and rollback; later, the answer to each review |
| `MISSION.md` | planner | Paste-ready prompt for the executor: objective, decisions already made, authorizations (including "commit on `exec-<slug>`"), hard stops, method. Ends with the `## Ejecución (orquestador)` block: model, effort, scope, verification |
| `REVIEW-BRIEF.md` | planner | Briefing for the attacker: weakest claims first, what was never tested |
| `REVIEW.md` | reviewer | Verdict, verification table, findings `BLOCKING` / `SHOULD-FIX` / `CONSIDER` |
| `REVIEW-1.md` | coordinator | The first round's `REVIEW.md`, renamed before a second round |
| `EXECUTION.md` | executor | What was done, files touched, verification result, deviations, loose ends |
| `REVIEW-diff.md` | reviewer | Optional review of the executor's diff against `MISSION.md` |

For small work the executing agent does itself, the `plan` skill picks *light
mode* and writes only `PLAN.md`. Under orchestration the packet is always
complete.

### Prerequisites

- **Orca** with orchestration turned on (Settings → Experimental). Check with
  `orca status --json`.
- **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** and the
  **[Codex CLI](https://github.com/openai/codex)**, both logged in. Keep Codex
  up to date: an outdated one shows an update dialog that blocks the dispatch.
  Model IDs change and depend on your account; check them with `/model`.
- **A plans directory the agents can write to.** `mkdir -p ~/repos/plans`, then
  add it as a writable root in Codex (`writable_roots` under
  `[sandbox_workspace_write]` in `~/.codex/config.toml`) and as
  `permissions.additionalDirectories` in `~/.claude/settings.json`. Without
  this, the reviewer and executor stop to ask before writing `REVIEW.md` and
  `EXECUTION.md`.
- **A shell that doesn't prompt on start.** With oh-my-zsh, put
  `zstyle ':omz:update' mode disabled` in `~/.zshrc`.

Also know the limit on **production writes**: Claude Code's auto mode refuses
commands that change live data even when settings allow them, so plan for a
person to approve those steps in the executor's tab. The *Preflight de
entorno* section of [`ORCHESTRATOR.md`](ORCHESTRATOR.md) covers this and every
other known way a run gets stuck, with how to recover.

### Running it

1. Open this repo in Orca and start `claude` in the main tab.
2. Tell it:

   > Read `ORCHESTRATOR.md` and act as the coordinator for this: *&lt;your ask&gt;*

3. Answer the planning questions. The `plan` skill reads the repo first and only
   asks what the evidence can't answer: what "done" means, what's out of scope,
   which permissions the work needs, what must never happen.
4. Wait for the review. The coordinator accepts or rejects each finding and
   records why in `PLAN.md`. It runs a second round when it rejected a blocking
   finding or when the accepted fixes change scope, architecture or the model.
   After two rounds, or on `RETHINK`, it asks you to decide.
5. **Gate.** It shows you the objective, the model it picked, the main risks,
   the findings it rejected, and the authorizations `MISSION.md` claims. Answer
   `aprobar` (approve), `cambiar` (change) or `cancelar` (cancel). Authorizations
   count only because you re-affirm them here; approving is also your OK for the
   executor to commit on its branch.
6. The executor works in the child worktree `exec-<slug>` and commits there.
   Read its `EXECUTION.md` and the diff, then **you merge** (and run
   `/opsx:archive` from `main` if it applied an OpenSpec change).

`ORCHESTRATOR.md` is written in Spanish (Rioplatense) because it is the
coordinator's own prompt; the gate options stay in Spanish too.

### Without Orca

The two skills work on their own, in any harness that reads skills:

- **Plan:** in Claude Code, *"Use the `plan` skill for: &lt;your ask&gt;"*.
  (`/plan` may open Claude Code's built-in plan mode instead of the skill.)
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
