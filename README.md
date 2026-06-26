# smartcrate

<!-- FILL IN: one or two sentences. What does smartcrate do, and for whom? -->
_TODO — short description of what this project does._

> **Status:** greenfield. Built with **spec-driven development** — we agree on
> *what* to build before writing code.

---

## How this project is built

This repo uses [**OpenSpec**](https://openspec.dev) for spec-driven development.
Requirements live as plain-markdown specs checked into the repo, and every
change starts as a reviewable proposal *before* any code is written.

The loop, run as slash commands in Claude Code or Cursor:

```
/opsx:propose "<idea>"   →   review   →   /opsx:apply   →   /opsx:archive
   (proposal, specs,                       (implement        (merge specs,
    design, tasks)                          the tasks)         file the change)
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
git clone <repo-url> smartcrate && cd smartcrate

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
smartcrate/
├── README.md             ← you are here
├── CLAUDE.md             ← pointer to agents/ (for AI tools)
├── agents/
│   ├── AGENTS.md         ← the rules: workflow, conventions, safety
│   └── MEMORY.md         ← durable facts & decision log
├── openspec/
│   ├── specs/            ← living specs = WHAT the system does (source of truth)
│   └── changes/          ← in-flight changes; archive/ holds completed ones
├── .claude/ , .cursor/   ← OpenSpec slash commands + skills
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

This repo is a clean starting point for any spec-driven project. To reuse it:
rename the project, replace the `TODO` placeholders in `README.md`,
`agents/AGENTS.md`, and `agents/MEMORY.md`, trim `.gitignore` to your stack, and
run `/opsx:propose` for your first feature.

---

## License

<!-- FILL IN: e.g. MIT. Add a LICENSE file. -->
_TODO_
