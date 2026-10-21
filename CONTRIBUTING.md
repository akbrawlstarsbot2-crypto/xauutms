# Contributing

Thanks for contributing to XAU Marks The Spot's Discord Bot Master Reference.

## Scope

This repository contains two things:

- a large master reference file for copy-paste adoption
- a clean modular starter for developers who want a sane public repo layout

Contributions should improve one of these without making the repository harder to understand.

## Project Values

Contributions must align with fair use, user safety, and responsible open-source practice.
This repository should not be advanced toward exploitative, deceptive, or harmful applications.

## Contribution Rules

- Keep changes focused.
- Preserve author credit to XAU Marks The Spot.
- Prefer small, composable templates over tightly coupled code.
- Avoid adding hidden external service requirements.
- Document any new environment variable in `.env.example` and `README.md`.
- If you add a dependency, update `requirements.txt` and explain why in the PR.
- Do not submit features intended for abusive automation, exploitative gambling flows, or manipulation of sensitive audiences.
- If a feature can be dual-use, include explicit safeguards and abuse-mitigation notes.

## Prohibited Contribution Areas

Pull requests are out of scope and may be closed without merge if they primarily enable:

- unlawful behavior or platform policy evasion
- scam, phishing, or impersonation workflows
- harassment, stalking, or doxxing automation
- exploitative betting/gambling systems, especially where minors or financially vulnerable users could be targeted
- engagement loops designed to pressure sensitive audiences into harmful spending or risky behavior

## Development Guidelines

- Target Python 3.10+
- Use `discord.py` idioms
- Keep slash commands typed and documented
- Prefer reusable helpers in `utils/` and `views/`
- Keep example data safe to commit; never commit secrets
- Default to least privilege for permissions and intents
- Prefer opt-in behavior over forced or hidden behavior

## Before Opening a PR

1. Run a syntax check on the changed Python files.
2. Confirm `.env.example` still matches the code.
3. Update README sections affected by your change.
4. Keep runtime files out of git.
5. Confirm the change does not introduce harmful-use pathways.
6. Add or update safeguards for moderation, permissions, and abuse controls when relevant.

## Pull Request Notes

Include:

- what changed
- why it changed
- whether it affects the modular starter, the master reference, or both
- any new env vars, commands, or dependencies
- explicit risk notes for dual-use features and how abuse is mitigated
