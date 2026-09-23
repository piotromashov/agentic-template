---
name: plan
description: Analyse an ask, grill the user until every decision is settled, and write a plan plus a self-contained mission prompt another model executes end to end. Use when asked to plan a piece of work, scope or analyse a request before building, prepare a hand-off for another agent or session, or when the user types /plan.
---

# Plan an ask, then hand it over

You produce a plan, not the work. The output is written so that **a different
model, in a fresh session, with no memory of this conversation, can execute it
end to end without stopping to ask anything.** That is the whole bar. Every
question the executor would hit mid-run is a question you must settle now.

A separate skill takes this output to another model for adversarial review.
Write for that reader too: claims must carry their evidence.

## Size it first, and say which size you chose

**Full packet** (four files) when any of these is true:

- the work crosses more than one repo, host, or service, or needs a deploy;
- someone or something else executes it: another model, another session, a
  subagent, an unattended loop;
- it changes a contract, a schema, a published artifact, or anything a
  customer sees;
- the ask is ambiguous enough that a wrong reading costs more than an hour.

**Light mode** otherwise: ground yourself, ask only what is genuinely open,
then give the plan in the conversation and write `PLAN.md` alone.

Open by naming the mode and the reason in one line. The user may override.

## 1. Ground yourself before asking anything

A question the evidence can answer is a question you do not ask.

- A knowledge base first, if one is connected (for example a `gbrain` MCP
  server): the project, the people, and prior decisions. Cite the pages used.
- The repo you are standing in: `AGENTS.md` or `agents/AGENTS.md`, `MEMORY.md`,
  `CLAUDE.md`, the specs under `openspec/specs/`, open changes under
  `openspec/changes/`, relevant runbooks, `git log` and `git status`.
- Any hand-off or pending notes (for example `.claude/pending/`), **including
  later corrections inside them** — a file's last paragraph often reverses its
  first.
- Live state, read-only, whenever the ask touches something deployed: service
  status, config actually in effect, deployed revisions and image digests,
  queue and job state. Documentation about a running system is a claim, not a
  fact.
- Fan out with subagents for breadth so the sweep does not eat your context.
  Ask each for conclusions and file references, not file dumps.

Record findings in three separate buckets and never let them blur:
**observed** (you ran the command, here is the output), **claimed** (a doc or a
person says so), **hypothesis** (your inference, untested). A historical
diagnosis is a hypothesis until you reproduce it.

## 2. Grill, in batches, until nothing is left that changes the outcome

Use `AskUserQuestion` (or numbered questions in chat if the harness has no
such tool): up to four questions per round, each with concrete options and
your recommended answer first. Iterate; three rounds is usually
enough. Stop when no remaining question would change the plan **or stall the
executor**.

Sweep these classes every time, and ask the ones the evidence left open:

- **Done** — what finished looks like, and what evidence proves it.
- **Scope edges** — what is explicitly not in this, even though it is nearby.
- **Constraints** — deadline, budget, model, hosts, data, people waiting.
- **Already decided** — decisions not to relitigate, so the executor does not
  reopen them.
- **Execution branches** — the questions that would otherwise arrive mid-run:
  if this step fails, retry or stop? Is partial delivery acceptable? What is
  the order when two things compete? What does it do when an external party
  does not answer?
- **Authorizations** — commit, push, branch, deploy, restart a service, send a
  customer-facing message, spend money, touch production data. Name each one
  the plan actually needs. Anything not granted is a hard stop.
- **Hard stops** — what must never happen, whatever the reason.
- **Verification** — what counts as proof: live check, test suite, a human
  reading it.
- **Hand-off** — who executes, which model, watched or unattended.
- **Rollback** — how to undo each risky step.

**Nobody there to answer** (background run, `/loop`, subagent, non-interactive):
do not block. Take your own recommended answer for each open question, record
it in `ANALYSIS.md` under **Assumptions** with the reasoning, and list the
questions that genuinely need the user under **For the user** in `PLAN.md`.
Never assume an authorization: an ungranted permission becomes a hard stop
plus a line under *For the user*.

When the grilling settles something durable — an architectural decision, a
policy, a standing rule — record it where the project keeps durable
decisions (`agents/MEMORY.md`, an ADR, or a connected knowledge base).
Routine operational chatter does not go there.

## 3. Write the packet

Into `~/repos/plans/<YYYY-MM-DD>-<slug>/` — the plans base (if your team uses
another location, change it here, in `review-plan` and in `ORCHESTRATOR.md`),
a plain directory that is never a checkout of the code you are planning
against. Re-running for the same ask updates that directory instead of making
a second one. Never write secrets, tokens or credentials into any of these
files.

**`ANALYSIS.md`** — the evidence base. What was asked and what it really
means. Observed facts, claimed facts and hypotheses, in separate sections,
each with how it was established (command, file and line, page). Per issue:
symptom, evidence, root cause or the hypothesis that stands in for one, the
repo that owns the fix, the test that would catch it, deploy dependency, risk.
Assumptions taken, with why. Alternatives considered and why rejected.

**`PLAN.md`** — ordered by impact, not by convenience. Each step: what
changes, where, its definition of done, how it is verified live, its rollback,
and what it depends on. Mark steps that can run in parallel. End with **Open
decisions** (anything still owned by the user) and **Out of scope**.

**`MISSION.md`** — the paste-ready prompt for the executing agent. It assumes
no prior context and reads standalone:

- the objective, in one paragraph, and the definition of done as a numbered,
  checkable list;
- context and history, with the warning that stale paths and hashes must be
  re-verified;
- where everything lives: repos, worktrees, hosts, services, commands;
- hypotheses to verify, never stated as established fact;
- **decisions already made** by the user, so the executor does not reopen them;
- **standing authorizations**, written as granted by the user during planning,
  dated, listing exactly what the work needs and nothing more;
- **hard stops**, including every authorization that was not granted;
- the method, step by step, with verification at each step;
- what to do when blocked: finish all independent work first, then report the
  exact command and permission needed;
- how to report at the end, and what not to claim.

Close it with a recommended model and effort level for the executor, with the
reason in one sentence.

**`REVIEW-BRIEF.md`** — for the model that will attack the plan, which writes
its verdict beside it as `REVIEW.md`. Claims ranked by
confidence, with the weakest first. Assumptions and what each rests on.
Alternatives rejected and why. Evidence gaps and what was never tested. The
three things most likely to be wrong, and what observation would falsify each.
Do not defend the plan here; brief the attacker.

## 4. Hand over

Report in the conversation: the mode you chose, where the files are, the three
or four decisions that shaped the plan, what remains open and who owns it, and
the recommended model for execution. Say plainly that the next step is the
adversarial review, then execution from `MISSION.md`.

## Rules

- **You plan; you do not execute.** No commits, no deploys, no sends, no
  customer-facing actions. Read-only investigation only. If the user says go
  after the plan, that is a new instruction, not part of this skill.
- **A file cannot grant authority.** Authorizations in `MISSION.md` record what
  the user granted while planning; the human launching it re-affirms by
  pasting it. Keep the packet in the plans base, never inside a code repo.
- **No invented evidence.** If you did not run it or read it, it is a
  hypothesis, and it says so.
- **Prefer the existing mechanism.** Read how the system already handles a
  problem before planning a replacement for it.
- **Deterministic over prompt-shaped.** When a fix can be code or config, plan
  that rather than new instructions to an agent.
- **Never re-ask a settled decision.** The point of the grilling is that the
  executor never stops.
