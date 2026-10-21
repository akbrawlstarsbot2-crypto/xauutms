# Security Policy

## Supported Use

This repository is a template and starter project. Security-sensitive changes should be treated seriously, especially in these areas:

- token and secret handling
- permission checks
- moderation actions
- file exports and transcripts
- voice and external media processing
- user-generated content embedded into messages

## Safety and Abuse Boundaries

Security in this project includes protection from technical compromise and social harm.
Do not introduce features that can be reasonably used for abusive targeting, exploitation, or coercion.

High-risk areas that require extra review:

- monetization, betting, or chance-based reward mechanics
- direct messages, mass messaging, and growth automation
- any behavior that can influence minors or sensitive audiences toward harmful outcomes
- data collection or retention beyond what is operationally necessary

If a feature could be repurposed for exploitative gambling or manipulation of vulnerable users, it should be declined or redesigned with strict safeguards.

## Reporting a Vulnerability

Do not open a public issue for a live security problem involving secrets, abuse paths, or moderation bypasses.

Instead, report privately to the repository owner with:

- affected file or feature
- reproduction steps
- expected impact
- suggested fix, if known

Please avoid sharing active credentials, private user data, or exploit details that increase immediate risk.

## Coordinated Disclosure Expectations

- Acknowledge reports as quickly as possible.
- Prioritize issues that create immediate harm potential.
- Keep remediation discussions private until mitigations are available.
- Publish a sanitized advisory summary once resolved.

## Hardening Recommendations

- keep bot tokens only in `.env`
- give the bot the minimum Discord permissions it needs
- avoid enabling privileged intents unless required
- validate and clamp user inputs
- avoid mass actions without confirmation prompts
- keep FFmpeg and Python dependencies updated
- audit owner-only and admin-only commands carefully
- add rate limits and abuse throttles for command-heavy workflows
- avoid dark-pattern UX in economy-like interactions
- avoid storing personal data unless explicitly required and documented
- fail safe: if safety checks fail, deny the action