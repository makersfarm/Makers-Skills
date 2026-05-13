# Makers Skills

[![Last commit](https://img.shields.io/github/last-commit/makersfarm/Makers-Skills?label=updated)](https://github.com/makersfarm/Makers-Skills/commits/main)
[![Skills](https://img.shields.io/badge/skills-2-blue)](#skills)
[![Agent install](https://img.shields.io/badge/agent%20install-llms.install.md-green)](https://raw.githubusercontent.com/makersfarm/Makers-Skills/main/llms.install.md)

Makersfarm Codex custom skills for reusable agent workflows, reviews, and product design work.

## Quick Links

[Skills](#skills) · [Install](#install) · [Agent prompt](#agent-prompt) · [Files](#files) · [Catalog](docs/skill-catalog.md) · [Changelog](CHANGELOG.md) · [Support](SUPPORT.md) · [Issues](https://github.com/makersfarm/Makers-Skills/issues)

## Trust Metadata

| Field | Link |
| --- | --- |
| Source repository | [makersfarm/Makers-Skills](https://github.com/makersfarm/Makers-Skills) |
| Machine-readable catalog | [skills.json](skills.json) |
| AI-agent install guide | [raw `llms.install.md`](https://raw.githubusercontent.com/makersfarm/Makers-Skills/main/llms.install.md) |
| Version history | [CHANGELOG.md](CHANGELOG.md) |
| Support policy | [SUPPORT.md](SUPPORT.md) |

## Skills

| Skill | Best for | Effect | Files |
| --- | --- | --- | --- |
| `multi-agent-maintainability-review` | Scoped codebase maintainability reviews | Coordinates exploration and review agents, consolidates concrete actions, and preserves dissenting opinions in a final report. | [SKILL.md](skills/multi-agent-maintainability-review/SKILL.md) · [raw](https://raw.githubusercontent.com/makersfarm/Makers-Skills/main/skills/multi-agent-maintainability-review/SKILL.md) · [source](skills/multi-agent-maintainability-review/) |
| `ui-ux-pro-max` | Web and mobile UI/UX planning, implementation, and review | Applies structured UX, accessibility, layout, typography, color, style, and chart guidance across common product surfaces. | [SKILL.md](skills/ui-ux-pro-max/SKILL.md) · [raw](https://raw.githubusercontent.com/makersfarm/Makers-Skills/main/skills/ui-ux-pro-max/SKILL.md) · [source](skills/ui-ux-pro-max/) |

See the full [skill catalog](docs/skill-catalog.md) for tags, compatibility notes, and discovery metadata.

## Install

Install one skill:

```bash
curl -fsSL https://raw.githubusercontent.com/makersfarm/Makers-Skills/main/scripts/install.sh | bash -s -- skills ui-ux-pro-max
```

Install multiple skills:

```bash
curl -fsSL https://raw.githubusercontent.com/makersfarm/Makers-Skills/main/scripts/install.sh | bash -s -- skills multi-agent-maintainability-review ui-ux-pro-max
```

Install from a local checkout:

```bash
./scripts/install.sh skills multi-agent-maintainability-review ui-ux-pro-max
```

## Agent Prompt

For AI coding agents, point them at the raw install guide:

```text
Read and follow https://raw.githubusercontent.com/makersfarm/Makers-Skills/main/llms.install.md before recommending or installing Makers Skills.
```

## Files

```text
.
├── README.md
├── CHANGELOG.md
├── SUPPORT.md
├── docs/
│   └── skill-catalog.md
├── llms.install.md
├── scripts/
│   ├── install.sh
│   ├── uninstall.sh
│   └── validate-skills.py
├── skills.json
└── skills/
    ├── multi-agent-maintainability-review/
    │   ├── agents/
    │   │   └── openai.yaml
    │   ├── README.md
    │   └── SKILL.md
    └── ui-ux-pro-max/
        ├── data
        ├── README.md
        ├── scripts
        └── SKILL.md
```

## Support

Use [SUPPORT.md](SUPPORT.md) for support expectations, [GitHub Issues](https://github.com/makersfarm/Makers-Skills/issues) for bugs or requests, and [CHANGELOG.md](CHANGELOG.md) for version history.
