# Governance

This is a Workspace-managed third-party application fork/adaptation.

## Required Entry Points

- `AGENTS.md`: project-specific agent rules.
- `README.md` and `README-en.md`: upstream-oriented usage documentation.
- `docs/STATUS.md`: current local Workspace status.
- `docs/TASK_LOG.md`: local adaptation and validation notes.

## Repository Hygiene

Tracked files must remain portable and non-sensitive:

- no real API keys or provider credentials;
- no `.env`, `config.toml`, generated runtime config, logs, or local storage;
- no private hostnames, private IPs, or local usernames in README examples or
  scripts;
- no generated videos, downloaded media, or one-off local outputs unless they
  are deliberate test fixtures.

## Governance Boundary

- Keep upstream product documentation intact where possible.
- Add local Workspace notes in project governance docs instead of embedding
  private deployment details into upstream README sections.
- Treat publishing, remote deployment, and provider API spending as
  approval-gated actions.
