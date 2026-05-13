---
name: multi-agent-maintainability-review
description: Use when the user asks for a scoped codebase or project maintainability review using multiple subagents, especially for code patterns, development patterns, framework usage, project organization, documentation, and final consolidated recommendations.
---

# Multi-Agent Maintainability Review

## Overview

Run a read-only, scope-bounded maintainability review with two rounds of subagents: exploration first, then review of the consolidated action list. Produce a final report that preserves subagent opinions and adds a pragmatic synthesis.

## Preconditions

- Keep the review scope explicit: repository, folder, package, service, or module path.
- Stay read-only unless the user explicitly asks to write a report file.
- Use subagents only when the user explicitly asks for subagents, multi-agent work, delegation, or this skill's workflow.
- Default review points: code patterns, development patterns, framework usage, project organization, documentation.
- Add tests, CI, deployment, operations, security, typing, and dependency management when they are relevant to maintainability.

## Workflow

### 0. Choose Review Configuration

Before exploring, decide whether to use the default configuration or ask the user for custom values.

Default configuration:

| Setting | Default |
|---|---|
| Review points | code patterns, development patterns, framework usage, project organization, documentation |
| Explorer agents | 4 |
| Reviewer agents | 3 |
| Explorer output target | up to 20 actions per explorer |
| Consolidated actions | 20 |
| Reviewer status set | `수용`, `일부 수용`, `다른 방향으로 접근`, `수용하지 않음` |
| Final output | chat summary, Markdown document, or PR to the connected project git repository |
| Priority criteria | urgency, impact, regression risk, prerequisites |

Use the defaults when:
- the user already described the review points,
- the user asks for "the same method", "default", or "like before",
- asking would slow down a straightforward review.

Ask one concise customization question when the user explicitly wants to tune the workflow or the request is broad enough that defaults may waste work. Ask for only the missing values.

Customization prompt:

```text
초기 설정을 확인하겠습니다.
1. 리뷰 포인트는 기본값을 사용할까요, 아니면 직접 지정할까요?
2. 코드베이스 탐색 서브에이전트는 몇 개로 할까요? 기본값은 4개입니다.
3. 20개 항목 리뷰 서브에이전트는 몇 개로 할까요? 기본값은 3개입니다.
4. 최종 산출물은 채팅 요약, Markdown 문서, 연결된 프로젝트 git PR 중 무엇으로 할까요?
```

If the user customizes counts:
- Use at least 1 explorer and 1 reviewer.
- Keep the consolidated action count at 20 unless the user changes it.
- Match lens count to agent count. For fewer agents, merge adjacent lenses. For more agents, split lenses by subsystem or concern.
- In the final report, compute total opinions as `consolidated actions * reviewer agents`.

Final output handling:
- **Chat summary**: do not create files; return the consolidated result in the final response.
- **Markdown document**: write one Markdown file in the requested scope or requested path.
- **Project git PR**: create or reuse a branch, write the Markdown report in the connected project repository, run validation, commit, push, and open a PR only when the user explicitly requested this output and the environment supports the required git/GitHub operations.

### 1. Bound the Scope

Identify and repeat the exact scope before dispatching agents.

Good scope examples:
- `infosilo/` only
- `src/api` and its tests
- one FastAPI service, excluding dashboard/frontend
- documentation and deployment scripts under one folder

If scope is ambiguous and a wrong assumption would waste work, ask one concise question. Otherwise infer the narrowest reasonable scope from the user's words and current workspace.

### 2. Dispatch Explorer Agents

Send the configured number of independent read-only explorer agents. Give each the same project scope and review points, but assign a different lens. Ask each agent for up to 20 concrete maintainability actions with file/line references and reasons.

Default lenses for 4 explorers:

| Explorer | Lens |
|---|---|
| A | Architecture, framework usage, routing/composition, dependency boundaries |
| B | Domain workflow, service layer, typing, error handling, external integrations |
| C | Persistence, migrations, data contracts, configuration, operational safety |
| D | Tests, CI/dev workflow, packaging, docs, deployment/runbooks |

Lens adjustment:
- 1 explorer: use all review points in one broad pass.
- 2 explorers: split into architecture/service and data/tests/operations.
- 3 explorers: split into architecture/service, data/config, tests/docs/deploy.
- More than 4 explorers: split by project subsystem, framework, or risk area.

Explorer prompt template:

```text
Read-only exploration. Do not edit files. Scope is limited to: {scope}.

Review points: {review_points}.
Your lens: {lens}.

Find up to 20 maintainability actions. Each action must be concrete, scoped, and supported by file/line references when possible.
Return a numbered list. For each item include:
- action
- evidence/reference
- why it matters

Do not propose changes outside the scope.
```

### 3. Consolidate to 20 Actions

Merge the explorer outputs into one final list of 20 actions.

Rules:
- Deduplicate overlapping items.
- Prefer actions with direct evidence and clear maintenance payoff.
- Separate "broken now" from "structural improvement".
- Keep actions scoped to the bounded project area.
- Preserve important minority opinions as notes when an item is controversial.

Use concise action wording. Each action should be implementable or documentable later.

### 4. Dispatch Review Agents

Ask the configured number of reviewers to classify all 20 actions. Give every reviewer the same 20-item list and a distinct review lens.

Statuses:
- `수용`: accept as proposed.
- `일부 수용`: accept the direction, but narrow scope or change sequencing.
- `다른 방향으로 접근`: accept the problem, but use a different solution.
- `수용하지 않음`: do not pursue under current conditions.

Default lenses for 3 reviewers:

| Reviewer | Lens |
|---|---|
| A | Architecture/framework correctness and long-term modularity |
| B | Operations, testing, CI, deployment, production risk |
| C | Pragmatic cost/benefit, sequencing, churn control |

Reviewer lens adjustment:
- 1 reviewer: pragmatic overall acceptance review.
- 2 reviewers: architecture/framework and operations/testing.
- More than 3 reviewers: add security, product impact, documentation, or subsystem-specific reviewers.

Reviewer prompt template:

```text
Read-only review. Do not edit files. Scope is limited to: {scope}.

You are Reviewer {name}: {lens}.
Evaluate each of the 20 proposed maintainability actions below.

For EACH item, choose exactly one status:
- 수용
- 일부 수용
- 다른 방향으로 접근
- 수용하지 않음

Provide a concise reason in Korean. If you choose 일부 수용 or 다른 방향으로 접근, state what to change about the proposal.

Return a Markdown table with columns:
ID | 상태 | 이유

20 actions:
{actions}
```

### 5. Produce the Final Report

Use the configured final output mode. If the user did not specify a mode, default to chat summary unless they asked for a file or PR.

Recommended report structure:

```markdown
# {Project/Scope} 유지보수성 개선 검토

작성일: {date}

## 목적
## 리뷰어 관점
## 요약
## 20개 개선 항목
## {opinion_count}개 세부 의견
## 항목별 종합 판단
## 실행 우선순위
## 후속 실행 계획
## 최종 의견
```

For the opinion section, use one row per action and one column per reviewer:

```markdown
| ID | 개선 항목 | Reviewer A | Reviewer B | Reviewer C |
|---:|---|---|---|---|
```

For summary, include status counts across all reviewer opinions.

For prioritization, score or label each consolidated action with:
- **Urgency**: how soon the issue should be addressed.
- **Impact**: expected maintainability, reliability, or operational payoff.
- **Regression risk**: likelihood that the change itself can break behavior.
- **Prerequisites**: required earlier work, decisions, access, or design.

For synthesis, group actions into practical phases:
1. Small, high-confidence fixes.
2. Operational safety and validation boundaries.
3. Structural refactors.
4. Larger design changes that need a separate plan.

For the follow-up execution plan, use exactly three buckets:

| Bucket | Purpose |
|---|---|
| 바로 실행 | Low-risk, clear, high-confidence work that can start now. |
| 설계 후 실행 | Valuable work that needs sequencing, contract decisions, or design first. |
| 보류/재검토 | Work that is low priority, too risky now, blocked, or only partially accepted. |

## Quality Bar

Before finalizing:
- Confirm no code files were changed unless the user asked for implementation.
- Confirm all generated recommendations stay within scope.
- Confirm the report contains the configured number of consolidated actions and reviewer opinions.
- Confirm the final output mode was followed: chat summary, Markdown document, or project git PR.
- Confirm priority criteria include urgency, impact, regression risk, and prerequisites.
- Confirm the follow-up execution plan is split into `바로 실행`, `설계 후 실행`, and `보류/재검토`.
- Keep "수용" decisions separate from "일부 수용" and "다른 방향으로 접근"; do not flatten nuance.
- Include the assistant's own final judgment, not only subagent summaries.

## Common Mistakes

- Dispatching agents before scope is bounded.
- Asking all explorer agents the same generic question and getting duplicate lists.
- Treating "use subagents" as permission to edit code.
- Producing 60 opinions without a final synthesis.
- Calling broad architecture refactors "must do now" when reviewers recommend phased adoption.
