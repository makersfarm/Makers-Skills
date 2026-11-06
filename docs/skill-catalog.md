# Makers Skills Catalog

[Back to root README](../README.md)

Public catalog for the skills in this repository. `SKILL.md` remains the canonical runtime instruction file; this page is a concise discovery surface.

## Quick Navigation

[Catalog](#catalog) | [File Trees](#file-trees) | [SKILLmd Previews](#skillmd-previews) | [Related Skills](#related-skills)

## Catalog

| Skill | Best for | Category | Tags | SKILL.md | Raw |
| --- | --- | --- | --- | --- | --- |
| [`executive-status-brief`](../skills/executive-status-brief/SKILL.md) | Korean executive updates covering progress, necessary decisions and trade-offs, and context within 1,300 characters by default. | Reporting | `executive-reporting`, `status-update`, `decision-making`, `korean` | [Preview](../skills/executive-status-brief/SKILL.md) | [Raw](https://raw.githubusercontent.com/makersfarm/Makers-Skills/main/skills/executive-status-brief/SKILL.md) |
| [`multi-agent-maintainability-review`](../skills/multi-agent-maintainability-review/SKILL.md) | Scoped maintainability reviews using multiple subagents, consolidated recommendations, and pragmatic review synthesis. | Code review | `maintainability`, `subagents`, `review`, `documentation` | [Preview](../skills/multi-agent-maintainability-review/SKILL.md) | [Raw](https://raw.githubusercontent.com/makersfarm/Makers-Skills/main/skills/multi-agent-maintainability-review/SKILL.md) |
| [`ui-ux-pro-max`](../skills/ui-ux-pro-max/SKILL.md) | UI/UX planning, design critique, layout, accessibility, typography, color, and component guidance for web and mobile. | Design | `ui`, `ux`, `accessibility`, `design-system` | [Preview](../skills/ui-ux-pro-max/SKILL.md) | [Raw](https://raw.githubusercontent.com/makersfarm/Makers-Skills/main/skills/ui-ux-pro-max/SKILL.md) |

## File Trees

```text
skills/
  executive-status-brief/
    README.md
    SKILL.md  # Korean executive reporting instructions
    agents/
      openai.yaml
  multi-agent-maintainability-review/
    README.md
    SKILL.md  # Runtime instructions and review workflow
    agents/
      openai.yaml
  ui-ux-pro-max/
    README.md
    SKILL.md  # Runtime instructions and design guidance index
    data      # Placeholder path file copied from the source skill
    scripts   # Placeholder path file copied from the source skill
```

## SKILL.md Previews

### executive-status-brief

Writes Korean reports in the order 진행상황, 내가 결정해야할 것 및 trade-off, and 맥락을 알려줘야할 것. The default limit is 1,300 characters for the entire response. Verified progress is kept separate from plans or unverified outcomes, and no unnecessary decision or approval step is invented.

Links: [GitHub preview](../skills/executive-status-brief/SKILL.md) | [Raw](https://raw.githubusercontent.com/makersfarm/Makers-Skills/main/skills/executive-status-brief/SKILL.md)

### multi-agent-maintainability-review

Runs a read-only, scope-bounded maintainability review with explorer and reviewer subagents. Use it when the user asks for a scoped codebase or project maintainability review, especially around code patterns, framework usage, project organization, and documentation.

Links: [GitHub preview](../skills/multi-agent-maintainability-review/SKILL.md) | [Raw](https://raw.githubusercontent.com/makersfarm/Makers-Skills/main/skills/multi-agent-maintainability-review/SKILL.md)

### ui-ux-pro-max

Provides UI/UX design intelligence for web and mobile work, including style selection, accessibility, layout, typography, color systems, charts, and component guidance across common frontend stacks.

Links: [GitHub preview](../skills/ui-ux-pro-max/SKILL.md) | [Raw](https://raw.githubusercontent.com/makersfarm/Makers-Skills/main/skills/ui-ux-pro-max/SKILL.md)

## Related Skills

| Starting skill | Related skill | Relationship | Shared tags |
| --- | --- | --- | --- |
| [`multi-agent-maintainability-review`](../skills/multi-agent-maintainability-review/SKILL.md) | [`ui-ux-pro-max`](../skills/ui-ux-pro-max/SKILL.md) | Complements maintainability reviews when UI quality, accessibility, and frontend structure are part of the review scope. | `review`, `ux`, `frontend` |
| [`ui-ux-pro-max`](../skills/ui-ux-pro-max/SKILL.md) | [`multi-agent-maintainability-review`](../skills/multi-agent-maintainability-review/SKILL.md) | Complements UI/UX work when the request expands into broader codebase quality, architecture, or documentation review. | `review`, `documentation`, `quality` |

[Back to root README](../README.md)
