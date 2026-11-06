# Executive Status Brief · 임원 보고

Write concise Korean executive updates that separate verified progress, decisions and trade-offs, and context. Unless the user requests another length, the entire response stays within 1,300 characters, including headings, spaces, links, and sources.

## Install

From the repository root:

```bash
./scripts/install.sh skills executive-status-brief
```

## Usage

```text
$executive-status-brief 현재 업무 진행상황을 임원 보고 형식으로 정리해줘.
```

The report uses three sections:

1. 진행상황
2. 내가 결정해야할 것 및 trade-off
3. 맥락을 알려줘야할 것

It distinguishes local validation from live success, requests only decisions that actually need user judgment, and does not treat a report as authorization to contact others or deploy changes.

## Files

- [SKILL.md](SKILL.md): Canonical reporting instructions.
- [agents/openai.yaml](agents/openai.yaml): Codex display metadata and example prompt.
- [Catalog](../../docs/skill-catalog.md) · [Changelog](../../CHANGELOG.md).
