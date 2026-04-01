# AI and Developer Instructions

This file exists so both human developers and AI models can work in the same repository without drifting out of scope.

## Non-negotiable Instructions

1. Stay inside the assignment scope.
2. Use the current Jira ticket as the source of truth for the immediate task.
3. Read the existing documentation before making changes.
4. Build on previous work instead of replacing it unless replacement is explicitly required.
5. Update the repository documentation in the same pull request as the code or structure change.
6. Prefer simple, stable, low-risk solutions.
7. Leave clear handoff notes for the next person.

## Required Reading Order Before Changing Anything

Every developer or AI model should read files in this order:
1. `README.md`
2. `docs/PROJECT_SCOPE.md`
3. `docs/ARCHITECTURE_DECISIONS.md`
4. `docs/DEV_LOG.md`
5. `docs/TEAM_HANDOFF.md`
6. Relevant Jira issue

## Instructions for AI Models

When asked to work in this repository, AI should:
- summarize the current task in one or two sentences
- identify which team owns the work
- confirm which files are likely to change
- avoid changing unrelated files
- preserve previous documentation unless it is clearly outdated
- append to logs rather than rewriting history
- document assumptions explicitly
- ask for clarification only when the task cannot proceed safely

### AI Scope Guardrails

AI must not:
- invent new product requirements
- introduce authentication, cloud deployment, or unrelated infrastructure
- silently change API contracts or DB schema without documenting it
- delete previous team notes without reason
- change multiple teams' work areas unless the Jira issue calls for it

## Documentation Update Rule for Every PR

Every PR must answer these questions in the repo docs:
- What changed?
- Why did it change?
- What assumptions were made?
- What is still unfinished?
- What should the next person do next?

## Required Doc Updates by Situation

### If Structure Changed
Update:
- `README.md`
- `docs/DEV_LOG.md`
- `docs/TEAM_HANDOFF.md`

### If a Technical Decision Changed
Update:
- `docs/ARCHITECTURE_DECISIONS.md`
- `docs/DEV_LOG.md`
- `docs/TEAM_HANDOFF.md`

### If Work Was Completed on a Jira Issue
Update:
- `docs/DEV_LOG.md`
- `docs/TEAM_HANDOFF.md`
- PR description using the PR template

### If Work Was Blocked
Update:
- `docs/DEV_LOG.md`
- `docs/TEAM_HANDOFF.md`
- Jira status/comment

## Commit Guidance

Use readable commit messages tied to Jira.

Examples:
- `SE3-23 initialize backend folder structure`
- `SE3-21 add draft schema notes and sql examples`
- `SE3-32 create qa test plan skeleton`

## Pull Request Guidance

A PR should be small enough that another student can review it quickly.

A PR should include:
- Jira issue link or ID
- summary of change
- files changed
- test or verification notes
- documentation updates
- blockers or follow-up work

## Handoff Guidance

Always assume the next person starts with zero context.

Your handoff note should say:
- what is finished
- what is not finished
- where the next person should start
- what commands or files matter most
- what risks or assumptions remain
