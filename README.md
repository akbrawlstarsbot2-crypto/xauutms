# Discord Bot Master Reference

Author: XAU Marks The Spot

A production-scale Discord bot starter and reference template built on `discord.py`, designed to work in two modes:

- a clean modular starter for real GitHub repos
- a single massive master reference for copy-paste adoption

This repository is meant to be a practical foundation for almost any common Discord bot build: moderation, economy, tickets, leveling, role menus, polls, giveaways, reminders, starboard, suggestions, stats channels, music, automod, and more.

## What This Repo Includes

- A clean modular starter entrypoint: `bot.py`
- A single large master reference file: `discord-bot-master-reference.py`
- Starter packages: `cogs/`, `utils/`, `views/`
- Complete slash-command patterns
- UI templates: buttons, selects, modals, paginators, confirmations, persistent views
- Storage patterns: JSON + SQLite
- Production helpers: logging, autosave, cooldowns, permissions, error handling
- 10 popular bot system templates beyond the base core:
  - custom help command
  - fun commands
  - polls
  - giveaways
  - starboard
  - reminders
  - music bot skeleton
  - automod / anti-spam
  - live stats channels
  - suggestion system

## Core Systems Covered

- configuration and env validation
- logging and log channels
- atomic JSON persistence
- SQLite abstraction
- permission guards
- cooldown helpers
- embed builders
- Discord UI component patterns
- command groups and cogs
- moderation skeleton
- economy skeleton
- ticket system skeleton
- welcome / goodbye system
- self-role menu skeleton
- XP / leveling system
- audit-style log relay
- event reference library
- utility helpers

## Requirements

- Python 3.10+
- FFmpeg on your PATH if you want music support
- A Discord application and bot token

Install dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

1. Create a Discord bot in the Discord Developer Portal.
2. Enable the intents you actually use, especially privileged intents if needed:
   - `SERVER MEMBERS INTENT`
   - `MESSAGE CONTENT INTENT`
3. Copy `.env.example` to `.env`.
4. Fill in your bot token and owner ID.
5. Run the modular starter:

```bash
python bot.py
```

6. Or run the full master reference directly:

```bash
python discord-bot-master-reference.py
```

## Environment Variables

The repo ships with a ready-to-copy `.env.example`.

| Variable | Required | Purpose |
|---|---|---|
| `DISCORD_TOKEN` | Yes | Your bot token |
| `OWNER_ID` | Yes | Your Discord user ID for owner-only commands |
| `LOG_CHANNEL_ID` | No | Log / audit embed channel |
| `WELCOME_CHANNEL_ID` | No | Default welcome / goodbye channel |
| `STARBOARD_CHANNEL_ID` | No | Starboard destination channel |
| `SUGGESTIONS_CHANNEL_ID` | No | Suggestion board channel |
| `TEST_GUILD_ID` | No | Dev guild for fast slash-command sync |
| `BOT_PREFIX` | No | Prefix for the modular starter, default `!` |

## Project Layout

```text
.
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml
│   │   ├── config.yml
│   │   └── feature_request.yml
│   ├── workflows/
│   │   └── python.yml
│   ├── dependabot.yml
│   └── pull_request_template.md
├── .editorconfig
├── bot.py
├── cogs/
│   ├── __init__.py
│   ├── admin.py
│   └── general.py
├── discord-bot-master-reference.py
├── utils/
│   ├── __init__.py
│   ├── config.py
│   └── embeds.py
├── views/
│   ├── __init__.py
│   └── confirm.py
├── README.md
├── CONTRIBUTING.md
├── SECURITY.md
├── CODE_OF_CONDUCT.md
├── CHANGELOG.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── .env.example
├── .gitignore
├── GITHUB_DESCRIPTION.txt
└── bot_data/
    ├── database.example.json
    └── database.json
```

Notes:

- `bot.py` is the clean modular starter you can use for a normal GitHub project.
- `discord-bot-master-reference.py` remains the large all-in-one reference file.
- `database.json` is the local runtime JSON store and is ignored by git.
- `database.example.json` is a tracked starter template.
- `bot.db` is created automatically at runtime and ignored by git.
- `bot.log` is created automatically at runtime and ignored by git.

## Starter vs Reference

Use `bot.py` if you want a normal maintainable repo layout with cogs and shared helpers.

Use `discord-bot-master-reference.py` if you want the complete one-file template library with all systems and examples in one place.

## Ready-Made Template Sections

Search the file for these section tags:

- `§01` to `§30` cover the core bot reference and production helpers
- `§31` to `§40` cover the extra popular bot templates

Highlights from the extra expansion:

- `§31 HELP-CMD`: dynamic help command
- `§32 FUN-CMD`: 8ball, trivia, coinflip, RPS, jokes, choose
- `§33 POLL-SYS`: button polls with vote tracking
- `§34 GIVE-SYS`: timed giveaways and rerolls
- `§35 STAR-SYS`: starboard relay
- `§36 REMIND-SYS`: timed reminders with DM delivery
- `§37 MUSIC-SKEL`: yt-dlp + FFmpeg queue skeleton
- `§38 AUTOMOD`: anti-spam, caps, links, mentions
- `§39 STATS-CHAN`: live server stats channels
- `§40 SUGGEST-SYS`: suggestion workflow with approval / denial

## Making It Your Own

The intended workflow is:

1. Start from `bot.py` if you want a usable public repo immediately.
2. Keep the master file as your long-form reference base.
3. Copy only the sections you actually want from the reference into your modular bot.
4. Replace JSON-backed systems with SQLite-backed logic as your usage grows.

## XAU Marks The Spot features

The enabled cogs include fun commands, polls, giveaways, reminders, moderation, economy, XP/levels, tickets, suggestions, starboard, server stats, and music. SQLite data is stored in `bot_data/xau.sqlite3`; small atomic JSON persistence helpers are in `utils/json_store.py`.

### Required setup

1. Copy `.env.example` to `.env` and set `DISCORD_TOKEN` and `OWNER_ID`.
2. Invite the bot with `bot` and `applications.commands` scopes and the permissions used by the features you enable.
3. Enable **Message Content Intent** and **Server Members Intent** in the Discord Developer Portal for anti-spam, XP, and member stats.
4. Set `STARBOARD_CHANNEL_ID` and `SUGGESTIONS_CHANNEL_ID` in `.env` if you want dedicated channels; otherwise suggestions go to the channel where `/suggest` is run.
5. For fast command updates while testing, set `TEST_GUILD_ID` to your server ID. Global slash command updates can take time to appear.
6. Music playback requires FFmpeg installed and available on PATH. Keep `yt-dlp` updated. Use media sources you have permission to play.

### Commands

Use Discord's `/` picker to explore commands. Main groups include `/8ball`, `/coinflip`, `/dice`, `/choose`, `/poll`, `/giveaway`, `/remindme`, `/purge`, `/warn`, `/warnings`, `/kick`, `/ban`, `/timeout`, `/balance`, `/daily`, `/work`, `/pay`, `/economy-top`, `/rank`, `/level-top`, `/ticket-panel`, `/suggest`, `/serverinfo`, `/stats-channel`, `/join`, `/play`, `/queue`, `/skip`, and `/stop`. Some commands require the relevant Discord server permission.


## `/say` announcement command

Members with **Manage Messages** can use `/say output:<message>` to post the text in a gold-colored announcement embed. The command is registered with the other slash commands at startup.

**Discord limitation:** Discord controls how slash-command invocations appear in chat. A bot cannot delete or hide the user's `/say` interaction itself through the bot API; the bot response contains only the styled announcement.
