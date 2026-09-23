# PROJECT_NAME

<!-- FILL IN: one or two sentences. What does PROJECT_NAME do, and for whom? -->
_TODO — short description of what this project does._

> **Status:** greenfield. Built with **spec-driven development** — we agree on
> *what* to build before writing code.

---

## How this project is built

This repo uses [**OpenSpec**](https://openspec.dev) with the **`intent-driven`**
schema. Requirements live as plain-markdown specs checked into the repo, and every
change starts as a reviewable proposal *before* any code is written.

The loop, run as slash commands in Claude Code or Cursor:

```
/opsx:propose "<idea>"   →   review   →   /opsx:apply   →   /opsx:archive
   (proposal, specs,                       (implement        (merge specs,
    design, adr, tasks)                     the tasks)         file the change)
```

The payoff: you review **intent** (a spec delta) instead of reverse-engineering
it from a diff, and the specs become living documentation of what the system is
supposed to do — not just what the code currently does.

---

## Getting started

**Prerequisites:** Node.js ≥ 20.19 and an AI coding tool (Claude Code or Cursor).

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
├── agents/
│   ├── AGENTS.md         ← the rules: workflow, conventions, safety
│   └── MEMORY.md         ← durable facts & decision log
├── openspec/
│   ├── config.yaml       ← active schema (intent-driven) + per-artifact skill rules
│   ├── schemas/          ← the intent-driven schema + artifact templates
│   ├── specs/            ← living specs = WHAT the system does (source of truth)
│   └── changes/          ← in-flight changes; archive/ holds completed ones
├── adr/                  ← durable Architecture Decision Records (immutable)
├── .claude/ , .cursor/   ← OpenSpec commands + skills + subagents
├── .gitignore
└── src/                  ← code (created as features are built)
```

Where knowledge lives: **requirements** → `openspec/specs/`; **how we work** →
`agents/AGENTS.md`; **facts & decisions** → `agents/MEMORY.md`. When specs and
docs disagree, the spec wins.

---

## Contributing

Changes start as proposals, not pull requests of raw code. Run
`/opsx:propose "<your idea>"`, refine the generated spec delta and tasks, then
`/opsx:apply`. See [`agents/AGENTS.md`](agents/AGENTS.md) for the full workflow
and safety rules.

---

## Using this as a template

This repo is a clean starting point for any **intent-driven** OpenSpec project.
It ships the `intent-driven` schema, the bound skills (`grill-me`, `c4-diagrams`,
`gherkin-authoring`, `architectural-decision-records`, `openspec-git-discipline`,
`adversarial-authoring`), the `opsx:*` commands, and the git-discipline gates. To
reuse it:

1. Replace the **`PROJECT_NAME`** placeholder everywhere (`README.md`,
   `CLAUDE.md`, `AGENTS.md`, `agents/AGENTS.md`, `agents/MEMORY.md`, `adr/README.md`).
2. Fill in the `TODO` placeholders (description, stack, build/run/test, license).
3. Trim `.gitignore` to your stack.
4. Run `/opsx:propose "your first feature"` — the artifact chain is
   **proposal → specs → design → adr → tasks**.

---

## License

<!-- FILL IN: e.g. MIT. Add a LICENSE file. -->
_TODO_
