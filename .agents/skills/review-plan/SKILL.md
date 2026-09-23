---
name: review-plan
description: Adversarially review a plan packet produced by the plan skill — verify its load-bearing claims read-only, attack its reasoning, and write a verdict to REVIEW.md. Use when asked to review, challenge, red-team or stress-test a plan or mission before it is executed, when pointed at a ~/repos/plans/<slug>/ directory, or when the user types /review-plan.
---

# Attack the plan before production does

You did not write this plan and you owe it nothing. Someone is about to hand
`MISSION.md` to an agent that will execute it end to end without stopping.
Your job is to find what breaks first, while it is still cheap.

You are usually a different model in a fresh session. That is the point. Read
the packet cold. Confidence in the writing is not evidence; a claim stated
firmly and a claim that is true look identical on the page.

## What you are given

A directory, normally `~/repos/plans/<YYYY-MM-DD>-<slug>/`, holding some of:
`ANALYSIS.md` (the evidence base), `PLAN.md` (ordered steps), `MISSION.md`
(the executable prompt), `REVIEW-BRIEF.md` (the planner's own account of where
it is weak). A light-mode packet may be `PLAN.md` alone. If the plan exists
only in a conversation, review that and say so.

**Read `REVIEW-BRIEF.md` last.** Form your own picture from the analysis, the
plan and the mission first. Then read the brief to see what the planner
already doubts. Reading it first anchors you to their framing, which is
exactly the bias this review exists to cancel.

## 1. Verify the load-bearing claims yourself

A load-bearing claim is one where, if it is false, a step fails or the plan
aims at the wrong thing. Go and check those, read-only:

- paths, file names, function names, config keys, service and unit names;
- commits, tags, image digests, deployed revisions, versions actually in
  effect rather than documented;
- that a named test, spec or contract exists and says what is claimed;
- that a described failure reproduces, and fails for the stated reason;
- that state the plan depends on is still there: queue contents, job status,
  enrolled records, pending sends.

**Read-only, without exception.** No writes, no commits, no deploys, no
restarts, no messages, no mutation of live data. If checking something would
change it, do not check it; record it as unverifiable and say what would be
needed.

Classify every claim you touch as **verified**, **contradicted** or
**unverifiable**, and keep the command or file reference that settles it.
Contradicted load-bearing claims are automatically blocking.

## 2. Attack along every dimension, not just the interesting one

- **Cause or symptom.** Is each fix aimed at a cause the evidence supports, or
  at the last error message someone saw? A retry dressed as a fix is a finding.
- **Stale ground.** Which facts were true when written and have moved since.
- **The verification is the weak point.** For each definition of done, ask
  whether it would still pass in a world where the bug is present. A check
  that cannot fail proves nothing.
- **Failure and partial success.** What happens when a step half-completes. Is
  it idempotent on retry. What if two runs overlap. What if the deploy lands
  on one host and not the other.
- **Reversibility.** Blast radius of each risky step, and whether the rollback
  is tested or merely asserted.
- **Coupling.** Who else reads or writes what this touches. What holds code or
  config in memory and therefore needs restarting. Ordering that is implied
  but never stated.
- **Executor stalls.** Anywhere a fresh agent would have to stop and ask: an
  unresolved decision, a missing permission, an ambiguous order, a name that
  exists in two places. The plan's own bar is that this never happens.
- **Authority fit.** Do the granted authorizations actually cover every step,
  and is anything granted wider than the work needs. Both directions are
  findings.
- **Safety.** Destructive, irreversible or customer-facing actions without a
  gate. Anything that could send, publish or delete on a bad branch.
- **Scope.** Steps that do not serve the objective, and steps the objective
  needs that nobody wrote down.
- **People.** Assumptions that someone external will answer, in time, at all.

**Settled decisions are out of bounds, with one exception.** `MISSION.md`
lists decisions the user already made; do not relitigate taste. If a settled
decision rests on a fact you just contradicted, that is in scope and it is
blocking.

## 3. Write `REVIEW.md` beside the packet

Structure it so the planner can act without reading twice:

- **Verdict** — `SHIP`, `REVISE` or `RETHINK`, with one sentence of reason.
  Advice to the user, not an automatic gate.
- **Verification table** — each load-bearing claim, its status, and the
  evidence or the reason it could not be checked.
- **Findings**, grouped `BLOCKING`, `SHOULD-FIX`, `CONSIDER`. Every finding
  carries: the claim or step it attacks, the evidence, a concrete failure
  scenario in one or two sentences, and a specific correction. A finding with
  no failure scenario is an opinion; cut it.
- **What holds up** — briefly, so the planner does not churn what is already
  sound.
- **Unverifiable and untested** — what you could not check, and the
  observation that would settle each one.

Severity discipline: `BLOCKING` means it fails, breaks something, or does harm
if executed as written. Not style, not preference, not a better idea you had.
**An empty blocking list is a legitimate and valuable result.** Manufacturing
findings to look thorough is the failure mode of this skill.

## 4. Hand back, do not fix

You never edit `ANALYSIS.md`, `PLAN.md`, `MISSION.md` or the brief. The
planning model reconciles: accepting, rejecting with reasons, recording what
it did. That split is the whole value; a critic who rewrites the work becomes
its author.

Report in the conversation: the verdict, the blocking findings in one line
each, and where `REVIEW.md` is. One review round is the default. A second is
warranted only when the planner contests a blocking finding, and then you
review the contested point, not the whole plan again.

## Rules

- Read-only on every system, always.
- Never print secrets, tokens, credentials or customer personal data, and
  never quote them into `REVIEW.md`.
- No finding without evidence or a falsifiable failure scenario.
- Say what you did not check. Silence reads as coverage.
- Do not soften a blocking finding because the plan is otherwise good, and do
  not inflate a nitpick because the plan is otherwise weak.
- Works unattended: write the file, report, ask nothing.
