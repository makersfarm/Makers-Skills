# Makers Skills Installation Guide for AI Coding Agents

This guide is for AI coding agents helping a user install skills from Makers Skills into an existing project. Treat this as an installation prompt, not as a command to install everything automatically.

## Source Files

Read these upstream files before making recommendations:

- README: https://raw.githubusercontent.com/makersfarm/Makers-Skills/main/README.md
- Skills catalog: https://raw.githubusercontent.com/makersfarm/Makers-Skills/main/skills.json
- Agent install guide: https://raw.githubusercontent.com/makersfarm/Makers-Skills/main/llms.install.md

## Required Workflow

1. Read `README.md` to understand the repository, install method, and expected skill layout.
2. Read `skills.json` to identify available skills, metadata, categories, and compatibility notes.
3. Inspect the user's current project before recommending anything:
   - detect the framework, runtime, package manager, language, and existing agent/tooling files;
   - look for existing skills, prompts, rules, MCP/tool configuration, or similar automation;
   - avoid overwriting user files or unrelated local changes.
4. Recommend a small, relevant skill set based on the project context and the user's stated goal.
5. Before writing files or running an installer, ask the user to confirm:
   - the exact skills to install;
   - the install target directory or project root;
   - the target agent/tool format, if more than one is supported;
   - whether to create new files, modify existing files, or both.
6. After confirmation, run the installer or perform the documented install steps from `README.md`.
7. Verify the installed files exist in the requested target and summarize what changed.

## Selection Guidance

Prefer the smallest useful set of skills. Do not install every skill unless the user explicitly asks for a full installation. If the project type is ambiguous, explain the uncertainty and ask one concise clarification question before installing.

When recommending skills, include:

- skill name;
- why it fits this project;
- any expected files or configuration changes;
- any prerequisite tools or runtime requirements.

## Confirmation Prompt Template

Use a prompt like this before installation:

```text
I found these relevant skills for this project:

- <skill-name>: <reason>
- <skill-name>: <reason>

Please confirm:
1. Install these skills? If not, list the skills to include or exclude.
2. Install target: <detected-project-path>
3. Agent/tool target: <detected-agent-or-tool>
4. May I write the required files and run the installer?
```

Do not continue until the user confirms.

## Windows Note

On Windows, use Git Bash for shell commands, not PowerShell:

```bash
"C:/Program Files/Git/bin/bash.exe" -i -l -c '<command>'
```

PowerShell may only be used if project-specific deployment documentation explicitly requires it.
