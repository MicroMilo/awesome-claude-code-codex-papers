# Evaluation Protocol Checklist

Use this checklist when reviewing a paper or designing a reproduction.

## Product identity

- Product name and CLI/runtime version
- Backbone model and model snapshot
- Reasoning effort or inference mode
- Date of execution for drifting hosted products

## Environment

- Repository commit and task specification
- Container or VM image
- Network access
- Tool and permission policy
- Context files such as AGENTS.md or CLAUDE.md

## Budget

- Wall-clock timeout
- Maximum turns or iterations
- Input and output token limits
- Maximum parallel agents
- Monetary budget

## Outcome

- Task success or pass rate
- Quality or domain-specific metric
- Wall-clock latency
- Token and monetary cost
- Tool calls and repair iterations
- Failure category

## Minimum comparison matrix

When practical, report three conditions:

1. The production product configuration, such as Claude Code or Codex CLI.
2. A neutral harness using the same model and budget.
3. The proposed method using the same model and budget.

Any variable that cannot be held fixed should be documented as a caveat rather than silently ignored.
