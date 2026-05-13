# Multi-Agent Maintainability Review

Run a scoped maintainability review with multiple read-only agents, then turn their findings into a practical, prioritized action plan. This skill is for teams that want more than a single reviewer pass: it separates exploration from proposal review, preserves dissenting opinions, and ends with clear next actions.

## Quick Links

- [Overview](#overview)
- [Installation](#installation)
- [SKILL.md](./SKILL.md)
- [Files](#files)
- [Related Skills](#related-skills)
- [Version History](../../CHANGELOG.md)

## Overview

`multi-agent-maintainability-review` helps you evaluate a repository, service, package, or folder without immediately changing code. It dispatches several explorer agents across different maintainability lenses, consolidates their findings into 20 concrete actions, then asks reviewer agents to classify each action as accepted, partially accepted, better solved another way, or not accepted.

The effect is a review report that is easier to act on:

- Concrete actions with scope and evidence.
- Fewer duplicate architecture comments.
- Explicit tradeoffs between impact, urgency, regression risk, and prerequisites.
- A final execution plan split into work to do now, work to design first, and work to defer or revisit.
- Reviewer disagreement kept visible instead of flattened into one generic recommendation.

## Installation

From the repository root:

```bash
./scripts/install.sh skills multi-agent-maintainability-review
```

This command assumes the repository installer is available at `scripts/install.sh`.

## When To Use

- You need a maintainability review for a bounded codebase scope.
- You want multiple independent perspectives before deciding what to change.
- You need file-backed recommendations, not broad architecture advice.
- You want a final Markdown-style report with prioritized follow-up work.
- You are comparing code patterns, framework usage, project organization, documentation, testing, CI, deployment, operations, or similar maintainability concerns.

## When Not To Use

- You already know the exact bug or failing test to fix.
- You want agents to edit files during the review.
- The requested scope is too broad to inspect meaningfully in one pass.
- You need a security audit, compliance audit, or production incident response as the primary outcome.
- You only need a short code review of one patch or pull request.

## Files

```text
skills/multi-agent-maintainability-review/
├── README.md
├── SKILL.md
└── agents/
    └── openai.yaml
```

- [`README.md`](./README.md): Human-facing overview, setup, links, and usage guidance.
- [`SKILL.md`](./SKILL.md): Runtime skill instructions and workflow.
- [`agents/openai.yaml`](./agents/openai.yaml): Agent configuration for this skill.

## SKILL.md Preview

Excerpt from [`SKILL.md`](./SKILL.md):

```markdown
Run a read-only, scope-bounded maintainability review with two rounds of subagents: exploration first, then review of the consolidated action list. Produce a final report that preserves subagent opinions and adds a pragmatic synthesis.
```

The workflow covers:

- Choosing review configuration.
- Bounding the review scope.
- Dispatching explorer agents.
- Consolidating findings into 20 actions.
- Dispatching reviewer agents.
- Producing a final report with priorities and follow-up buckets.

## Source Links

- [Source directory](https://github.com/makersfarm/Makers-Skills/tree/main/skills/multi-agent-maintainability-review)
- [Raw SKILL.md](https://raw.githubusercontent.com/makersfarm/Makers-Skills/main/skills/multi-agent-maintainability-review/SKILL.md)
- [Raw agent config](https://raw.githubusercontent.com/makersfarm/Makers-Skills/main/skills/multi-agent-maintainability-review/agents/openai.yaml)
- [Repository changelog](../../CHANGELOG.md)

## Related Skills

- [`ui-ux-pro-max`](../ui-ux-pro-max/SKILL.md): Use when the maintainability work includes UI/UX review, frontend implementation quality, or design-system-facing recommendations.

## Version History

See [CHANGELOG.md](../../CHANGELOG.md) for release notes and documentation updates.
