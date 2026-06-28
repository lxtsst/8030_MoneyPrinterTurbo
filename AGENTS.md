# MoneyPrinterTurbo Workspace Agent Rules

This project is a local Workspace-managed fork/adaptation of MoneyPrinterTurbo.
Workspace-level rules still apply unless this file is more specific.

## Project Role

- Treat this repository as a third-party application fork with local deployment
  adaptations.
- Preserve upstream architecture unless the user explicitly asks for a redesign.
- Keep local runtime configuration, API keys, generated videos, logs, and
  deployment state out of tracked files.

## Source Authority

Use sources in this order:

1. Workspace `AGENTS.md` and `06_项目创建与治理分级规范.md`.
2. This project `AGENTS.md` and `docs/GOVERNANCE.md`.
3. Upstream project documentation in `README.md` and `README-en.md`.
4. Existing source, tests, and Docker compose files.

## Safety And Config

- Do not commit `.env`, `config.toml`, generated runtime config, local storage,
  API keys, provider credentials, cookies, upload tokens, or generated media.
- README examples must use placeholders such as `<user>@<host>`,
  `<remote-dir>`, `<project-root>`, and environment variable names.
- Remote deployment must require explicit target arguments; do not bake private
  hosts or usernames into scripts.
- Network/API calls and provider integrations should be opt-in during tests.

## Engineering Rules

- Keep changes narrow and compatible with upstream where practical.
- Add or preserve tests for changed core logic.
- Update README and `docs/TASK_LOG.md` when runtime, deployment, config, or
  security behavior changes.
- Prefer local-first operation and explicit operator-controlled deployment.
