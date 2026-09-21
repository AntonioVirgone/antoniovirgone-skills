# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root, or **`CONTEXT-MAP.md`** if it exists — it points at one `CONTEXT.md` per context.
- **`docs/adr/`** — read ADRs that touch the area you're about to work in.

If any of these files don't exist, **proceed silently**. Don't flag their absence; don't suggest creating them upfront. The `domain-modeling` skill creates them lazily when terms or decisions actually get resolved.

## Format

- `CONTEXT.md`: the project name as title, one paragraph describing the system, then `## Language` with one entry per term: `**Term**:` + a prose definition (what it is, what it depends on, what it is *not*) + a line `_Avoid_: synonyms not to use (and why)`. Entries cite the ADRs that ground them (`(ADR-0004)`).
- ADRs: `docs/adr/NNNN-slug.md`, four-digit numbering — check `ls docs/adr` before picking the number. A title that states the decision, then prose: context, the choice, the rejected alternative and why, the consequences. When a later ADR supersedes part of one, the old ADR stays and gains a `> **Superata da ADR-00NN** su …` block saying what remains in force.

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, a test name), use the term as defined in `CONTEXT.md`. Don't drift to synonyms the glossary explicitly avoids.

If the concept you need isn't in the glossary yet, that's a signal — either you're inventing language the project doesn't use (reconsider) or there's a real gap (note it for `domain-modeling`).

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> _Contradicts ADR-0007 (event-sourced orders) — but worth reopening because…_
