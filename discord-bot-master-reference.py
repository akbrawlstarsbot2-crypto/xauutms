"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║         DISCORD BOT MASTER REFERENCE — discord.py Ultimate Template             ║
║                  Every pattern, every skeleton, every tool.                     ║
║                          Author: XAU Marks The Spot                                   ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║  INDEX — Jump to any section using your editor's search (Ctrl+F the tag)        ║
╠════════════════╦═════════════════════════════════════════════════════════════════╣
║  TAG           ║  SECTION                                                        ║
╠════════════════╬═════════════════════════════════════════════════════════════════╣
║  §01 CONFIG    ║  Imports, Intents, Environment Validation                       ║
║  §02 LOGGING   ║  Logger Setup, Discord Log Channel                              ║
║  §03 DB-JSON   ║  Atomic JSON Save/Load                                          ║
║  §04 DB-SQL    ║  SQLite Abstraction Layer                                       ║
║  §05 PERMS     ║  Permission Helpers, Role Guards                                ║
║  §06 COOLDOWN  ║  Custom Cooldown Buckets, Decorators                            ║
║  §07 EMBEDS    ║  Embed Library (rich, compact, paged, error, success)            ║
║  §08 UI-BTN    ║  Button Views (restricted, toggle, link, danger-confirm)        ║
║  §09 UI-MODAL  ║  Modals (single, multi-field, chained/multi-step)               ║
║  §10 UI-SELECT ║  Select Menus (string, role, channel, user, multi)              ║
║  §11 UI-PAGE   ║  Paginator (forward/back, jump-to-page, per-page size)          ║
║  §12 UI-CONF   ║  Confirmation Dialog (yes/no with timeout)                      ║
║  §13 UI-PERSIST║  Persistent Views (survive bot restarts)                        ║
║  §14 CTX-MENU  ║  Context Menus (right-click user, right-click message)          ║
║  §15 BOT-CLASS ║  Bot Class, setup_hook, Cog loading, Status Rotation            ║
║  §16 BG-TASKS  ║  Background Tasks (autosave, status, cleanup, reminder)         ║
║  §17 ERR-HAND  ║  Global Error Handler (all error types categorized)             ║
║  §18 CMD-PAT   ║  Slash Command Patterns (A-J: all patterns)                     ║
║  §19 CMD-GRP   ║  Command Groups, Subcommand Groups                              ║
║  §20 COG-SKEL  ║  Cog Skeleton, Hot-reload Commands                              ║
║  §21 MOD-SYS   ║  Skeleton: Moderation (warn, mute, kick, ban, purge)            ║
║  §22 ECO-SYS   ║  Skeleton: Economy (balance, earn, pay, shop, leaderboard)      ║
║  §23 TKT-SYS   ║  Skeleton: Ticket System (create, close, transcript)            ║
║  §24 WEL-SYS   ║  Skeleton: Welcome/Goodbye System                               ║
║  §25 RXN-ROLES ║  Skeleton: Reaction Roles (button-based)                        ║
║  §26 LVL-SYS   ║  Skeleton: XP / Leveling System                                 ║
║  §27 LOG-SYS   ║  Skeleton: Server Audit Log Relay                               ║
║  §28 EVENTS    ║  Events Library (all major discord.py events)                   ║
║  §29 UTILS     ║  Utility Functions (chunking, time, mentions, fuzzy search)     ║
║  §30 RUNNER    ║  Execution Runner                                               ║
╠════════════════╬═════════════════════════════════════════════════════════════════╣
║  — EXPANSION: 10 MOST POPULAR BOT TEMPLATES —                                  ║
╠════════════════╬═════════════════════════════════════════════════════════════════╣
║  §31 HELP-CMD  ║  Custom Paginated Help Command (dynamic, category-grouped)      ║
║  §32 FUN-CMD   ║  Fun Commands (8ball, trivia, RPS, coinflip, choose, joke)       ║
║  §33 POLL-SYS  ║  Poll System (button votes, no double-vote, timed auto-close)   ║
║  §34 GIVE-SYS  ║  Giveaway System (timed, multi-winner, reroll, persistent)       ║
║  §35 STAR-SYS  ║  Starboard (reaction threshold, raw events, no duplicates)      ║
║  §36 REMIND-SYS║  Reminder System (DM on fire, list, cancel, recurring)           ║
║  §37 MUSIC-SKEL║  Music Bot Skeleton (yt-dlp, FFmpeg, queue, NowPlaying embed)    ║
║  §38 AUTOMOD   ║  Anti-Spam / AutoMod (rate, caps, links, mentions, escalation)  ║
║  §39 STATS-CHAN ║  Server Stats Voice Channels (live member/bot/boost counts)     ║
║  §40 SUGGEST-SYS║ Suggestion System (submit, vote, approve, deny, track)         ║
╚════════════════╩═════════════════════════════════════════════════════════════════╝

HOW TO USE THIS FILE:
  1. Copy any section or class into your bot project.
  2. Each class/function is self-contained and annotated with usage rules.
  3. Search any §TAG above to jump directly to the section.
  4. The bot at the bottom (§30) wires EVERYTHING together as a demo.

REQUIREMENTS:
    pip install discord.py python-dotenv yt-dlp PyNaCl
  FFmpeg must be installed and on system PATH (for music bot §37)

.env file must contain:
  DISCORD_TOKEN=your_token_here
  LOG_CHANNEL_ID=optional_channel_id_for_logs
  OWNER_ID=your_discord_user_id
  WELCOME_CHANNEL_ID=optional
  STARBOARD_CHANNEL_ID=optional
  SUGGESTIONS_CHANNEL_ID=optional
"""

# =============================================================================
# §01 CONFIG — Imports, Intents, Environment Validation
# =============================================================================

import os
import re
import json
import math
import random
import time
import asyncio
import logging
import sqlite3
import datetime
import textwrap
import traceback
import importlib
from io import StringIO, BytesIO
from typing import Optional, List, Dict, Any, Callable, Union, Tuple

import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import View, Button, Select, TextInput, Modal, RoleSelect, ChannelSelect, UserSelect, MentionableSelect
from dotenv import load_dotenv

# ─── Load .env before anything else ───────────────────────────────────────────
load_dotenv()

# ─── Required Tokens & IDs ────────────────────────────────────────────────────
TOKEN: str         = os.getenv("DISCORD_TOKEN", "")
LOG_CHANNEL_ID: int = int(os.getenv("LOG_CHANNEL_ID", "0") or "0")
OWNER_ID: int       = int(os.getenv("OWNER_ID", "0") or "0")

# ─── Environment Validation (call before bot.run) ─────────────────────────────
def validate_environment() -> bool:
    """
    GUIDE: Call this before starting the bot.
    Checks every required env variable and prints a clear error if missing.
    Returns True if all checks pass.
    """
    errors = []
    if not TOKEN:
        errors.append("DISCORD_TOKEN is missing from your .env file")
    if not OWNER_ID:
        errors.append("OWNER_ID is missing (used for owner-only commands)")
    if errors:
        print("═" * 60)
        print("  ENVIRONMENT VALIDATION FAILED")
        print("═" * 60)
        for err in errors:
            print(f"  ❌  {err}")
        print("═" * 60)
        return False
    print("✅ Environment validation passed.")
    return True

# ─── Intents ──────────────────────────────────────────────────────────────────
# GUIDE: Only enable what your bot actually needs. Extra intents = extra RAM.
# Privileged intents (members, message_content, presences) must also be enabled
# in the Discord Developer Portal under your bot's settings.
intents = discord.Intents.default()
intents.guilds          = True   # Always needed for guild bots
intents.members         = True   # Privileged — needed for on_member_join/leave, member lists
intents.messages        = True   # Receive message events
intents.message_content = True   # Privileged — read message text (for prefix cmds / listeners)
intents.reactions       = True   # Reaction events
intents.voice_states    = True   # Voice channel join/leave/move events
intents.presences       = False  # Privileged — Status/activity tracking. Disable unless needed.

# ─── Global Constants ─────────────────────────────────────────────────────────
EMBED_COLOR_DEFAULT  = 0x3498DB   # Blue
EMBED_COLOR_SUCCESS  = 0x2ECC71   # Green
EMBED_COLOR_WARNING  = 0xF39C12   # Orange
EMBED_COLOR_ERROR    = 0xE74C3C   # Red
EMBED_COLOR_NEUTRAL  = 0x95A5A6   # Grey
EMBED_COLOR_GOLD     = 0xF1C40F   # Gold (economy, levels)
EMBED_COLOR_PURPLE   = 0x9B59B6   # Purple (logs, admin)


# =============================================================================
# §02 LOGGING — Logger Setup, Discord Log Channel
# =============================================================================

# ─── Python Logger ────────────────────────────────────────────────────────────
# GUIDE: Use `logger.info()`, `logger.warning()`, `logger.error()` throughout
# your code instead of print(). Outputs to both console and an optional
# Discord channel (wired up in §15 BOT-CLASS).

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),                        # Console
        logging.FileHandler("bot.log", encoding="utf-8"),  # File
    ]
)
logger = logging.getLogger("MasterBot")

# Silence noisy discord.py internals (set to WARNING or ERROR to reduce spam)
logging.getLogger("discord").setLevel(logging.WARNING)
logging.getLogger("discord.http").setLevel(logging.WARNING)

async def send_log_to_channel(bot: commands.Bot, title: str, description: str, color: int = EMBED_COLOR_PURPLE):
    """
    GUIDE: Call anywhere to push a log embed to your designated log channel.
    Set LOG_CHANNEL_ID in .env to use this.

    Usage:
        await send_log_to_channel(bot, "User Banned", f"{user} was banned by {mod}")
    """
    if not LOG_CHANNEL_ID:
        return
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel and isinstance(channel, discord.TextChannel):
        embed = discord.Embed(title=title, description=description, color=color, timestamp=discord.utils.utcnow())
        try:
            await channel.send(embed=embed)
        except discord.Forbidden:
            logger.warning("Cannot send to log channel — missing permissions.")


# =============================================================================
# §03 DB-JSON — Atomic JSON Save/Load
# =============================================================================
# GUIDE: For small bots. Keeps all data in a single JSON file.
# Atomic save prevents data corruption on crash: writes to .tmp first, then renames.
# Scale limit: Fine up to ~10,000 users. Beyond that, use §04 DB-SQL.

CONFIG_DIR = os.path.join(os.getcwd(), "bot_data")
DB_FILE    = os.path.join(CONFIG_DIR, "database.json")

BOT_DATABASE: Dict[str, Any] = {}

def ensure_dirs():
    os.makedirs(CONFIG_DIR, exist_ok=True)

def load_json_db() -> dict:
    """Load JSON database from disk. Returns empty dict on failure."""
    try:
        if os.path.exists(DB_FILE):
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load JSON DB: {e}")
    return {}

def save_json_db(data: dict) -> bool:
    """
    Atomically save data dict to disk.
    Returns True on success, False on failure.
    """
    try:
        ensure_dirs()
        tmp = DB_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        # Atomic overwrite
        os.replace(tmp, DB_FILE)
        return True
    except Exception as e:
        logger.error(f"Failed to save JSON DB: {e}")
        return False

def db_get(key: str, default: Any = None) -> Any:
    """Get a value from the in-memory database."""
    return BOT_DATABASE.get(key, default)

def db_set(key: str, value: Any, autosave: bool = False) -> None:
    """Set a value in the in-memory database. Optionally persist immediately."""
    BOT_DATABASE[key] = value
    if autosave:
        save_json_db(BOT_DATABASE)

def db_delete(key: str, autosave: bool = False) -> None:
    """Remove a key from the in-memory database."""
    BOT_DATABASE.pop(key, None)
    if autosave:
        save_json_db(BOT_DATABASE)

# ─── Per-User / Per-Guild Namespacing ─────────────────────────────────────────
def user_key(user_id: int) -> str:
    """Returns the standard key for storing per-user data: 'user:123456'"""
    return f"user:{user_id}"

def guild_key(guild_id: int) -> str:
    """Returns the standard key for storing per-guild data: 'guild:123456'"""
    return f"guild:{guild_id}"

def get_user_data(user_id: int) -> dict:
    return BOT_DATABASE.setdefault(user_key(user_id), {})

def get_guild_data(guild_id: int) -> dict:
    return BOT_DATABASE.setdefault(guild_key(guild_id), {})


# =============================================================================
# §04 DB-SQL — SQLite Abstraction Layer
# =============================================================================
# GUIDE: Use this for anything relational: leaderboards, inventory, logs.
# Uses the synchronous sqlite3 module wrapped in run_in_executor so it doesn't
# block the asyncio event loop.
# For true async, swap to `aiosqlite` (pip install aiosqlite).

SQL_FILE = os.path.join(CONFIG_DIR, "bot.db")

class Database:
    """
    Lightweight synchronous SQLite wrapper that's safe to use from async code.
    
    Usage:
        db = Database()
        db.initialize()   # Call once at bot startup
        
        # Write
        db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        
        # Read one row
        row = db.fetchone("SELECT coins FROM users WHERE user_id=?", (user_id,))
        coins = row["coins"] if row else 0
        
        # Read all rows
        rows = db.fetchall("SELECT * FROM leaderboard ORDER BY xp DESC LIMIT 10")
    """
    def __init__(self, path: str = SQL_FILE):
        ensure_dirs()
        self.path = path
        self._conn: Optional[sqlite3.Connection] = None

    def connect(self):
        if self._conn is None:
            self._conn = sqlite3.connect(self.path, check_same_thread=False)
            self._conn.row_factory = sqlite3.Row  # Rows accessible by column name
            self._conn.execute("PRAGMA journal_mode=WAL")  # Better concurrency
            self._conn.execute("PRAGMA foreign_keys=ON")
        return self._conn

    def initialize(self):
        """Create all required tables if they don't exist. Add your own here."""
        conn = self.connect()
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                user_id     INTEGER PRIMARY KEY,
                guild_id    INTEGER NOT NULL,
                coins       INTEGER DEFAULT 0,
                xp          INTEGER DEFAULT 0,
                level       INTEGER DEFAULT 1,
                warnings    INTEGER DEFAULT 0,
                joined_at   TEXT    DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS warnings (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                guild_id    INTEGER NOT NULL,
                mod_id      INTEGER NOT NULL,
                reason      TEXT    NOT NULL,
                created_at  TEXT    DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS guild_config (
                guild_id        INTEGER PRIMARY KEY,
                prefix          TEXT    DEFAULT '!',
                log_channel     INTEGER,
                welcome_channel INTEGER,
                mute_role       INTEGER,
                level_up_msg    INTEGER DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS tickets (
                ticket_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                guild_id    INTEGER NOT NULL,
                channel_id  INTEGER,
                status      TEXT    DEFAULT 'open',
                created_at  TEXT    DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        logger.info("✅ SQLite database initialized.")

    def execute(self, sql: str, params: tuple = ()) -> sqlite3.Cursor:
        conn = self.connect()
        cursor = conn.execute(sql, params)
        conn.commit()
        return cursor

    def executemany(self, sql: str, params_list: list) -> None:
        conn = self.connect()
        conn.executemany(sql, params_list)
        conn.commit()

    def fetchone(self, sql: str, params: tuple = ()) -> Optional[sqlite3.Row]:
        conn = self.connect()
        return conn.execute(sql, params).fetchone()

    def fetchall(self, sql: str, params: tuple = ()) -> List[sqlite3.Row]:
        conn = self.connect()
        return conn.execute(sql, params).fetchall()

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None

# Singleton instance — import and use anywhere
db = Database()


# =============================================================================
# §05 PERMS — Permission Helpers, Role Guards
# =============================================================================
# GUIDE: Use these as decorators on slash commands or call them inside commands.

def is_owner():
    """Check decorator: only the bot owner (OWNER_ID in .env) can run this."""
    async def predicate(interaction: discord.Interaction) -> bool:
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("❌ Owner only.", ephemeral=True)
            return False
        return True
    return app_commands.check(predicate)

def has_any_role(*role_names: str):
    """
    Check decorator: user must have at least one of the named roles.

    Usage:
        @bot.tree.command()
        @has_any_role("Moderator", "Admin")
        async def cmd(inter): ...
    """
    async def predicate(interaction: discord.Interaction) -> bool:
        if not interaction.guild:
            return False
        user_roles = {r.name for r in interaction.user.roles}
        if not user_roles.intersection(set(role_names)):
            await interaction.response.send_message(
                f"❌ You need one of these roles: {', '.join(role_names)}", ephemeral=True
            )
            return False
        return True
    return app_commands.check(predicate)

def has_role_id(role_id: int):
    """Check decorator: user must have a specific role by ID."""
    async def predicate(interaction: discord.Interaction) -> bool:
        if not interaction.guild:
            return False
        if not any(r.id == role_id for r in interaction.user.roles):
            await interaction.response.send_message("❌ Missing required role.", ephemeral=True)
            return False
        return True
    return app_commands.check(predicate)

def guild_only():
    """Check decorator: command cannot be used in DMs."""
    async def predicate(interaction: discord.Interaction) -> bool:
        if not interaction.guild:
            await interaction.response.send_message("❌ Server only.", ephemeral=True)
            return False
        return True
    return app_commands.check(predicate)

async def safe_respond(interaction: discord.Interaction, content: str = None, embed: discord.Embed = None, ephemeral: bool = False):
    """
    GUIDE: Use this instead of manually checking interaction.response.is_done().
    Handles both fresh interactions and already-responded interactions gracefully.
    """
    kwargs = {"ephemeral": ephemeral}
    if content:
        kwargs["content"] = content
    if embed:
        kwargs["embed"] = embed
    try:
        if interaction.response.is_done():
            await interaction.followup.send(**kwargs)
        else:
            await interaction.response.send_message(**kwargs)
    except discord.NotFound:
        pass  # Interaction expired — silently ignore


# =============================================================================
# §06 COOLDOWN — Custom Cooldown Buckets, Decorators
# =============================================================================
# GUIDE: discord.py has built-in cooldowns but they don't work well with
# slash commands. Use this custom cooldown manager for full control.

class CooldownManager:
    """
    Manual per-user cooldown tracker.
    
    Usage:
        cd = CooldownManager()
        
        @bot.tree.command()
        async def cmd(inter):
            remaining = cd.check(inter.user.id, "daily", cooldown_seconds=86400)
            if remaining > 0:
                return await inter.response.send_message(f"Cooldown: {remaining:.0f}s left")
            cd.reset(inter.user.id, "daily")
            # ... do stuff
    """
    def __init__(self):
        self._store: Dict[str, float] = {}  # key -> last_used_timestamp

    def _key(self, user_id: int, bucket: str) -> str:
        return f"{user_id}:{bucket}"

    def check(self, user_id: int, bucket: str, cooldown_seconds: float) -> float:
        """Returns remaining seconds if on cooldown, else 0."""
        key = self._key(user_id, bucket)
        last = self._store.get(key, 0)
        elapsed = time.time() - last
        remaining = cooldown_seconds - elapsed
        return max(0.0, remaining)

    def reset(self, user_id: int, bucket: str):
        """Stamp the cooldown (call after the user successfully uses the command)."""
        self._store[self._key(user_id, bucket)] = time.time()

    def clear(self, user_id: int, bucket: str):
        """Forcibly clear a user's cooldown (admin override)."""
        self._store.pop(self._key(user_id, bucket), None)

cooldowns = CooldownManager()

def format_remaining(seconds: float) -> str:
    """Convert remaining seconds to human-readable string. '2h 30m', '45s' etc."""
    if seconds < 60:
        return f"{seconds:.0f}s"
    if seconds < 3600:
        return f"{seconds/60:.0f}m {seconds%60:.0f}s"
    hours = seconds // 3600
    mins  = (seconds % 3600) // 60
    return f"{hours:.0f}h {mins:.0f}m"


# =============================================================================
# §07 EMBEDS — Embed Library
# =============================================================================
# GUIDE: All embed creation goes through these helpers for consistency.
# Never construct embeds ad-hoc in commands — use or extend these builders.

class EmbedBuilder:
    """
    Complete embed factory. All methods return discord.Embed.
    
    Quickstart:
        await inter.response.send_message(embed=EmbedBuilder.success("Done!", "Your item was saved."))
        await inter.response.send_message(embed=EmbedBuilder.error("Failed", "Could not find that user."))
        await inter.response.send_message(embed=EmbedBuilder.info("Profile", "John", fields=[("Level", "5", True)]))
    """

    @staticmethod
    def base(title: str = None, description: str = None, color: int = EMBED_COLOR_DEFAULT) -> discord.Embed:
        embed = discord.Embed(title=title, description=description, color=color, timestamp=discord.utils.utcnow())
        embed.set_footer(text="Master Bot Reference")
        return embed

    @staticmethod
    def success(title: str, description: str = "") -> discord.Embed:
        return EmbedBuilder.base(f"✅ {title}", description, EMBED_COLOR_SUCCESS)

    @staticmethod
    def error(title: str, description: str = "") -> discord.Embed:
        return EmbedBuilder.base(f"❌ {title}", description, EMBED_COLOR_ERROR)

    @staticmethod
    def warning(title: str, description: str = "") -> discord.Embed:
        return EmbedBuilder.base(f"⚠️ {title}", description, EMBED_COLOR_WARNING)

    @staticmethod
    def info(
        title: str,
        description: str = "",
        fields: List[Tuple[str, str, bool]] = None,
        thumbnail_url: str = None,
        image_url: str = None,
        author_name: str = None,
        author_icon: str = None,
        color: int = EMBED_COLOR_DEFAULT,
    ) -> discord.Embed:
        """
        Full-featured embed builder.
        fields: list of (name, value, inline) tuples
        """
        embed = EmbedBuilder.base(title, description, color)
        if fields:
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
        if thumbnail_url:
            embed.set_thumbnail(url=thumbnail_url)
        if image_url:
            embed.set_image(url=image_url)
        if author_name:
            embed.set_author(name=author_name, icon_url=author_icon)
        return embed

    @staticmethod
    def boxed(title: str, description: str, color: int = EMBED_COLOR_DEFAULT) -> discord.Embed:
        """Embed with ASCII box around description text (decorative style)."""
        width = 36
        top    = f"╔{'═'*width}╗"
        bottom = f"╚{'═'*width}╝"
        lines  = textwrap.wrap(description, width - 2)
        body   = "\n".join(f"║ {line:<{width-2}} ║" for line in lines)
        box    = f"```\n{top}\n{body}\n{bottom}\n```"
        return EmbedBuilder.base(title, box, color)

    @staticmethod
    def user_card(member: discord.Member) -> discord.Embed:
        """Ready-made user profile card embed."""
        embed = EmbedBuilder.base(f"👤 {member.display_name}", color=EMBED_COLOR_DEFAULT)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Username",    value=str(member),                                 inline=True)
        embed.add_field(name="ID",          value=str(member.id),                              inline=True)
        embed.add_field(name="Joined Server",value=discord.utils.format_dt(member.joined_at, "R") if member.joined_at else "Unknown", inline=True)
        embed.add_field(name="Account Age", value=discord.utils.format_dt(member.created_at, "R"),inline=True)
        top_role = member.top_role
        embed.add_field(name="Top Role",    value=top_role.mention if top_role != member.guild.default_role else "None", inline=True)
        embed.add_field(name="Bot?",        value="Yes" if member.bot else "No",               inline=True)
        return embed

    @staticmethod
    def leaderboard(title: str, entries: List[Tuple[str, str]], color: int = EMBED_COLOR_GOLD) -> discord.Embed:
        """
        Leaderboard embed.
        entries: list of (name_str, value_str) — will be numbered 1..N automatically.
        """
        medals = ["🥇", "🥈", "🥉"]
        lines = []
        for i, (name, value) in enumerate(entries):
            prefix = medals[i] if i < 3 else f"`{i+1}.`"
            lines.append(f"{prefix} **{name}** — {value}")
        embed = EmbedBuilder.base(f"🏆 {title}", "\n".join(lines) or "No entries.", color)
        return embed


# =============================================================================
# §08 UI-BTN — Button Views
# =============================================================================

# ─── A. Basic Restricted View (owner-only interaction) ────────────────────────
class RestrictedView(View):
    """
    GUIDE: Restricts all button interactions to the user who summoned the view.
    Inherit from this instead of View for all user-facing menus.
    
    Usage:
        view = RestrictedView(inter.user.id, timeout=120)
        view.add_item(...)
        await inter.response.send_message(embed=..., view=view)
    """
    def __init__(self, owner_id: int, timeout: float = 300.0):
        super().__init__(timeout=timeout)
        self.owner_id = owner_id
        self.message: Optional[discord.Message] = None  # Store message ref to edit on timeout

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message("❌ This menu isn't yours!", ephemeral=True)
            return False
        return True

    async def on_timeout(self):
        """Automatically disable all components when the view expires."""
        for child in self.children:
            child.disabled = True
        if self.message:
            try:
                await self.message.edit(content="*Menu expired.*", view=self)
            except (discord.NotFound, discord.HTTPException):
                pass


# ─── B. Accept/Decline View ───────────────────────────────────────────────────
class AcceptDeclineView(RestrictedView):
    """
    GUIDE: Simple two-button confirmation. Result is stored in self.accepted.
    Use with asyncio.wait_for or the ConfirmationDialog helper (§12).
    
    Usage:
        view = AcceptDeclineView(inter.user.id)
        msg = await inter.response.send_message("Continue?", view=view)
        view.message = await inter.original_response()
        await view.wait()  # blocks until button clicked or timeout
        if view.accepted:
            ...
    """
    def __init__(self, owner_id: int, timeout: float = 60.0):
        super().__init__(owner_id, timeout)
        self.accepted: Optional[bool] = None

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.success, emoji="✅")
    async def btn_accept(self, interaction: discord.Interaction, button: Button):
        self.accepted = True
        self.stop()
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(content="✅ Accepted.", view=self)

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.danger, emoji="❌")
    async def btn_decline(self, interaction: discord.Interaction, button: Button):
        self.accepted = False
        self.stop()
        await interaction.response.edit_message(content="❌ Declined.", view=None)


# ─── C. Toggle Button View ────────────────────────────────────────────────────
class ToggleView(RestrictedView):
    """
    GUIDE: A button that switches label/style/state on each click.
    
    Usage:
        view = ToggleView(inter.user.id, initial_state=False)
        await inter.response.send_message("Feature is OFF", view=view)
    """
    def __init__(self, owner_id: int, initial_state: bool = False, timeout: float = 300.0):
        super().__init__(owner_id, timeout)
        self.state = initial_state
        self._update_button()

    def _update_button(self):
        btn = self.btn_toggle
        if self.state:
            btn.label = "ON"
            btn.style = discord.ButtonStyle.success
            btn.emoji = "🟢"
        else:
            btn.label = "OFF"
            btn.style = discord.ButtonStyle.secondary
            btn.emoji = "🔴"

    @discord.ui.button(label="OFF", style=discord.ButtonStyle.secondary, emoji="🔴")
    async def btn_toggle(self, interaction: discord.Interaction, button: Button):
        self.state = not self.state
        self._update_button()
        status = "ON" if self.state else "OFF"
        await interaction.response.edit_message(content=f"Feature is **{status}**", view=self)


# ─── D. Link Button View (no callback needed) ─────────────────────────────────
def make_link_view(*links: Tuple[str, str]) -> View:
    """
    GUIDE: Creates a view with non-interactive URL buttons.
    Links are (label, url) tuples. Max 5 per row.
    
    Usage:
        view = make_link_view(("GitHub", "https://github.com"), ("Docs", "https://docs.example.com"))
        await inter.response.send_message("Check these out!", view=view)
    """
    view = View()
    for label, url in links:
        view.add_item(Button(label=label, url=url, style=discord.ButtonStyle.link))
    return view


# ─── E. Multi-Row Dynamic Button Grid ─────────────────────────────────────────
class DynamicButtonGrid(RestrictedView):
    """
    GUIDE: Programmatically add buttons from a list. Useful for menus where
    the options are defined at runtime (e.g., from database).
    Max 25 buttons (5 rows × 5 cols).
    
    Usage:
        options = [("Option A", "a"), ("Option B", "b"), ("Option C", "c")]
        view = DynamicButtonGrid(inter.user.id, options)
        view.message = await inter.response.send_message("Pick:", view=view, wait=True)
        # view.chosen_value set after click
    """
    def __init__(self, owner_id: int, options: List[Tuple[str, str]], timeout: float = 60.0):
        super().__init__(owner_id, timeout)
        self.chosen_value: Optional[str] = None
        for i, (label, value) in enumerate(options[:25]):
            row = i // 5
            btn = Button(label=label, custom_id=f"dyn_{value}", row=row)
            btn.callback = self._make_callback(value)
            self.add_item(btn)

    def _make_callback(self, value: str):
        async def callback(interaction: discord.Interaction):
            self.chosen_value = value
            self.stop()
            for child in self.children:
                child.disabled = True
            await interaction.response.edit_message(content=f"Selected: **{value}**", view=self)
        return callback


# =============================================================================
# §09 UI-MODAL — Modals
# =============================================================================
# GUIDE: Modals are popup forms. Rules:
#   1. Must be the FIRST response to an interaction (cannot defer first).
#   2. Max 5 fields per modal.
#   3. Fields must be TextInput — no other component type is allowed.

# ─── A. Single-Field Quick Modal ──────────────────────────────────────────────
class QuickInputModal(Modal):
    """
    GUIDE: One-liner modal for a single text input.
    
    Usage:
        async def callback(interaction, value):
            await interaction.response.send_message(f"You said: {value}")
        
        await inter.response.send_modal(QuickInputModal("Enter Name", "Your Name", callback))
    """
    answer = TextInput(label="Input", placeholder="Type here...", max_length=500)

    def __init__(self, modal_title: str, field_label: str, callback: Callable):
        super().__init__(title=modal_title)
        self.answer.label = field_label
        self._cb = callback

    async def on_submit(self, interaction: discord.Interaction):
        await self._cb(interaction, self.answer.value)

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        logger.error(f"Modal error: {error}")
        await interaction.response.send_message("❌ Modal error.", ephemeral=True)


# ─── B. Full Multi-Field Config Modal ─────────────────────────────────────────
class ConfigModal(Modal, title="⚙️ Configure Bot Settings"):
    """
    GUIDE: Full 5-field modal template. Copy and rename fields as needed.
    Each TextInput is a class variable — set defaults in __init__.
    """
    field_name = TextInput(
        label="Setting Name",
        placeholder="e.g., Welcome Channel Name",
        required=True,
        max_length=50,
    )
    field_value = TextInput(
        label="Setting Value",
        placeholder="e.g., #general",
        required=True,
        max_length=200,
    )
    field_description = TextInput(
        label="Description (optional)",
        style=discord.TextStyle.paragraph,
        placeholder="Describe what this setting does...",
        required=False,
        max_length=1000,
    )

    def __init__(self, existing_name: str = "", existing_value: str = ""):
        super().__init__()
        # Pre-fill with existing data
        if existing_name:
            self.field_name.default = existing_name
        if existing_value:
            self.field_value.default = existing_value

    async def on_submit(self, interaction: discord.Interaction):
        name  = self.field_name.value
        value = self.field_value.value
        desc  = self.field_description.value or "No description."
        embed = EmbedBuilder.success("Settings Saved", f"**{name}**: {value}\n\n*{desc}*")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        logger.error(f"ConfigModal error: {traceback.format_exc()}")
        await safe_respond(interaction, "❌ Something went wrong.", ephemeral=True)


# ─── C. Chained / Multi-Step Modal Flow ───────────────────────────────────────
# GUIDE: Discord doesn't allow sending Modal-from-Modal directly.
# Use a button inside a view to send the next modal instead.
# Pattern: Modal1.on_submit → send a View with "Next Step" button → button triggers Modal2

class StepOneModal(Modal, title="Step 1: Basic Info"):
    name  = TextInput(label="Character Name", max_length=50, required=True)
    race  = TextInput(label="Race",           max_length=30, required=True)

    async def on_submit(self, interaction: discord.Interaction):
        # Store partial data then show step 2 as a button
        view = _StepTwoTrigger(self.name.value, self.race.value)
        await interaction.response.send_message(
            f"Step 1 saved. Click **Next** for step 2.", view=view, ephemeral=True
        )

class StepTwoModal(Modal, title="Step 2: Stats"):
    def __init__(self, name: str, race: str):
        super().__init__()
        self._name = name
        self._race = race

    stats  = TextInput(label="Stat Block (STR/DEX/CON...)", max_length=100, required=True)
    backstory = TextInput(label="Backstory", style=discord.TextStyle.paragraph, required=False)

    async def on_submit(self, interaction: discord.Interaction):
        embed = EmbedBuilder.success(
            "Character Created!",
            f"**Name:** {self._name}\n**Race:** {self._race}\n**Stats:** {self.stats.value}"
        )
        await interaction.response.send_message(embed=embed)

class _StepTwoTrigger(View):
    def __init__(self, name: str, race: str):
        super().__init__(timeout=120)
        self._name = name
        self._race = race

    @discord.ui.button(label="Next Step →", style=discord.ButtonStyle.primary)
    async def next(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(StepTwoModal(self._name, self._race))


# =============================================================================
# §10 UI-SELECT — Select Menus
# =============================================================================

# ─── A. String Select ─────────────────────────────────────────────────────────
class StringSelectView(RestrictedView):
    """
    GUIDE: User picks from a list of text options.
    Max 25 options. Set max_values > 1 for multi-select.
    
    Usage:
        options = [("Warrior", "warrior", "Frontline fighter", "⚔️"), ...]
        view = StringSelectView(inter.user.id, options)
        await inter.response.send_message("Choose your class:", view=view)
    """
    def __init__(self, owner_id: int, options: List[Tuple[str, str, str, str]], timeout: float = 60.0):
        super().__init__(owner_id, timeout)
        self.chosen: Optional[str] = None
        select_options = [
            discord.SelectOption(label=label, value=value, description=desc, emoji=emoji)
            for label, value, desc, emoji in options[:25]
        ]
        sel = Select(
            placeholder="Choose an option...",
            min_values=1,
            max_values=1,
            options=select_options,
        )
        sel.callback = self._callback
        self.add_item(sel)

    async def _callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.owner_id:
            return await interaction.response.send_message("Not your menu!", ephemeral=True)
        self.chosen = interaction.data["values"][0]
        self.stop()
        await interaction.response.edit_message(content=f"Selected: **{self.chosen}**", view=None)


# ─── B. Role Select ───────────────────────────────────────────────────────────
class RoleSelectView(RestrictedView):
    """
    GUIDE: Shows Discord's native role picker. No manual option building needed.
    User can pick 1-N roles from the server's role list.
    
    Usage:
        view = RoleSelectView(inter.user.id, max_roles=2)
        await inter.response.send_message("Pick roles:", view=view)
        await view.wait()
        chosen_roles = view.chosen_roles  # list of discord.Role
    """
    def __init__(self, owner_id: int, max_roles: int = 1, timeout: float = 60.0):
        super().__init__(owner_id, timeout)
        self.chosen_roles: List[discord.Role] = []
        sel = RoleSelect(placeholder="Select role(s)...", min_values=1, max_values=max_roles)
        sel.callback = self._callback
        self.add_item(sel)

    async def _callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.owner_id:
            return await interaction.response.send_message("Not your menu!", ephemeral=True)
        self.chosen_roles = interaction.data["values"]  # list of role IDs as strings
        self.stop()
        await interaction.response.edit_message(content=f"Roles selected ✅", view=None)


# ─── C. Channel Select ────────────────────────────────────────────────────────
class ChannelSelectView(RestrictedView):
    """
    GUIDE: Native channel picker. Filter by channel type.
    
    Usage:
        view = ChannelSelectView(inter.user.id, channel_types=[discord.ChannelType.text])
        await inter.response.send_message("Pick a channel:", view=view)
        await view.wait()
        channel_id = view.chosen_channel_id
    """
    def __init__(self, owner_id: int, channel_types: List[discord.ChannelType] = None, timeout: float = 60.0):
        super().__init__(owner_id, timeout)
        self.chosen_channel_id: Optional[int] = None
        kwargs = {"placeholder": "Select a channel..."}
        if channel_types:
            kwargs["channel_types"] = channel_types
        sel = ChannelSelect(**kwargs)
        sel.callback = self._callback
        self.add_item(sel)

    async def _callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.owner_id:
            return await interaction.response.send_message("Not your menu!", ephemeral=True)
        values = interaction.data.get("values", [])
        self.chosen_channel_id = int(values[0]) if values else None
        self.stop()
        await interaction.response.edit_message(content="Channel selected ✅", view=None)


# ─── D. User Select ───────────────────────────────────────────────────────────
class UserSelectView(RestrictedView):
    """GUIDE: Native user picker. Lets user pick server members."""
    def __init__(self, owner_id: int, max_users: int = 1, timeout: float = 60.0):
        super().__init__(owner_id, timeout)
        self.chosen_user_ids: List[int] = []
        sel = UserSelect(placeholder="Select user(s)...", min_values=1, max_values=max_users)
        sel.callback = self._callback
        self.add_item(sel)

    async def _callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.owner_id:
            return await interaction.response.send_message("Not your menu!", ephemeral=True)
        self.chosen_user_ids = [int(v) for v in interaction.data.get("values", [])]
        self.stop()
        await interaction.response.edit_message(content=f"User(s) selected ✅", view=None)


# =============================================================================
# §11 UI-PAGE — Paginator
# =============================================================================

class Paginator(RestrictedView):
    """
    GUIDE: Multi-page embed navigator. Handles any list of data.
    
    Usage:
        pages = ["Page 1 content", "Page 2 content", "Page 3 content"]
        pager = Paginator(inter.user.id, pages, title="My List", per_page=1)
        await inter.response.send_message(embed=pager.get_embed(), view=pager)
    
    Advanced: Pass a list of discord.Embed directly as `pages` for full control.
    """
    def __init__(
        self,
        owner_id: int,
        pages: List[Any],
        title: str = "Results",
        per_page: int = 10,
        timeout: float = 300.0,
        color: int = EMBED_COLOR_DEFAULT,
    ):
        super().__init__(owner_id, timeout)
        self.title    = title
        self.color    = color
        self.per_page = per_page

        # Support either raw strings or pre-built embeds
        if pages and isinstance(pages[0], discord.Embed):
            self.embed_pages = pages
            self.raw_pages   = None
        else:
            self.raw_pages   = [str(p) for p in pages]
            total = math.ceil(len(self.raw_pages) / per_page)
            self.embed_pages = self._build_embed_pages(total)

        self.current = 0
        self._update_buttons()

    def _build_embed_pages(self, total: int) -> List[discord.Embed]:
        pages = []
        for i in range(total):
            chunk = self.raw_pages[i * self.per_page : (i + 1) * self.per_page]
            content = "\n".join(f"`{i*self.per_page+j+1}.` {item}" for j, item in enumerate(chunk))
            embed = EmbedBuilder.base(self.title, content, self.color)
            embed.set_footer(text=f"Page {i+1}/{total} • {len(self.raw_pages)} items")
            pages.append(embed)
        return pages or [EmbedBuilder.base(self.title, "*No results.*", self.color)]

    def get_embed(self) -> discord.Embed:
        return self.embed_pages[self.current]

    def _update_buttons(self):
        total = len(self.embed_pages)
        self.btn_first.disabled    = self.current == 0
        self.btn_prev.disabled     = self.current == 0
        self.btn_next.disabled     = self.current >= total - 1
        self.btn_last.disabled     = self.current >= total - 1
        self.btn_page_info.label   = f"{self.current+1}/{total}"

    @discord.ui.button(emoji="⏮️", style=discord.ButtonStyle.secondary, row=0)
    async def btn_first(self, interaction: discord.Interaction, button: Button):
        self.current = 0
        self._update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @discord.ui.button(emoji="◀️", style=discord.ButtonStyle.secondary, row=0)
    async def btn_prev(self, interaction: discord.Interaction, button: Button):
        self.current = max(0, self.current - 1)
        self._update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @discord.ui.button(label="1/1", style=discord.ButtonStyle.primary, disabled=True, row=0)
    async def btn_page_info(self, interaction: discord.Interaction, button: Button):
        pass  # Static display label — no action

    @discord.ui.button(emoji="▶️", style=discord.ButtonStyle.secondary, row=0)
    async def btn_next(self, interaction: discord.Interaction, button: Button):
        self.current = min(len(self.embed_pages) - 1, self.current + 1)
        self._update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @discord.ui.button(emoji="⏭️", style=discord.ButtonStyle.secondary, row=0)
    async def btn_last(self, interaction: discord.Interaction, button: Button):
        self.current = len(self.embed_pages) - 1
        self._update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)


# =============================================================================
# §12 UI-CONF — Confirmation Dialog Helper
# =============================================================================

async def confirm(
    interaction: discord.Interaction,
    prompt: str = "Are you sure?",
    timeout: float = 30.0,
    ephemeral: bool = True,
) -> bool:
    """
    GUIDE: Drop-in confirmation prompt. Returns True if confirmed, False otherwise.
    Handles the entire interaction flow internally.
    
    Usage:
        confirmed = await confirm(inter, "This will delete your data. Continue?")
        if not confirmed:
            return
        # proceed with deletion
    """
    view = AcceptDeclineView(interaction.user.id, timeout=timeout)
    embed = EmbedBuilder.warning("Confirmation Required", prompt)
    await interaction.response.send_message(embed=embed, view=view, ephemeral=ephemeral)
    view.message = await interaction.original_response()
    await view.wait()
    return view.accepted is True


# =============================================================================
# §13 UI-PERSIST — Persistent Views (survive bot restarts)
# =============================================================================
# GUIDE: Normal views die when the bot restarts. Persistent views survive.
# Rules:
#   1. Every Button/Select in the view MUST have a unique, hardcoded custom_id.
#   2. Register the view with bot.add_view(MyPersistentView()) in setup_hook.
#   3. Do NOT set a timeout (pass timeout=None).
#   4. Store the message ID so you can re-attach if needed.

class PersistentRoleButton(View):
    """
    GUIDE: Persistent button for self-assignable roles.
    Register in setup_hook:
        bot.add_view(PersistentRoleButton(role_id=123456789))
    
    Send with:
        await channel.send("Click to get the role!", view=PersistentRoleButton(role_id=...))
    """
    def __init__(self, role_id: int):
        super().__init__(timeout=None)  # MUST be None for persistence
        self.role_id = role_id
        # custom_id MUST be hardcoded (not dynamic) and globally unique
        self.btn.custom_id = f"persist_role_{role_id}"

    @discord.ui.button(label="Toggle Role", style=discord.ButtonStyle.primary, emoji="🎭", custom_id="persist_role_placeholder")
    async def btn(self, interaction: discord.Interaction, button: Button):
        if not interaction.guild:
            return
        role = interaction.guild.get_role(self.role_id)
        if not role:
            return await interaction.response.send_message("❌ Role not found.", ephemeral=True)
        member = interaction.user
        if role in member.roles:
            await member.remove_roles(role, reason="Self-role toggle")
            await interaction.response.send_message(f"✅ Removed **{role.name}**.", ephemeral=True)
        else:
            await member.add_roles(role, reason="Self-role toggle")
            await interaction.response.send_message(f"✅ Gave you **{role.name}**.", ephemeral=True)


# =============================================================================
# §14 CTX-MENU — Context Menus (right-click on users/messages)
# =============================================================================
# GUIDE: Context menus appear when you right-click a user or message in Discord.
# They live under Apps > [YourBotName] in the context menu.
# Must be registered just like slash commands (via tree.sync()).

# Right-click a USER
# @bot.tree.context_menu(name="View Profile")
# async def ctx_view_profile(interaction: discord.Interaction, member: discord.Member):
#     embed = EmbedBuilder.user_card(member)
#     await interaction.response.send_message(embed=embed, ephemeral=True)

# Right-click a MESSAGE
# @bot.tree.context_menu(name="Bookmark Message")
# async def ctx_bookmark(interaction: discord.Interaction, message: discord.Message):
#     try:
#         embed = EmbedBuilder.info(
#             "📌 Bookmarked Message",
#             message.content[:2000] or "*[no text content]*",
#             fields=[
#                 ("Author", message.author.mention, True),
#                 ("Channel", message.channel.mention, True),
#                 ("Link", f"[Jump]({message.jump_url})", True),
#             ]
#         )
#         await interaction.user.send(embed=embed)
#         await interaction.response.send_message("📌 Bookmarked to your DMs!", ephemeral=True)
#     except discord.Forbidden:
#         await interaction.response.send_message("❌ I can't DM you. Check your DM settings.", ephemeral=True)

# NOTE: Context menu functions are commented out so they don't register at
# module import time. Uncomment and attach to your bot instance in §15.


# =============================================================================
# §15 BOT-CLASS — Bot Class, setup_hook, Cog loading, Status Rotation
# =============================================================================

# Status rotation pool
STATUS_ROTATION = [
    discord.Game("with slash commands"),
    discord.Activity(type=discord.ActivityType.watching,  name="the server"),
    discord.Activity(type=discord.ActivityType.listening, name="your commands"),
    discord.Streaming(name="Discord Bot Dev", url="https://twitch.tv/discord"),
]

class MasterBot(commands.Bot):
    """
    GUIDE: Main bot class. Inheriting from commands.Bot gives you:
      - self.tree (app_commands.CommandTree) — slash commands
      - self.cogs — loaded cog modules
      - Full event system
      - @tasks.loop integration
    """
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents, help_command=None)
        self.db = db
        self.json_db_loaded = False
        self._status_index = 0

    async def setup_hook(self):
        """
        GUIDE: Runs ONCE on startup, before connecting to Discord gateway.
        This is the correct place to:
          - Load cogs
          - Register persistent views
          - Initialize database
          - Sync slash commands
        """
        # Initialize SQLite
        self.db.initialize()

        # Load JSON DB
        global BOT_DATABASE
        BOT_DATABASE = load_json_db()
        self.json_db_loaded = True
        logger.info("📂 JSON database loaded.")

        # Load all cogs (comment out any you haven't created yet)
        # for cog in ["cogs.moderation", "cogs.economy", "cogs.leveling"]:
        #     try:
        #         await self.load_extension(cog)
        #         logger.info(f"✅ Loaded cog: {cog}")
        #     except Exception as e:
        #         logger.error(f"❌ Failed to load cog {cog}: {e}")

        # Register persistent views (MUST match custom_ids in buttons)
        # self.add_view(PersistentRoleButton(role_id=YOUR_ROLE_ID))

        # Register context menus
        # self.tree.add_command(ctx_view_profile)
        # self.tree.add_command(ctx_bookmark)

        # Sync slash commands globally
        # WARNING: Global sync takes up to 1 hour to propagate.
        # For development, sync to a specific guild instantly:
        #   TEST_GUILD = discord.Object(id=YOUR_TEST_GUILD_ID)
        #   self.tree.copy_global_to(guild=TEST_GUILD)
        #   await self.tree.sync(guild=TEST_GUILD)
        await self.tree.sync()
        logger.info("✅ Slash commands synced globally.")

        # Start background tasks
        self.task_autosave.start()
        self.task_status_rotation.start()

    async def on_ready(self):
        logger.info(f"✅ Logged in as {self.user} (ID: {self.user.id})")
        logger.info(f"📊 Connected to {len(self.guilds)} guild(s)")
        logger.info(f"🏓 Latency: {round(self.latency * 1000)}ms")

    async def on_disconnect(self):
        logger.warning("⚡ Disconnected from Discord. Force saving...")
        if self.json_db_loaded:
            save_json_db(BOT_DATABASE)

    async def close(self):
        """Graceful shutdown: save data, close DB connections."""
        logger.info("🛑 Shutting down...")
        if self.json_db_loaded:
            save_json_db(BOT_DATABASE)
        self.db.close()
        await super().close()


# Create the single bot instance
bot = MasterBot()


# =============================================================================
# §16 BG-TASKS — Background Tasks
# =============================================================================
# GUIDE: Use @tasks.loop for anything that needs to run on a schedule.
# Always add a @task.before_loop to wait for the bot to be ready.
# Always cancel tasks in bot.close() if they hold resources.

@bot.task_autosave.before_loop if hasattr(bot, "task_autosave") else lambda f: f
async def _before_autosave():
    await bot.wait_until_ready()

# Define tasks on the bot instance so they can access `bot`
@tasks.loop(minutes=5)
async def _task_autosave():
    if bot.json_db_loaded:
        save_json_db(BOT_DATABASE)
        logger.debug("💾 Autosaved JSON DB.")

@tasks.loop(minutes=10)
async def _task_status_rotation():
    status = STATUS_ROTATION[bot._status_index % len(STATUS_ROTATION)]
    await bot.change_presence(activity=status)
    bot._status_index += 1

@tasks.loop(hours=24)
async def _task_daily_cleanup():
    """
    GUIDE: Example: daily cleanup task. Runs once every 24 hours.
    Use this for resetting daily streaks, clearing temp data, etc.
    """
    logger.info("🧹 Running daily cleanup...")
    # Example: reset "daily_claimed" flag for all users
    for key, val in BOT_DATABASE.items():
        if isinstance(val, dict) and "daily_claimed" in val:
            val["daily_claimed"] = False

# Attach tasks to bot class (workaround for defining tasks at module level)
MasterBot.task_autosave       = _task_autosave
MasterBot.task_status_rotation = _task_status_rotation
MasterBot.task_daily_cleanup  = _task_daily_cleanup

# Start before_loop hooks
_task_autosave.before_loop(lambda: bot.wait_until_ready())
_task_status_rotation.before_loop(lambda: bot.wait_until_ready())
_task_daily_cleanup.before_loop(lambda: bot.wait_until_ready())


# =============================================================================
# §17 ERR-HAND — Global Error Handler (all error types categorized)
# =============================================================================

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    """
    GUIDE: Catches ALL slash command errors globally.
    Add specific error types to the if-chain below for custom messages.
    """
    original = getattr(error, "original", error)
    logger.error(f"[CMD ERROR] /{interaction.command.name if interaction.command else '?'}: {original}")

    # ── Categorized error messages ─────────────────────────────────────────
    if isinstance(error, app_commands.MissingPermissions):
        msg = f"❌ You need: `{'`, `'.join(error.missing_permissions)}`"

    elif isinstance(error, app_commands.BotMissingPermissions):
        msg = f"❌ I need: `{'`, `'.join(error.missing_permissions)}`"

    elif isinstance(error, app_commands.CommandOnCooldown):
        msg = f"⏳ On cooldown. Try again in **{error.retry_after:.1f}s**."

    elif isinstance(error, app_commands.CheckFailure):
        # check() predicates (§05) raise this — they already sent a message
        return

    elif isinstance(error, app_commands.CommandNotFound):
        msg = "❓ Command not found."

    elif isinstance(original, discord.Forbidden):
        msg = "❌ I don't have permission to do that."

    elif isinstance(original, discord.NotFound):
        msg = "❌ Couldn't find that resource."

    elif isinstance(original, discord.HTTPException):
        msg = f"❌ Discord API error: `{original.status}` — `{original.text[:80]}`"

    elif isinstance(original, ValueError):
        msg = f"❌ Invalid value: {str(original)[:200]}"

    else:
        msg = f"❌ Unexpected error: `{str(original)[:150]}`"
        # Full traceback to log channel
        tb = traceback.format_exc()
        asyncio.create_task(send_log_to_channel(bot, "Unhandled Error", f"```{tb[:1800]}```", EMBED_COLOR_ERROR))

    await safe_respond(interaction, msg, ephemeral=True)


@bot.event
async def on_error(event: str, *args, **kwargs):
    """Catches errors in event listeners (not slash commands)."""
    logger.error(f"[EVENT ERROR] {event}:\n{traceback.format_exc()}")


# =============================================================================
# §18 CMD-PAT — Slash Command Patterns (A–J)
# =============================================================================

# ─── Pattern A: Basic deferred command ────────────────────────────────────────
@bot.tree.command(name="ping", description="Check bot latency.")
async def cmd_ping(inter: discord.Interaction):
    """
    GUIDE: Defer when your command takes > 3 seconds (API calls, DB queries).
    After deferring, use inter.followup.send() instead of inter.response.send_message().
    """
    await inter.response.defer()
    await asyncio.sleep(0.5)  # Simulate slow work
    latency = round(bot.latency * 1000)
    embed = EmbedBuilder.success("Pong!", f"Latency: **{latency}ms**")
    await inter.followup.send(embed=embed)


# ─── Pattern B: Typed args, choices, descriptions ─────────────────────────────
@bot.tree.command(name="roll", description="Roll dice.")
@app_commands.describe(
    sides="Number of sides on the die",
    count="How many dice to roll",
    secret="Only you can see the result",
)
@app_commands.choices(sides=[
    app_commands.Choice(name="d4",  value=4),
    app_commands.Choice(name="d6",  value=6),
    app_commands.Choice(name="d8",  value=8),
    app_commands.Choice(name="d10", value=10),
    app_commands.Choice(name="d12", value=12),
    app_commands.Choice(name="d20", value=20),
    app_commands.Choice(name="d100",value=100),
])
async def cmd_roll(inter: discord.Interaction, sides: int = 20, count: int = 1, secret: bool = False):
    count = max(1, min(20, count))
    rolls = [random.randint(1, sides) for _ in range(count)]
    total = sum(rolls)
    rolls_str = " + ".join(f"`{r}`" for r in rolls)
    embed = EmbedBuilder.info(
        f"🎲 {count}d{sides}",
        f"{rolls_str} = **{total}**",
        color=EMBED_COLOR_GOLD,
    )
    await inter.response.send_message(embed=embed, ephemeral=secret)


# ─── Pattern C: Autocomplete ──────────────────────────────────────────────────
_ITEM_DATABASE = ["Apple", "Banana", "Battleaxe", "Bandage", "Buckler", "Shield", "Sword", "Staff", "Spear"]

async def autocomplete_items(inter: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    """
    GUIDE: Autocomplete functions run on every keystroke.
    Keep them fast — no heavy DB calls. Cache results if needed.
    Return max 25 choices.
    """
    matches = [item for item in _ITEM_DATABASE if current.lower() in item.lower()]
    return [app_commands.Choice(name=m, value=m) for m in matches[:25]]

@bot.tree.command(name="lookup", description="Look up an item from the database.")
@app_commands.autocomplete(item_name=autocomplete_items)
@app_commands.describe(item_name="Start typing to search...")
async def cmd_lookup(inter: discord.Interaction, item_name: str):
    if item_name not in _ITEM_DATABASE:
        return await inter.response.send_message(f"❌ `{item_name}` not found.", ephemeral=True)
    embed = EmbedBuilder.info(f"📦 {item_name}", f"Details for **{item_name}**.")
    await inter.response.send_message(embed=embed)


# ─── Pattern D: Trigger Modal ─────────────────────────────────────────────────
@bot.tree.command(name="config", description="Open the configuration form.")
async def cmd_config(inter: discord.Interaction):
    """GUIDE: send_modal() CANNOT be called after defer(). It must be the first response."""
    await inter.response.send_modal(ConfigModal())


# ─── Pattern E: Trigger Paginator ─────────────────────────────────────────────
@bot.tree.command(name="itemlist", description="Show all items in the database.")
async def cmd_itemlist(inter: discord.Interaction):
    pager = Paginator(inter.user.id, _ITEM_DATABASE, title="📦 Item List", per_page=3)
    msg = await inter.response.send_message(embed=pager.get_embed(), view=pager)
    pager.message = await inter.original_response()


# ─── Pattern F: Admin-only with double permission check ───────────────────────
@bot.tree.command(name="admintest", description="Admin only test command.")
@app_commands.default_permissions(administrator=True)
async def cmd_admintest(inter: discord.Interaction):
    """
    GUIDE: @app_commands.default_permissions hides the command in Discord UI for non-admins.
    Always add a code-level check too, since permissions can be overridden server-side.
    """
    if not inter.user.guild_permissions.administrator:
        return await inter.response.send_message("❌ Nice try.", ephemeral=True)
    await inter.response.send_message("✅ Admin confirmed.", ephemeral=True)


# ─── Pattern G: Owner-only with custom check ──────────────────────────────────
@bot.tree.command(name="ownertest", description="Bot owner only.")
@is_owner()
async def cmd_ownertest(inter: discord.Interaction):
    await inter.response.send_message(f"👑 Hello, owner! Guilds: {len(bot.guilds)}", ephemeral=True)


# ─── Pattern H: Cooldown example ──────────────────────────────────────────────
@bot.tree.command(name="daily", description="Claim your daily reward.")
async def cmd_daily(inter: discord.Interaction):
    remaining = cooldowns.check(inter.user.id, "daily", cooldown_seconds=86400)
    if remaining > 0:
        return await inter.response.send_message(
            f"⏳ Daily cooldown: **{format_remaining(remaining)}** left.", ephemeral=True
        )
    cooldowns.reset(inter.user.id, "daily")
    reward = random.randint(50, 200)
    user_data = get_user_data(inter.user.id)
    user_data["coins"] = user_data.get("coins", 0) + reward
    save_json_db(BOT_DATABASE)
    embed = EmbedBuilder.success("Daily Reward!", f"You claimed **{reward} coins**! 💰")
    await inter.response.send_message(embed=embed)


# ─── Pattern I: Send file attachment ──────────────────────────────────────────
@bot.tree.command(name="export", description="Export data as a text file.")
async def cmd_export(inter: discord.Interaction):
    """GUIDE: Build a file in memory (no disk write needed) using BytesIO/StringIO."""
    await inter.response.defer(ephemeral=True)
    content = json.dumps(BOT_DATABASE, indent=2, ensure_ascii=False)
    file_obj = discord.File(StringIO(content), filename="database_export.json")
    await inter.followup.send("📄 Here's your export:", file=file_obj, ephemeral=True)


# ─── Pattern J: Multi-step workflow (confirm then act) ────────────────────────
@bot.tree.command(name="reset", description="Reset your profile data.")
async def cmd_reset(inter: discord.Interaction):
    confirmed = await confirm(inter, "This will erase ALL your data. This cannot be undone!")
    if not confirmed:
        return
    db_delete(user_key(inter.user.id), autosave=True)
    await inter.followup.send(embed=EmbedBuilder.success("Reset", "Your data has been wiped."), ephemeral=True)


# =============================================================================
# §19 CMD-GRP — Command Groups, Subcommand Groups
# =============================================================================
# GUIDE: Groups create commands like /group subcommand
# Nested groups create /group subgroup subcommand (2 levels deep max)

# ── Top-level group: /db ──────────────────────────────────────────────────────
db_group = app_commands.Group(name="db", description="Database management.")

@db_group.command(name="info", description="Show database statistics.")
async def db_info(inter: discord.Interaction):
    embed = EmbedBuilder.info(
        "📊 Database Info",
        f"JSON keys: **{len(BOT_DATABASE)}**\nSQLite path: `{SQL_FILE}`",
    )
    await inter.response.send_message(embed=embed, ephemeral=True)

@db_group.command(name="save", description="Force save database to disk.")
@app_commands.default_permissions(administrator=True)
async def db_save(inter: discord.Interaction):
    success = save_json_db(BOT_DATABASE)
    if success:
        await inter.response.send_message(embed=EmbedBuilder.success("Saved", "Database written to disk."), ephemeral=True)
    else:
        await inter.response.send_message(embed=EmbedBuilder.error("Failed", "Could not save."), ephemeral=True)

bot.tree.add_command(db_group)

# ── Nested subgroup: /char create, /char edit, /char view ────────────────────
char_group = app_commands.Group(name="char", description="Character management.")

@char_group.command(name="create", description="Start character creation wizard.")
async def char_create(inter: discord.Interaction):
    await inter.response.send_modal(StepOneModal())

@char_group.command(name="view", description="View your character sheet.")
async def char_view(inter: discord.Interaction):
    data = get_user_data(inter.user.id)
    char = data.get("character")
    if not char:
        return await inter.response.send_message("❌ No character found. Use `/char create`.", ephemeral=True)
    embed = EmbedBuilder.info(f"📜 {char.get('name', 'Unknown')}", str(char), color=EMBED_COLOR_GOLD)
    await inter.response.send_message(embed=embed)

bot.tree.add_command(char_group)


# =============================================================================
# §20 COG-SKEL — Cog Skeleton & Hot-reload Commands
# =============================================================================
# GUIDE: Cogs let you split your bot into separate files.
# File structure:
#   bot.py           ← main file (this reference)
#   cogs/
#     __init__.py    ← empty
#     moderation.py  ← ModCog
#     economy.py     ← EconomyCog
#
# In each cog file, define setup(bot) at the bottom:
#   async def setup(bot): await bot.add_cog(MyCog(bot))
#
# Load in setup_hook: await bot.load_extension("cogs.moderation")

class ExampleCog(commands.Cog, name="Example"):
    """
    GUIDE: Cog template. Copy to cogs/example.py, rename the class,
    and add your commands inside.
    """
    def __init__(self, bot: MasterBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"✅ Cog '{self.qualified_name}' ready.")

    @app_commands.command(name="cogtest", description="Test that this cog works.")
    async def cog_test(self, inter: discord.Interaction):
        await inter.response.send_message(f"✅ Cog `{self.qualified_name}` is active!", ephemeral=True)

# Hot-reload commands (owner-only) ────────────────────────────────────────────
cog_group = app_commands.Group(name="cog", description="Cog management (owner only).")

@cog_group.command(name="reload", description="Hot-reload a cog without restarting.")
@is_owner()
@app_commands.describe(name="The cog name (e.g. cogs.moderation)")
async def cog_reload(inter: discord.Interaction, name: str):
    try:
        await bot.reload_extension(name)
        await inter.response.send_message(f"✅ Reloaded `{name}`.", ephemeral=True)
    except Exception as e:
        await inter.response.send_message(f"❌ `{e}`", ephemeral=True)

@cog_group.command(name="load", description="Load a new cog.")
@is_owner()
async def cog_load(inter: discord.Interaction, name: str):
    try:
        await bot.load_extension(name)
        await inter.response.send_message(f"✅ Loaded `{name}`.", ephemeral=True)
    except Exception as e:
        await inter.response.send_message(f"❌ `{e}`", ephemeral=True)

@cog_group.command(name="unload", description="Unload a cog.")
@is_owner()
async def cog_unload(inter: discord.Interaction, name: str):
    try:
        await bot.unload_extension(name)
        await inter.response.send_message(f"✅ Unloaded `{name}`.", ephemeral=True)
    except Exception as e:
        await inter.response.send_message(f"❌ `{e}`", ephemeral=True)

@cog_group.command(name="list", description="List all loaded cogs.")
@is_owner()
async def cog_list(inter: discord.Interaction):
    cogs = "\n".join(f"• `{name}`" for name in bot.extensions) or "*No cogs loaded.*"
    await inter.response.send_message(cogs, ephemeral=True)

bot.tree.add_command(cog_group)


# =============================================================================
# §21 MOD-SYS — Skeleton: Moderation System
# =============================================================================
# GUIDE: Copy into cogs/moderation.py. Wire roles/channels via guild_config table.
# All actions write to the warnings table (§04 DB-SQL).

mod_group = app_commands.Group(name="mod", description="Moderation commands.", default_permissions=discord.Permissions(moderate_members=True))

@mod_group.command(name="warn", description="Issue a warning to a member.")
@app_commands.describe(member="The member to warn", reason="Reason for the warning")
async def mod_warn(inter: discord.Interaction, member: discord.Member, reason: str = "No reason provided."):
    if member.top_role >= inter.user.top_role and inter.user.id != OWNER_ID:
        return await inter.response.send_message("❌ Can't warn someone at or above your role.", ephemeral=True)
    if member.bot:
        return await inter.response.send_message("❌ Can't warn bots.", ephemeral=True)

    db.execute(
        "INSERT INTO warnings (user_id, guild_id, mod_id, reason) VALUES (?,?,?,?)",
        (member.id, inter.guild_id, inter.user.id, reason)
    )
    count_row = db.fetchone("SELECT COUNT(*) as cnt FROM warnings WHERE user_id=? AND guild_id=?", (member.id, inter.guild_id))
    count = count_row["cnt"] if count_row else 1

    embed = EmbedBuilder.warning(
        "Member Warned",
        f"{member.mention} has been warned.\n**Reason:** {reason}\n**Total Warnings:** {count}",
    )
    await inter.response.send_message(embed=embed)
    # DM the warned user
    try:
        dm_embed = EmbedBuilder.warning("You've been warned", f"**Server:** {inter.guild.name}\n**Reason:** {reason}")
        await member.send(embed=dm_embed)
    except discord.Forbidden:
        pass
    await send_log_to_channel(bot, "⚠️ Member Warned", f"{member.mention} warned by {inter.user.mention}\nReason: {reason}")

@mod_group.command(name="warnings", description="View a member's warning history.")
@app_commands.describe(member="The member to check")
async def mod_warnings(inter: discord.Interaction, member: discord.Member):
    rows = db.fetchall("SELECT reason, created_at, mod_id FROM warnings WHERE user_id=? AND guild_id=? ORDER BY created_at DESC", (member.id, inter.guild_id))
    if not rows:
        return await inter.response.send_message(f"✅ {member.mention} has no warnings.", ephemeral=True)
    entries = [f"`{i+1}.` {r['reason']} — <@{r['mod_id']}> @ {r['created_at'][:10]}" for i, r in enumerate(rows)]
    pager = Paginator(inter.user.id, entries, title=f"⚠️ Warnings for {member.display_name}", per_page=5)
    await inter.response.send_message(embed=pager.get_embed(), view=pager)
    pager.message = await inter.original_response()

@mod_group.command(name="clearwarns", description="Clear all warnings for a member.")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(member="The member to clear warnings for")
async def mod_clearwarns(inter: discord.Interaction, member: discord.Member):
    db.execute("DELETE FROM warnings WHERE user_id=? AND guild_id=?", (member.id, inter.guild_id))
    await inter.response.send_message(embed=EmbedBuilder.success("Cleared", f"All warnings removed for {member.mention}."))

@mod_group.command(name="kick", description="Kick a member from the server.")
@app_commands.describe(member="The member to kick", reason="Reason for kick")
async def mod_kick(inter: discord.Interaction, member: discord.Member, reason: str = "No reason."):
    if member.top_role >= inter.user.top_role and inter.user.id != OWNER_ID:
        return await inter.response.send_message("❌ Can't kick someone at or above your role.", ephemeral=True)
    try:
        await member.kick(reason=f"{inter.user}: {reason}")
    except discord.Forbidden:
        return await inter.response.send_message("❌ Missing kick permission.", ephemeral=True)
    embed = EmbedBuilder.error("Member Kicked", f"{member} was kicked.\n**Reason:** {reason}")
    await inter.response.send_message(embed=embed)
    await send_log_to_channel(bot, "👢 Member Kicked", f"{member} kicked by {inter.user.mention}\nReason: {reason}", EMBED_COLOR_WARNING)

@mod_group.command(name="ban", description="Ban a member from the server.")
@app_commands.describe(member="The member to ban", reason="Reason", delete_days="Days of messages to delete (0-7)")
async def mod_ban(inter: discord.Interaction, member: discord.Member, reason: str = "No reason.", delete_days: int = 0):
    if member.top_role >= inter.user.top_role and inter.user.id != OWNER_ID:
        return await inter.response.send_message("❌ Can't ban someone at or above your role.", ephemeral=True)
    confirmed = await confirm(inter, f"Ban **{member}**?\nReason: {reason}")
    if not confirmed:
        return
    try:
        await member.ban(reason=f"{inter.user}: {reason}", delete_message_days=max(0, min(7, delete_days)))
    except discord.Forbidden:
        return await inter.followup.send("❌ Missing ban permission.", ephemeral=True)
    await inter.followup.send(embed=EmbedBuilder.error("Member Banned", f"{member} has been banned.\nReason: {reason}"))
    await send_log_to_channel(bot, "🔨 Member Banned", f"{member} banned by {inter.user.mention}\nReason: {reason}", EMBED_COLOR_ERROR)

@mod_group.command(name="unban", description="Unban a user by ID.")
@app_commands.default_permissions(ban_members=True)
@app_commands.describe(user_id="The user's Discord ID")
async def mod_unban(inter: discord.Interaction, user_id: str):
    try:
        uid = int(user_id)
        user = await bot.fetch_user(uid)
        await inter.guild.unban(user, reason=f"Unbanned by {inter.user}")
        await inter.response.send_message(embed=EmbedBuilder.success("Unbanned", f"{user} has been unbanned."))
    except ValueError:
        await inter.response.send_message("❌ Invalid user ID.", ephemeral=True)
    except discord.NotFound:
        await inter.response.send_message("❌ User not found or not banned.", ephemeral=True)

@mod_group.command(name="purge", description="Bulk-delete messages in this channel.")
@app_commands.default_permissions(manage_messages=True)
@app_commands.describe(amount="Number of messages to delete (1-100)")
async def mod_purge(inter: discord.Interaction, amount: int = 10):
    amount = max(1, min(100, amount))
    confirmed = await confirm(inter, f"Delete **{amount}** messages from {inter.channel.mention}?")
    if not confirmed:
        return
    try:
        deleted = await inter.channel.purge(limit=amount, reason=f"Purge by {inter.user}")
        await inter.followup.send(embed=EmbedBuilder.success("Purged", f"Deleted **{len(deleted)}** messages."), ephemeral=True)
    except discord.Forbidden:
        await inter.followup.send("❌ Missing Manage Messages permission.", ephemeral=True)

@mod_group.command(name="timeout", description="Timeout (mute) a member.")
@app_commands.describe(member="The member", minutes="Duration in minutes", reason="Reason")
async def mod_timeout(inter: discord.Interaction, member: discord.Member, minutes: int = 10, reason: str = "No reason."):
    until = discord.utils.utcnow() + datetime.timedelta(minutes=minutes)
    try:
        await member.timeout(until, reason=reason)
    except discord.Forbidden:
        return await inter.response.send_message("❌ Missing Moderate Members permission.", ephemeral=True)
    embed = EmbedBuilder.warning("Member Timed Out", f"{member.mention} timed out for **{minutes}m**.\nReason: {reason}")
    await inter.response.send_message(embed=embed)

bot.tree.add_command(mod_group)


# =============================================================================
# §22 ECO-SYS — Skeleton: Economy System
# =============================================================================
# GUIDE: Uses JSON DB for simplicity. Swap get_user_data() calls to DB queries
# for production scale. All amounts stored as integers (coins).

eco_group = app_commands.Group(name="eco", description="Economy commands.")

def get_coins(user_id: int) -> int:
    return get_user_data(user_id).get("coins", 0)

def add_coins(user_id: int, amount: int) -> int:
    data = get_user_data(user_id)
    data["coins"] = max(0, data.get("coins", 0) + amount)
    save_json_db(BOT_DATABASE)
    return data["coins"]

def take_coins(user_id: int, amount: int) -> bool:
    """Returns False if user can't afford it."""
    data = get_user_data(user_id)
    if data.get("coins", 0) < amount:
        return False
    data["coins"] -= amount
    save_json_db(BOT_DATABASE)
    return True

@eco_group.command(name="balance", description="Check your coin balance.")
@app_commands.describe(member="Check another member's balance (optional)")
async def eco_balance(inter: discord.Interaction, member: discord.Member = None):
    target = member or inter.user
    coins  = get_coins(target.id)
    embed  = EmbedBuilder.info(f"💰 {target.display_name}'s Balance", f"**{coins:,} coins**", color=EMBED_COLOR_GOLD)
    await inter.response.send_message(embed=embed)

@eco_group.command(name="earn", description="Earn coins (cooldown: 1 hour).")
async def eco_earn(inter: discord.Interaction):
    remaining = cooldowns.check(inter.user.id, "earn", 3600)
    if remaining > 0:
        return await inter.response.send_message(f"⏳ Earn cooldown: **{format_remaining(remaining)}**", ephemeral=True)
    cooldowns.reset(inter.user.id, "earn")
    amount = random.randint(10, 100)
    new_bal = add_coins(inter.user.id, amount)
    embed = EmbedBuilder.success("Coins Earned!", f"+**{amount}** coins → Balance: **{new_bal:,}**")
    await inter.response.send_message(embed=embed)

@eco_group.command(name="pay", description="Send coins to another member.")
@app_commands.describe(member="Who to pay", amount="How many coins")
async def eco_pay(inter: discord.Interaction, member: discord.Member, amount: int):
    if member.id == inter.user.id:
        return await inter.response.send_message("❌ Can't pay yourself.", ephemeral=True)
    if amount <= 0:
        return await inter.response.send_message("❌ Amount must be positive.", ephemeral=True)
    if not take_coins(inter.user.id, amount):
        return await inter.response.send_message("❌ Insufficient coins.", ephemeral=True)
    add_coins(member.id, amount)
    embed = EmbedBuilder.success("Payment Sent!", f"Sent **{amount:,} coins** to {member.mention}.")
    await inter.response.send_message(embed=embed)

@eco_group.command(name="leaderboard", description="Top richest members.")
async def eco_leaderboard(inter: discord.Interaction):
    await inter.response.defer()
    users = [
        (k, v.get("coins", 0))
        for k, v in BOT_DATABASE.items()
        if k.startswith("user:") and isinstance(v, dict) and v.get("coins", 0) > 0
    ]
    users.sort(key=lambda x: x[1], reverse=True)
    entries = []
    for uid_key, coins in users[:10]:
        uid = int(uid_key.split(":")[1])
        user = bot.get_user(uid)
        name = user.display_name if user else f"User {uid}"
        entries.append((name, f"{coins:,} coins"))
    embed = EmbedBuilder.leaderboard("Economy Leaderboard", entries)
    await inter.followup.send(embed=embed)

# ── Shop skeleton ─────────────────────────────────────────────────────────────
SHOP_ITEMS = {
    "vip_role":   {"name": "VIP Role",   "price": 5000,  "description": "Get the VIP role."},
    "custom_nick":{"name": "Custom Nick","price": 1000,  "description": "Change your nickname."},
    "loot_box":   {"name": "Loot Box",   "price": 250,   "description": "Random reward 1x–5x price."},
}

@eco_group.command(name="shop", description="Browse the shop.")
async def eco_shop(inter: discord.Interaction):
    fields = [(v["name"], f"{v['price']:,} coins\n*{v['description']}*", True) for v in SHOP_ITEMS.values()]
    embed  = EmbedBuilder.info("🛒 Shop", "Use `/eco buy <item>` to purchase.", fields=fields, color=EMBED_COLOR_GOLD)
    await inter.response.send_message(embed=embed)

@eco_group.command(name="buy", description="Buy an item from the shop.")
@app_commands.describe(item="Item to purchase")
@app_commands.choices(item=[app_commands.Choice(name=v["name"], value=k) for k, v in SHOP_ITEMS.items()])
async def eco_buy(inter: discord.Interaction, item: str):
    shop_item = SHOP_ITEMS.get(item)
    if not shop_item:
        return await inter.response.send_message("❌ Item not found.", ephemeral=True)
    price = shop_item["price"]
    if not take_coins(inter.user.id, price):
        bal = get_coins(inter.user.id)
        return await inter.response.send_message(f"❌ Need {price:,} coins, you have {bal:,}.", ephemeral=True)
    # ── Item effect logic ───────────────────────────────────────────────────
    if item == "loot_box":
        reward = random.randint(price, price * 5)
        add_coins(inter.user.id, reward)
        await inter.response.send_message(embed=EmbedBuilder.success("Loot Box!", f"You won **{reward:,} coins**!"))
    else:
        # Add remaining item logic (role assignment, etc.)
        await inter.response.send_message(embed=EmbedBuilder.success("Purchased!", f"Bought **{shop_item['name']}**."))

bot.tree.add_command(eco_group)


# =============================================================================
# §23 TKT-SYS — Skeleton: Ticket System
# =============================================================================
# GUIDE: Creates private text channels for support tickets.
# Requires a "Tickets" category to exist. Set TICKET_CATEGORY_NAME below.
# Uses the tickets table in SQLite (§04 DB-SQL).

TICKET_CATEGORY_NAME = "Tickets"
TICKET_SUPPORT_ROLE  = "Support"  # Role that can see all tickets

ticket_group = app_commands.Group(name="ticket", description="Support ticket system.")

class TicketCloseView(View):
    """Persistent close button placed inside ticket channels."""
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.danger, emoji="🔒", custom_id="ticket_close")
    async def close_ticket(self, interaction: discord.Interaction, button: Button):
        channel = interaction.channel
        ticket_row = db.fetchone("SELECT * FROM tickets WHERE channel_id=?", (channel.id,))
        if not ticket_row:
            return await interaction.response.send_message("❌ No ticket record found.", ephemeral=True)

        confirmed = await confirm(interaction, "Close this ticket?")
        if not confirmed:
            return

        # Save transcript
        transcript = StringIO()
        async for msg in channel.history(limit=500, oldest_first=True):
            transcript.write(f"[{msg.created_at.strftime('%Y-%m-%d %H:%M')}] {msg.author}: {msg.content}\n")
        transcript.seek(0)
        file = discord.File(transcript, filename=f"ticket_{channel.name}_transcript.txt")

        # DM transcript to opener
        try:
            opener = await bot.fetch_user(ticket_row["user_id"])
            await opener.send(f"📄 Transcript for your ticket in **{interaction.guild.name}**:", file=file)
        except (discord.Forbidden, discord.NotFound):
            pass

        db.execute("UPDATE tickets SET status='closed' WHERE channel_id=?", (channel.id,))
        await interaction.followup.send("🔒 Ticket closed. Deleting channel in 5s...")
        await asyncio.sleep(5)
        await channel.delete(reason="Ticket closed.")

@ticket_group.command(name="open", description="Open a support ticket.")
@app_commands.describe(reason="Brief description of your issue")
async def ticket_open(inter: discord.Interaction, reason: str = "No reason provided."):
    # Check for existing open ticket
    existing = db.fetchone(
        "SELECT channel_id FROM tickets WHERE user_id=? AND guild_id=? AND status='open'",
        (inter.user.id, inter.guild_id)
    )
    if existing:
        chan = inter.guild.get_channel(existing["channel_id"])
        if chan:
            return await inter.response.send_message(f"❌ You already have an open ticket: {chan.mention}", ephemeral=True)

    # Find or create category
    category = discord.utils.get(inter.guild.categories, name=TICKET_CATEGORY_NAME)
    if not category:
        category = await inter.guild.create_category(TICKET_CATEGORY_NAME)

    support_role = discord.utils.get(inter.guild.roles, name=TICKET_SUPPORT_ROLE)

    # Build permission overwrites
    overwrites = {
        inter.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        inter.user:               discord.PermissionOverwrite(read_messages=True, send_messages=True),
        inter.guild.me:           discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True),
    }
    if support_role:
        overwrites[support_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

    channel = await inter.guild.create_text_channel(
        f"ticket-{inter.user.name}",
        category=category,
        overwrites=overwrites,
        reason=f"Ticket opened by {inter.user}",
    )

    db.execute(
        "INSERT INTO tickets (user_id, guild_id, channel_id) VALUES (?,?,?)",
        (inter.user.id, inter.guild_id, channel.id)
    )

    embed = EmbedBuilder.info(
        "🎟️ Support Ticket",
        f"Hello {inter.user.mention}!\n\n**Issue:** {reason}\n\nA staff member will be with you shortly.\nClick **Close Ticket** when resolved.",
    )
    await channel.send(embed=embed, view=TicketCloseView())
    await inter.response.send_message(f"✅ Ticket opened: {channel.mention}", ephemeral=True)

bot.tree.add_command(ticket_group)


# =============================================================================
# §24 WEL-SYS — Skeleton: Welcome / Goodbye System
# =============================================================================
# GUIDE: Set WELCOME_CHANNEL_ID in your guild_config table or .env.
# Customize the embed below. member.guild has all server info.

WELCOME_CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID", "0") or "0")

@bot.event
async def on_member_join(member: discord.Member):
    """Fires when a new member joins the server."""
    guild = member.guild
    channel_id = WELCOME_CHANNEL_ID
    if not channel_id:
        # Fallback: check guild_config DB
        row = db.fetchone("SELECT welcome_channel FROM guild_config WHERE guild_id=?", (guild.id,))
        if row and row["welcome_channel"]:
            channel_id = row["welcome_channel"]

    channel = guild.get_channel(channel_id)
    if not channel:
        return

    member_count = guild.member_count
    embed = EmbedBuilder.info(
        f"👋 Welcome to {guild.name}!",
        f"Hey {member.mention}, welcome! You are member **#{member_count}**.",
        thumbnail_url=member.display_avatar.url,
        color=EMBED_COLOR_SUCCESS,
    )
    embed.add_field(name="Account Created", value=discord.utils.format_dt(member.created_at, "R"), inline=True)
    await channel.send(embed=embed)

    # Optional: Assign auto-role
    # auto_role = guild.get_role(YOUR_AUTOROLE_ID)
    # if auto_role:
    #     await member.add_roles(auto_role)

@bot.event
async def on_member_remove(member: discord.Member):
    """Fires when a member leaves or is kicked/banned."""
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        await channel.send(
            embed=EmbedBuilder.warning(
                "Member Left",
                f"**{member}** has left the server. Members: {member.guild.member_count}"
            )
        )


# =============================================================================
# §25 RXN-ROLES — Skeleton: Button-Based Self-Role System
# =============================================================================
# GUIDE: Post a role-selection menu that users click to assign themselves roles.
# Backed by PersistentRoleButton (§13). Add more roles by extending role_data.

role_setup_group = app_commands.Group(
    name="rolesetup",
    description="Self-role menu management.",
    default_permissions=discord.Permissions(administrator=True)
)

@role_setup_group.command(name="post", description="Post a self-role selection menu in this channel.")
@app_commands.describe(title="Title of the menu embed")
async def rolesetup_post(inter: discord.Interaction, title: str = "🎭 Self-Roles"):
    """
    GUIDE: Modify role_data with your actual role IDs and labels.
    Each role gets a persistent button. Users click to toggle the role.
    """
    role_data = [
        # (role_id, button_label, button_style, emoji)
        # Replace role IDs with real ones from your server
        (0, "Gamer",     discord.ButtonStyle.primary,   "🎮"),
        (0, "Artist",    discord.ButtonStyle.secondary,  "🎨"),
        (0, "Developer", discord.ButtonStyle.success,    "💻"),
    ]

    view = View(timeout=None)
    for role_id, label, style, emoji in role_data:
        btn = Button(label=label, style=style, emoji=emoji, custom_id=f"selfrole_{role_id}")
        # Attach callback
        async def _cb(interaction: discord.Interaction, rid=role_id):
            role = interaction.guild.get_role(rid)
            if not role:
                return await interaction.response.send_message("❌ Role not configured.", ephemeral=True)
            if role in interaction.user.roles:
                await interaction.user.remove_roles(role)
                await interaction.response.send_message(f"✅ Removed **{role.name}**.", ephemeral=True)
            else:
                await interaction.user.add_roles(role)
                await interaction.response.send_message(f"✅ Added **{role.name}**.", ephemeral=True)
        btn.callback = _cb
        view.add_item(btn)

    embed = EmbedBuilder.info(title, "Click a button below to toggle a role.")
    await inter.response.send_message("✅ Role menu posted!", ephemeral=True)
    await inter.channel.send(embed=embed, view=view)

bot.tree.add_command(role_setup_group)


# =============================================================================
# §26 LVL-SYS — Skeleton: XP / Leveling System
# =============================================================================
# GUIDE: Grant XP on each message. Calculate level from XP using a curve.
# Level-up messages sent to the channel where the user leveled up.

XP_PER_MESSAGE   = 15      # Base XP granted per message
XP_COOLDOWN_SECS = 60      # Prevent XP farming — seconds between XP grants
XP_MULTIPLIER    = 1.0     # Global multiplier (set >1 for events)

def xp_for_level(level: int) -> int:
    """XP needed to reach `level`. Uses quadratic curve: 100 * level^2."""
    return 100 * (level ** 2)

def get_level_from_xp(xp: int) -> int:
    level = 1
    while xp >= xp_for_level(level + 1):
        level += 1
    return level

async def grant_xp(message: discord.Message):
    """Call from on_message to grant XP with cooldown gating."""
    uid = message.author.id
    remaining = cooldowns.check(uid, "xp", XP_COOLDOWN_SECS)
    if remaining > 0:
        return

    cooldowns.reset(uid, "xp")
    data = get_user_data(uid)
    old_level = get_level_from_xp(data.get("xp", 0))
    data["xp"] = data.get("xp", 0) + int(XP_PER_MESSAGE * XP_MULTIPLIER)
    new_level  = get_level_from_xp(data["xp"])

    if new_level > old_level:
        data["level"] = new_level
        embed = EmbedBuilder.success(
            "Level Up! 🎉",
            f"{message.author.mention} reached **Level {new_level}**!",
        )
        try:
            await message.channel.send(embed=embed)
        except discord.Forbidden:
            pass

lvl_group = app_commands.Group(name="lvl", description="XP and leveling commands.")

@lvl_group.command(name="rank", description="Check your rank and XP.")
@app_commands.describe(member="Member to check (optional)")
async def lvl_rank(inter: discord.Interaction, member: discord.Member = None):
    target = member or inter.user
    data   = get_user_data(target.id)
    xp     = data.get("xp", 0)
    level  = get_level_from_xp(xp)
    next_xp = xp_for_level(level + 1)
    progress = xp / next_xp if next_xp > 0 else 1.0
    bar_len  = 20
    filled   = int(bar_len * progress)
    bar      = "█" * filled + "░" * (bar_len - filled)
    embed = EmbedBuilder.info(
        f"📊 {target.display_name}'s Rank",
        f"Level **{level}** — `{xp:,} / {next_xp:,} XP`\n`[{bar}]`",
        thumbnail_url=target.display_avatar.url,
        color=EMBED_COLOR_GOLD,
    )
    await inter.response.send_message(embed=embed)

@lvl_group.command(name="leaderboard", description="XP leaderboard.")
async def lvl_leaderboard(inter: discord.Interaction):
    await inter.response.defer()
    users = [
        (k, v.get("xp", 0))
        for k, v in BOT_DATABASE.items()
        if k.startswith("user:") and isinstance(v, dict) and v.get("xp", 0) > 0
    ]
    users.sort(key=lambda x: x[1], reverse=True)
    entries = []
    for uid_key, xp in users[:10]:
        uid  = int(uid_key.split(":")[1])
        user = bot.get_user(uid)
        name = user.display_name if user else f"User {uid}"
        lvl  = get_level_from_xp(xp)
        entries.append((name, f"Lv.{lvl} — {xp:,} XP"))
    await inter.followup.send(embed=EmbedBuilder.leaderboard("XP Leaderboard", entries))

bot.tree.add_command(lvl_group)


# =============================================================================
# §27 LOG-SYS — Skeleton: Server Audit Log Relay
# =============================================================================
# GUIDE: Relays key Discord audit events to your log channel.
# Set LOG_CHANNEL_ID in .env. All events below are opt-in — comment out unwanted ones.

@bot.event
async def on_message_delete(message: discord.Message):
    if message.author.bot or not message.guild:
        return
    if not message.content:
        return  # Skip empty/attachment-only messages
    desc = (
        f"**Author:** {message.author.mention} (`{message.author}`)\n"
        f"**Channel:** {message.channel.mention}\n"
        f"**Content:**\n```{message.content[:900]}```"
    )
    await send_log_to_channel(bot, "🗑️ Message Deleted", desc)

@bot.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    if before.author.bot or not before.guild:
        return
    if before.content == after.content:
        return
    desc = (
        f"**Author:** {before.author.mention}\n"
        f"**Channel:** {before.channel.mention}\n"
        f"**Before:** {before.content[:400]}\n"
        f"**After:** {after.content[:400]}\n"
        f"[Jump to message]({after.jump_url})"
    )
    await send_log_to_channel(bot, "✏️ Message Edited", desc)

@bot.event
async def on_guild_role_create(role: discord.Role):
    await send_log_to_channel(bot, "🆕 Role Created", f"**{role.name}** (`{role.id}`)")

@bot.event
async def on_guild_role_delete(role: discord.Role):
    await send_log_to_channel(bot, "🗑️ Role Deleted", f"**{role.name}** (`{role.id}`)")

@bot.event
async def on_guild_channel_create(channel: discord.abc.GuildChannel):
    await send_log_to_channel(bot, "📢 Channel Created", f"**{channel.name}** (`{channel.id}`)")

@bot.event
async def on_guild_channel_delete(channel: discord.abc.GuildChannel):
    await send_log_to_channel(bot, "🗑️ Channel Deleted", f"**{channel.name}** (`{channel.id}`)")

@bot.event
async def on_member_ban(guild: discord.Guild, user: discord.User):
    await send_log_to_channel(bot, "🔨 Member Banned", f"{user.mention} (`{user}`) was banned from **{guild.name}**.", EMBED_COLOR_ERROR)

@bot.event
async def on_member_unban(guild: discord.Guild, user: discord.User):
    await send_log_to_channel(bot, "🔓 Member Unbanned", f"{user.mention} (`{user}`) was unbanned in **{guild.name}**.", EMBED_COLOR_SUCCESS)

@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    """Log voice channel joins, leaves, and moves."""
    if before.channel == after.channel:
        return
    if before.channel is None:
        desc = f"{member.mention} joined **{after.channel.name}**"
    elif after.channel is None:
        desc = f"{member.mention} left **{before.channel.name}**"
    else:
        desc = f"{member.mention} moved: **{before.channel.name}** → **{after.channel.name}**"
    await send_log_to_channel(bot, "🔊 Voice Update", desc)


# =============================================================================
# §28 EVENTS — Events Library (all major discord.py events, reference)
# =============================================================================
# GUIDE: These are ALL available events in discord.py 2.x.
# Most are commented out to avoid duplicate definitions. Uncomment what you need.
# Full docs: https://discordpy.readthedocs.io/en/stable/api.html#event-reference

@bot.event
async def on_message(message: discord.Message):
    """Every visible message. ALWAYS filter bots. ALWAYS call process_commands."""
    if message.author.bot:
        return
    if not message.guild:
        # Handle DMs here if needed
        return

    # Grant XP (§26)
    await grant_xp(message)

    # Auto-responder example
    if "hello bot" in message.content.lower():
        await message.channel.send(f"Hello, {message.author.mention}! 👋")

    # Required if you use prefix commands (@bot.command)
    await bot.process_commands(message)

# ── Commented event stubs — uncomment and fill in as needed ──────────────────

# @bot.event
# async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
#     """User adds a reaction to a message."""
#     pass

# @bot.event
# async def on_reaction_remove(reaction: discord.Reaction, user: discord.User):
#     """User removes a reaction."""
#     pass

# @bot.event
# async def on_guild_join(guild: discord.Guild):
#     """Bot added to a new server. Good place to send a welcome DM to owner."""
#     pass

# @bot.event
# async def on_guild_remove(guild: discord.Guild):
#     """Bot removed from a server. Clean up guild data."""
#     pass

# @bot.event
# async def on_thread_create(thread: discord.Thread):
#     """New thread created. Auto-join or send welcome message."""
#     await thread.join()

# @bot.event
# async def on_thread_delete(thread: discord.Thread):
#     pass

# @bot.event
# async def on_typing(channel, user, when):
#     """Someone starts typing."""
#     pass

# @bot.event
# async def on_bulk_message_delete(messages: list):
#     """Multiple messages deleted at once (purge)."""
#     pass

# @bot.event
# async def on_invite_create(invite: discord.Invite):
#     """New invite created. Track for invite tracking."""
#     pass

# @bot.event
# async def on_invite_delete(invite: discord.Invite):
#     pass

# @bot.event
# async def on_guild_emojis_update(guild, before, after):
#     pass

# @bot.event
# async def on_scheduled_event_create(event: discord.ScheduledEvent):
#     pass

# @bot.event
# async def on_automod_action(execution: discord.AutoModAction):
#     """Fires when Discord's AutoMod takes action."""
#     pass


# =============================================================================
# §29 UTILS — Utility Functions
# =============================================================================

def chunk_list(lst: list, size: int) -> List[list]:
    """Split a list into chunks of `size`. Useful for paginating raw data."""
    return [lst[i:i+size] for i in range(0, len(lst), size)]

def truncate(text: str, max_len: int = 1024, suffix: str = "...") -> str:
    """Truncate text to fit Discord's field limits."""
    if len(text) <= max_len:
        return text
    return text[:max_len - len(suffix)] + suffix

def format_dt_human(dt: datetime.datetime) -> str:
    """Discord timestamp that shows as 'January 1, 2025 12:00 PM'"""
    return discord.utils.format_dt(dt, style="f")

def format_dt_relative(dt: datetime.datetime) -> str:
    """Discord timestamp that shows as '2 hours ago'"""
    return discord.utils.format_dt(dt, style="R")

def user_mention(user_id: int) -> str:
    return f"<@{user_id}>"

def role_mention(role_id: int) -> str:
    return f"<@&{role_id}>"

def channel_mention(channel_id: int) -> str:
    return f"<#{channel_id}>"

def parse_duration(text: str) -> Optional[datetime.timedelta]:
    """
    Parse human-readable duration string into timedelta.
    Examples: "1h", "30m", "2d", "1h30m"
    Returns None if parsing fails.
    """
    pattern = re.compile(r"(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?")
    match = pattern.fullmatch(text.strip().lower())
    if not match or not any(match.groups()):
        return None
    days, hours, minutes, seconds = (int(v or 0) for v in match.groups())
    return datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

def fuzzy_find(query: str, candidates: List[str], threshold: float = 0.6) -> Optional[str]:
    """
    Simple fuzzy string matcher. Returns best match if similarity > threshold.
    Uses character overlap — no external library needed.
    """
    query = query.lower()
    best_match = None
    best_score = 0.0
    for c in candidates:
        c_lower = c.lower()
        overlap = sum(1 for ch in query if ch in c_lower)
        score   = overlap / max(len(query), len(c_lower))
        if score > best_score:
            best_score = score
            best_match = c
    return best_match if best_score >= threshold else None

def build_progress_bar(current: int, maximum: int, length: int = 20) -> str:
    """ASCII progress bar. Returns '████░░░░░░ 40%'"""
    pct    = max(0, min(1, current / maximum)) if maximum > 0 else 0
    filled = int(length * pct)
    bar    = "█" * filled + "░" * (length - filled)
    return f"`[{bar}]` {pct*100:.1f}%"

async def fetch_member_safe(guild: discord.Guild, user_id: int) -> Optional[discord.Member]:
    """
    Safe member fetch that tries cache first, then API.
    Use instead of guild.get_member() when the member might not be cached.
    """
    member = guild.get_member(user_id)
    if member:
        return member
    try:
        return await guild.fetch_member(user_id)
    except (discord.NotFound, discord.HTTPException):
        return None

async def send_dm(user: discord.User, content: str = None, embed: discord.Embed = None) -> bool:
    """
    Send a DM to a user. Returns False if DMs are closed.
    Always catch discord.Forbidden — many users block bot DMs.
    """
    try:
        if content:
            await user.send(content=content)
        if embed:
            await user.send(embed=embed)
        return True
    except discord.Forbidden:
        return False

def ordinal(n: int) -> str:
    """Return ordinal string: 1 → '1st', 2 → '2nd', 22 → '22nd'"""
    if 11 <= (n % 100) <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


# =============================================================================
# §31 HELP-CMD — Custom Paginated Help Command
# =============================================================================
# GUIDE: Replaces the default help command with a paginated, category-grouped
# slash command version. Reads command tree dynamically — no manual upkeep.
# Hidden commands (admin) are filtered based on caller's permissions.

help_group = app_commands.Group(name="help", description="Bot help and documentation.")

class HelpCategoryView(RestrictedView):
    """Paginated help that shows all commands grouped by command group."""
    def __init__(self, owner_id: int, pages: List[discord.Embed], timeout: float = 180.0):
        super().__init__(owner_id, timeout)
        self.pages   = pages
        self.current = 0
        self._update_buttons()

    def _update_buttons(self):
        self.btn_prev.disabled = self.current == 0
        self.btn_next.disabled = self.current >= len(self.pages) - 1
        self.btn_label.label   = f"{self.current + 1} / {len(self.pages)}"

    def get_page(self) -> discord.Embed:
        return self.pages[self.current]

    @discord.ui.button(emoji="◀️", style=discord.ButtonStyle.secondary)
    async def btn_prev(self, interaction: discord.Interaction, button: Button):
        self.current -= 1
        self._update_buttons()
        await interaction.response.edit_message(embed=self.get_page(), view=self)

    @discord.ui.button(label="1/1", style=discord.ButtonStyle.primary, disabled=True)
    async def btn_label(self, interaction: discord.Interaction, button: Button):
        pass

    @discord.ui.button(emoji="▶️", style=discord.ButtonStyle.secondary)
    async def btn_next(self, interaction: discord.Interaction, button: Button):
        self.current += 1
        self._update_buttons()
        await interaction.response.edit_message(embed=self.get_page(), view=self)

def _build_help_pages(bot_instance: commands.Bot) -> List[discord.Embed]:
    """
    Dynamically reads all slash commands from the bot tree and groups by
    top-level command or group name. Returns a list of embeds (one per group).
    """
    groups: Dict[str, List[str]] = {}

    for cmd in bot_instance.tree.get_commands():
        if isinstance(cmd, app_commands.Group):
            entries = []
            for sub in cmd.commands:
                if isinstance(sub, app_commands.Group):
                    for subsub in sub.commands:
                        entries.append(f"`/{cmd.name} {sub.name} {subsub.name}` — {subsub.description}")
                else:
                    entries.append(f"`/{cmd.name} {sub.name}` — {sub.description}")
            groups[cmd.name.capitalize()] = entries
        else:
            groups.setdefault("General", []).append(f"`/{cmd.name}` — {cmd.description}")

    pages = []
    for group_name, entries in sorted(groups.items()):
        embed = EmbedBuilder.info(
            f"📖 Help — {group_name}",
            "\n".join(entries) or "*No commands.*",
            color=EMBED_COLOR_DEFAULT,
        )
        pages.append(embed)

    if not pages:
        pages = [EmbedBuilder.info("📖 Help", "No commands registered yet.")]
    return pages

@help_group.command(name="all", description="Show all available bot commands.")
async def help_all(inter: discord.Interaction):
    pages = _build_help_pages(bot)
    view  = HelpCategoryView(inter.user.id, pages)
    view.message = await inter.response.send_message(embed=view.get_page(), view=view)
    view.message = await inter.original_response()

@help_group.command(name="command", description="Get detailed help for a specific command.")
@app_commands.describe(name="Command name (e.g. 'roll' or 'mod warn')")
async def help_command(inter: discord.Interaction, name: str):
    parts = name.strip("/").split()
    cmd   = bot.tree.get_command(parts[0])
    if cmd and len(parts) > 1 and isinstance(cmd, app_commands.Group):
        cmd = cmd.get_command(parts[1])
    if not cmd:
        return await inter.response.send_message(f"❌ Command `/{name}` not found.", ephemeral=True)
    desc = cmd.description or "No description provided."
    embed = EmbedBuilder.info(
        f"📖 /{name}",
        desc,
        fields=[("Usage", f"`/{name}`", False)],
        color=EMBED_COLOR_DEFAULT,
    )
    await inter.response.send_message(embed=embed, ephemeral=True)

bot.tree.add_command(help_group)


# =============================================================================
# §32 FUN-CMD — Fun Commands
# =============================================================================
# GUIDE: Self-contained fun commands. Each is independent — copy any one out.

fun_group = app_commands.Group(name="fun", description="Fun commands.")

# ── 8-Ball ────────────────────────────────────────────────────────────────────
_EIGHTBALL_RESPONSES = [
    ("🟢", "It is certain."), ("🟢", "Without a doubt."), ("🟢", "You may rely on it."),
    ("🟢", "Yes, definitely."), ("🟢", "Most likely."), ("🟡", "Reply hazy, try again."),
    ("🟡", "Ask again later."), ("🟡", "Cannot predict now."), ("🟡", "Concentrate and ask again."),
    ("🔴", "Don't count on it."), ("🔴", "My reply is no."), ("🔴", "Outlook not so good."),
    ("🔴", "Very doubtful."),
]

@fun_group.command(name="8ball", description="Ask the magic 8-ball a question.")
@app_commands.describe(question="Your yes/no question")
async def fun_8ball(inter: discord.Interaction, question: str):
    emoji, answer = random.choice(_EIGHTBALL_RESPONSES)
    embed = EmbedBuilder.info(
        "🎱 Magic 8-Ball",
        f"**Q:** {question[:200]}\n**A:** {emoji} {answer}",
        color=EMBED_COLOR_PURPLE,
    )
    await inter.response.send_message(embed=embed)

# ── Coinflip ──────────────────────────────────────────────────────────────────
@fun_group.command(name="coinflip", description="Flip a coin.")
async def fun_coinflip(inter: discord.Interaction):
    result = random.choice([("🪙 Heads!", 0x3498DB), ("🪙 Tails!", 0x95A5A6)])
    await inter.response.send_message(embed=EmbedBuilder.base(*result))

# ── Choose ────────────────────────────────────────────────────────────────────
@fun_group.command(name="choose", description="Pick one from a list of options.")
@app_commands.describe(options="Options separated by commas: apple, banana, cherry")
async def fun_choose(inter: discord.Interaction, options: str):
    choices = [o.strip() for o in options.split(",") if o.strip()]
    if len(choices) < 2:
        return await inter.response.send_message("❌ Provide at least 2 comma-separated options.", ephemeral=True)
    chosen = random.choice(choices)
    embed = EmbedBuilder.info("🎯 Decision Made", f"From {len(choices)} options, I choose:\n\n**{chosen}**")
    await inter.response.send_message(embed=embed)

# ── Joke ──────────────────────────────────────────────────────────────────────
_JOKES = [
    ("Why don't scientists trust atoms?", "Because they make up everything!"),
    ("I told my wife she was drawing her eyebrows too high.", "She looked surprised."),
    ("What do you call a fake noodle?", "An impasta!"),
    ("Why did the scarecrow win an award?", "Because he was outstanding in his field!"),
    ("I'm reading a book about anti-gravity.", "It's impossible to put down."),
]

@fun_group.command(name="joke", description="Get a random joke.")
async def fun_joke(inter: discord.Interaction):
    setup, punchline = random.choice(_JOKES)
    embed = EmbedBuilder.base("😂 Joke", color=EMBED_COLOR_GOLD)
    embed.add_field(name="Setup", value=setup, inline=False)
    embed.add_field(name="Punchline", value=f"||{punchline}||", inline=False)
    await inter.response.send_message(embed=embed)

# ── Rock Paper Scissors ───────────────────────────────────────────────────────
class RPSView(RestrictedView):
    _CHOICES   = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}
    _WIN_TABLE = {("rock", "scissors"), ("paper", "rock"), ("scissors", "paper")}

    def __init__(self, owner_id: int):
        super().__init__(owner_id, timeout=30.0)

    async def _play(self, interaction: discord.Interaction, player_choice: str):
        bot_choice = random.choice(list(self._CHOICES))
        pe, be = self._CHOICES[player_choice], self._CHOICES[bot_choice]
        if player_choice == bot_choice:
            result, color = "🤝 Tie!", EMBED_COLOR_NEUTRAL
        elif (player_choice, bot_choice) in self._WIN_TABLE:
            result, color = "🎉 You Win!", EMBED_COLOR_SUCCESS
        else:
            result, color = "🤖 Bot Wins!", EMBED_COLOR_ERROR
        embed = EmbedBuilder.base(
            f"Rock Paper Scissors — {result}",
            f"You: {pe} **{player_choice.capitalize()}**\nBot: {be} **{bot_choice.capitalize()}**",
            color,
        )
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)
        self.stop()

    @discord.ui.button(label="🪨 Rock",     style=discord.ButtonStyle.secondary)
    async def btn_rock(self, inter, btn):     await self._play(inter, "rock")

    @discord.ui.button(label="📄 Paper",    style=discord.ButtonStyle.secondary)
    async def btn_paper(self, inter, btn):    await self._play(inter, "paper")

    @discord.ui.button(label="✂️ Scissors", style=discord.ButtonStyle.secondary)
    async def btn_scissors(self, inter, btn): await self._play(inter, "scissors")

@fun_group.command(name="rps", description="Play Rock Paper Scissors against the bot.")
async def fun_rps(inter: discord.Interaction):
    view  = RPSView(inter.user.id)
    embed = EmbedBuilder.base("Rock Paper Scissors", "Make your move!", EMBED_COLOR_PURPLE)
    await inter.response.send_message(embed=embed, view=view)
    view.message = await inter.original_response()

# ── Trivia ────────────────────────────────────────────────────────────────────
_TRIVIA_POOL = [
    {"q": "What is the capital of France?",          "a": "Paris",    "w": ["London", "Berlin", "Madrid"]},
    {"q": "How many sides does a hexagon have?",      "a": "6",        "w": ["5", "7", "8"]},
    {"q": "What element has the symbol 'O'?",         "a": "Oxygen",   "w": ["Gold", "Osmium", "Oganesson"]},
    {"q": "Who wrote 'Romeo and Juliet'?",            "a": "Shakespeare","w": ["Dickens", "Austen", "Twain"]},
    {"q": "What is 12 × 12?",                        "a": "144",      "w": ["122", "132", "148"]},
    {"q": "What planet is known as the Red Planet?",  "a": "Mars",     "w": ["Venus", "Jupiter", "Saturn"]},
    {"q": "How many bones are in the human body?",   "a": "206",      "w": ["189", "215", "198"]},
    {"q": "What is the fastest land animal?",         "a": "Cheetah",  "w": ["Lion", "Greyhound", "Pronghorn"]},
]

class TriviaView(RestrictedView):
    def __init__(self, owner_id: int, correct: str, all_options: List[str]):
        super().__init__(owner_id, timeout=20.0)
        self.correct = correct
        for opt in all_options:
            btn = Button(label=opt, style=discord.ButtonStyle.secondary)
            btn.callback = self._make_cb(opt)
            self.add_item(btn)

    def _make_cb(self, choice: str):
        async def cb(interaction: discord.Interaction):
            if interaction.user.id != self.owner_id:
                return await interaction.response.send_message("Not your trivia!", ephemeral=True)
            for child in self.children:
                child.disabled = True
                if isinstance(child, Button):
                    if child.label == self.correct:
                        child.style = discord.ButtonStyle.success
                    elif child.label == choice and choice != self.correct:
                        child.style = discord.ButtonStyle.danger
            if choice == self.correct:
                result = EmbedBuilder.success("Correct!", f"✅ **{self.correct}** is right!")
            else:
                result = EmbedBuilder.error("Wrong!", f"❌ Correct answer: **{self.correct}**")
            await interaction.response.edit_message(embed=result, view=self)
            self.stop()
        return cb

@fun_group.command(name="trivia", description="Answer a random trivia question.")
async def fun_trivia(inter: discord.Interaction):
    item    = random.choice(_TRIVIA_POOL)
    options = item["w"][:3] + [item["a"]]
    random.shuffle(options)
    view  = TriviaView(inter.user.id, item["a"], options)
    embed = EmbedBuilder.info("🧠 Trivia", f"**{item['q']}**\n\nYou have 20 seconds!", color=EMBED_COLOR_PURPLE)
    await inter.response.send_message(embed=embed, view=view)
    view.message = await inter.original_response()

bot.tree.add_command(fun_group)


# =============================================================================
# §33 POLL-SYS — Poll System
# =============================================================================
# GUIDE: Button-based polls with duplicate vote prevention.
# Polls stored in BOT_DATABASE["polls"][str(message_id)] = {...}
# Background task auto-closes expired polls every 60 seconds.
# Max 4 options per poll (Discord row limit).

poll_group = app_commands.Group(name="poll", description="Create and manage polls.")

def _get_polls() -> dict:
    return BOT_DATABASE.setdefault("polls", {})

class PollView(View):
    """Persistent poll view. Survives restarts if registered with bot.add_view()."""
    def __init__(self, poll_id: str, options: List[str]):
        super().__init__(timeout=None)
        self.poll_id = poll_id
        for i, option in enumerate(options[:4]):
            btn = Button(
                label=option[:80],
                custom_id=f"poll_{poll_id}_opt{i}",
                style=discord.ButtonStyle.primary,
                row=0,
            )
            btn.callback = self._make_vote_cb(i)
            self.add_item(btn)

    def _make_vote_cb(self, opt_index: int):
        async def callback(interaction: discord.Interaction):
            poll_data = _get_polls().get(self.poll_id)
            if not poll_data:
                return await interaction.response.send_message("❌ Poll not found.", ephemeral=True)
            if poll_data.get("closed"):
                return await interaction.response.send_message("❌ This poll is closed.", ephemeral=True)
            uid = str(interaction.user.id)
            voted_map = poll_data.setdefault("voted", {})
            prev = voted_map.get(uid)
            if prev is not None:
                # Remove previous vote
                poll_data["votes"][prev] = max(0, poll_data["votes"][prev] - 1)
            voted_map[uid] = opt_index
            poll_data["votes"][opt_index] += 1
            save_json_db(BOT_DATABASE)

            opts    = poll_data["options"]
            total   = sum(poll_data["votes"])
            lines   = []
            for i, opt in enumerate(opts):
                count = poll_data["votes"][i]
                pct   = (count / total * 100) if total > 0 else 0
                bar   = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
                lines.append(f"**{opt}**\n`{bar}` {count} ({pct:.1f}%)")
            embed = EmbedBuilder.info(
                f"📊 {poll_data['question']}",
                "\n\n".join(lines),
                color=EMBED_COLOR_DEFAULT,
            )
            embed.set_footer(text=f"Total votes: {total} • Closes: {poll_data.get('ends_at', 'Never')}")
            await interaction.response.edit_message(embed=embed, view=self)
        return callback

@poll_group.command(name="create", description="Create a poll with up to 4 options.")
@app_commands.describe(
    question="The poll question",
    option1="Option 1", option2="Option 2",
    option3="Option 3 (optional)", option4="Option 4 (optional)",
    duration="Duration e.g. 1h, 30m, 2d (omit for no auto-close)",
)
async def poll_create(
    inter: discord.Interaction,
    question: str,
    option1: str,
    option2: str,
    option3: str = None,
    option4: str = None,
    duration: str = None,
):
    options = [o for o in [option1, option2, option3, option4] if o]
    ends_dt = None
    ends_str = "Never"
    if duration:
        td = parse_duration(duration)
        if not td:
            return await inter.response.send_message("❌ Invalid duration. Use: 1h, 30m, 2d", ephemeral=True)
        ends_dt  = (discord.utils.utcnow() + td).isoformat()
        ends_str = discord.utils.format_dt(discord.utils.utcnow() + td, "R")

    await inter.response.defer()

    # Temporary placeholder message_id — updated after send
    poll_id = str(inter.id)
    _get_polls()[poll_id] = {
        "question": question[:200],
        "options":  options,
        "votes":    [0] * len(options),
        "voted":    {},
        "closed":   False,
        "channel_id": inter.channel_id,
        "guild_id":   inter.guild_id,
        "ends_at":  ends_str,
        "ends_dt":  ends_dt,
    }
    save_json_db(BOT_DATABASE)

    view = PollView(poll_id, options)
    embed = EmbedBuilder.info(
        f"📊 {question}",
        "\n\n".join(f"**{o}**\n`{'░'*20}` 0 (0.0%)" for o in options),
        color=EMBED_COLOR_DEFAULT,
    )
    embed.set_footer(text=f"Total votes: 0 • Closes: {ends_str}")
    await inter.followup.send(embed=embed, view=view)

@poll_group.command(name="close", description="Immediately close an active poll.")
@app_commands.describe(poll_id="The interaction ID of the poll (shown at creation)")
@app_commands.default_permissions(manage_messages=True)
async def poll_close(inter: discord.Interaction, poll_id: str):
    poll_data = _get_polls().get(poll_id)
    if not poll_data:
        return await inter.response.send_message("❌ Poll not found.", ephemeral=True)
    poll_data["closed"] = True
    save_json_db(BOT_DATABASE)
    await inter.response.send_message("✅ Poll closed.", ephemeral=True)

@tasks.loop(seconds=60)
async def _task_poll_autoclose():
    """Auto-close polls whose end time has passed."""
    now = discord.utils.utcnow().isoformat()
    for pid, pdata in _get_polls().items():
        if not pdata.get("closed") and pdata.get("ends_dt") and pdata["ends_dt"] < now:
            pdata["closed"] = True
            logger.info(f"Auto-closed poll {pid}")
    save_json_db(BOT_DATABASE)

_task_poll_autoclose.before_loop(lambda: bot.wait_until_ready())

bot.tree.add_command(poll_group)


# =============================================================================
# §34 GIVE-SYS — Giveaway System
# =============================================================================
# GUIDE: Full giveaway system with timed auto-end, multi-winner, and reroll.
# Giveaways stored in BOT_DATABASE["giveaways"][str(message_id)] = {...}
# Background task checks every 30 seconds for ended giveaways.

give_group = app_commands.Group(name="giveaway", description="Giveaway management.")

def _get_giveaways() -> dict:
    return BOT_DATABASE.setdefault("giveaways", {})

class GiveawayEntryView(View):
    """Persistent Enter button for giveaways."""
    def __init__(self, giveaway_id: str):
        super().__init__(timeout=None)
        self.giveaway_id = giveaway_id
        self.btn.custom_id = f"giveaway_enter_{giveaway_id}"

    @discord.ui.button(label="🎉 Enter Giveaway", style=discord.ButtonStyle.success, custom_id="giveaway_enter_placeholder")
    async def btn(self, interaction: discord.Interaction, button: Button):
        gw = _get_giveaways().get(self.giveaway_id)
        if not gw:
            return await interaction.response.send_message("❌ Giveaway not found.", ephemeral=True)
        if gw.get("ended"):
            return await interaction.response.send_message("❌ This giveaway has ended.", ephemeral=True)
        uid = str(interaction.user.id)
        if uid in gw["entrants"]:
            gw["entrants"].remove(uid)
            save_json_db(BOT_DATABASE)
            return await interaction.response.send_message("✅ You left the giveaway.", ephemeral=True)
        gw["entrants"].append(uid)
        save_json_db(BOT_DATABASE)
        await interaction.response.send_message(
            f"✅ Entered! **{len(gw['entrants'])}** total entrants.", ephemeral=True
        )

def _build_giveaway_embed(gw: dict, ended: bool = False) -> discord.Embed:
    color  = EMBED_COLOR_GOLD if not ended else EMBED_COLOR_NEUTRAL
    status = "🏆 Winners: " + (", ".join(f"<@{w}>" for w in gw.get("winners", [])) or "None") if ended else f"Ends: {gw['ends_str']}"
    embed  = EmbedBuilder.info(
        f"🎉 GIVEAWAY — {gw['prize']}",
        f"React with 🎉 or click **Enter** to participate!\n\n"
        f"**Winners:** {gw['winner_count']}\n"
        f"**Hosted by:** <@{gw['host_id']}>\n"
        f"**Entrants:** {len(gw['entrants'])}\n"
        f"**{status}**",
        color=color,
    )
    return embed

async def _end_giveaway(giveaway_id: str):
    gw = _get_giveaways().get(giveaway_id)
    if not gw or gw.get("ended"):
        return
    gw["ended"] = True
    pool = gw["entrants"]
    count = min(gw["winner_count"], len(pool))
    winners = random.sample(pool, count) if count > 0 else []
    gw["winners"] = winners
    save_json_db(BOT_DATABASE)

    channel = bot.get_channel(gw["channel_id"])
    if not channel:
        return
    try:
        msg = await channel.fetch_message(int(giveaway_id))
    except (discord.NotFound, discord.HTTPException):
        return

    embed = _build_giveaway_embed(gw, ended=True)
    for item in msg.components:
        for comp in (item.children if hasattr(item, "children") else [item]):
            pass  # disable via editing view=None
    await msg.edit(embed=embed, view=None)

    if winners:
        mentions = " ".join(f"<@{w}>" for w in winners)
        await channel.send(f"🎊 Congratulations {mentions}! You won **{gw['prize']}**!")
    else:
        await channel.send(f"😔 No valid entrants for **{gw['prize']}**.")

@give_group.command(name="start", description="Start a giveaway.")
@app_commands.describe(
    prize="What is being given away",
    duration="How long: 1h, 30m, 2d",
    winners="Number of winners (default 1)",
)
@app_commands.default_permissions(manage_guild=True)
async def give_start(inter: discord.Interaction, prize: str, duration: str, winners: int = 1):
    td = parse_duration(duration)
    if not td:
        return await inter.response.send_message("❌ Invalid duration. Use: 1h, 30m, 2d", ephemeral=True)
    ends_at  = discord.utils.utcnow() + td
    ends_str = discord.utils.format_dt(ends_at, "R")

    await inter.response.defer()

    placeholder_id = str(inter.id)
    gw_data = {
        "prize":        prize[:200],
        "winner_count": max(1, min(20, winners)),
        "host_id":      inter.user.id,
        "channel_id":   inter.channel_id,
        "guild_id":     inter.guild_id,
        "ends_at":      ends_at.isoformat(),
        "ends_str":     ends_str,
        "entrants":     [],
        "winners":      [],
        "ended":        False,
    }
    _get_giveaways()[placeholder_id] = gw_data
    view  = GiveawayEntryView(placeholder_id)
    embed = _build_giveaway_embed(gw_data)
    msg   = await inter.followup.send(embed=embed, view=view)

    # Update key to real message ID
    real_id = str(msg.id)
    if real_id != placeholder_id:
        _get_giveaways()[real_id] = _get_giveaways().pop(placeholder_id)
        _get_giveaways()[real_id]["channel_id"] = msg.channel.id
    save_json_db(BOT_DATABASE)

@give_group.command(name="end", description="Force-end a giveaway now.")
@app_commands.describe(message_id="The giveaway message ID")
@app_commands.default_permissions(manage_guild=True)
async def give_end(inter: discord.Interaction, message_id: str):
    if message_id not in _get_giveaways():
        return await inter.response.send_message("❌ Giveaway not found.", ephemeral=True)
    await inter.response.defer(ephemeral=True)
    await _end_giveaway(message_id)
    await inter.followup.send("✅ Giveaway ended.", ephemeral=True)

@give_group.command(name="reroll", description="Reroll winners for an ended giveaway.")
@app_commands.describe(message_id="The giveaway message ID")
@app_commands.default_permissions(manage_guild=True)
async def give_reroll(inter: discord.Interaction, message_id: str):
    gw = _get_giveaways().get(message_id)
    if not gw:
        return await inter.response.send_message("❌ Giveaway not found.", ephemeral=True)
    pool = gw["entrants"]
    if not pool:
        return await inter.response.send_message("❌ No entrants to reroll.", ephemeral=True)
    count   = min(gw["winner_count"], len(pool))
    winners = random.sample(pool, count)
    gw["winners"] = winners
    save_json_db(BOT_DATABASE)
    mentions = " ".join(f"<@{w}>" for w in winners)
    await inter.response.send_message(f"🎊 Rerolled! New winner(s): {mentions}")

@tasks.loop(seconds=30)
async def _task_giveaway_check():
    now = discord.utils.utcnow().isoformat()
    for gid, gw in list(_get_giveaways().items()):
        if not gw.get("ended") and gw.get("ends_at") and gw["ends_at"] < now:
            await _end_giveaway(gid)

_task_giveaway_check.before_loop(lambda: bot.wait_until_ready())

bot.tree.add_command(give_group)


# =============================================================================
# §35 STAR-SYS — Starboard System
# =============================================================================
# GUIDE: Posts messages that hit a ⭐ reaction threshold to a #starboard channel.
# Uses on_raw_reaction_add (works even if the message isn't in cache).
# Set STARBOARD_CHANNEL_ID in .env or configure per-guild with /starboard set.
# Already-posted messages tracked so they're never double-posted.

STARBOARD_CHANNEL_ID = int(os.getenv("STARBOARD_CHANNEL_ID", "0") or "0")
STARBOARD_EMOJI      = "⭐"
STARBOARD_THRESHOLD  = 3  # Default minimum stars

def _get_starboard_config(guild_id: int) -> dict:
    return get_guild_data(guild_id).setdefault("starboard", {
        "channel_id": STARBOARD_CHANNEL_ID,
        "threshold":  STARBOARD_THRESHOLD,
        "posted":     {},  # {source_message_id: starboard_message_id}
    })

@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    """Fires on every reaction add, even for uncached messages."""
    if str(payload.emoji) != STARBOARD_EMOJI:
        return
    if not payload.guild_id:
        return

    guild  = bot.get_guild(payload.guild_id)
    if not guild:
        return

    config = _get_starboard_config(payload.guild_id)
    sb_channel_id = config.get("channel_id", 0)
    threshold     = config.get("threshold", STARBOARD_THRESHOLD)
    if not sb_channel_id:
        return

    sb_channel = guild.get_channel(sb_channel_id)
    if not sb_channel:
        return

    try:
        channel = guild.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
    except (discord.NotFound, discord.HTTPException, AttributeError):
        return

    # Count ⭐ reactions
    star_count = 0
    for reaction in message.reactions:
        if str(reaction.emoji) == STARBOARD_EMOJI:
            star_count = reaction.count
            break

    msg_id_str = str(payload.message_id)
    posted     = config.setdefault("posted", {})

    if star_count < threshold:
        return  # Not enough stars yet

    # Build starboard embed
    embed = discord.Embed(
        description=message.content[:2000] or "*[No text content]*",
        color=EMBED_COLOR_GOLD,
        timestamp=message.created_at,
    )
    embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
    embed.add_field(name="Source", value=f"[Jump to message]({message.jump_url})", inline=True)
    embed.add_field(name="Channel", value=message.channel.mention, inline=True)
    if message.attachments:
        embed.set_image(url=message.attachments[0].url)
    embed.set_footer(text=f"{STARBOARD_EMOJI} {star_count}")

    if msg_id_str in posted:
        # Update existing starboard post's star count
        try:
            sb_msg = await sb_channel.fetch_message(posted[msg_id_str])
            embed.set_footer(text=f"{STARBOARD_EMOJI} {star_count}")
            await sb_msg.edit(embed=embed)
        except (discord.NotFound, discord.HTTPException):
            del posted[msg_id_str]  # Re-post if original was deleted
    else:
        sb_msg = await sb_channel.send(
            content=f"{STARBOARD_EMOJI} **{star_count}** | {message.channel.mention}",
            embed=embed,
        )
        posted[msg_id_str] = sb_msg.id
    save_json_db(BOT_DATABASE)

star_group = app_commands.Group(name="starboard", description="Starboard configuration.", default_permissions=discord.Permissions(manage_guild=True))

@star_group.command(name="set", description="Set the starboard channel and star threshold.")
@app_commands.describe(channel="The starboard channel", threshold="Stars required (default 3)")
async def starboard_set(inter: discord.Interaction, channel: discord.TextChannel, threshold: int = 3):
    config = _get_starboard_config(inter.guild_id)
    config["channel_id"] = channel.id
    config["threshold"]  = max(1, threshold)
    save_json_db(BOT_DATABASE)
    embed = EmbedBuilder.success("Starboard Configured", f"Channel: {channel.mention}\nThreshold: {threshold} ⭐")
    await inter.response.send_message(embed=embed)

bot.tree.add_command(star_group)


# =============================================================================
# §36 REMIND-SYS — Reminder System
# =============================================================================
# GUIDE: Users set timed reminders. Bot DMs them when the timer fires.
# Reminders stored in BOT_DATABASE["reminders"] as a list of dicts.
# Background task checks every 30 seconds.

remind_group = app_commands.Group(name="remind", description="Reminder system.")

def _get_reminders() -> List[dict]:
    return BOT_DATABASE.setdefault("reminders", [])

@remind_group.command(name="me", description="Set a reminder.")
@app_commands.describe(
    duration="When to remind you: 10m, 2h, 1d",
    message="What to remind you about",
)
async def remind_me(inter: discord.Interaction, duration: str, message: str):
    td = parse_duration(duration)
    if not td:
        return await inter.response.send_message("❌ Invalid duration. Use: 10m, 2h, 1d", ephemeral=True)
    fires_at = (discord.utils.utcnow() + td).isoformat()
    reminder = {
        "id":         str(int(time.time() * 1000)),
        "user_id":    inter.user.id,
        "channel_id": inter.channel_id,
        "guild_id":   inter.guild_id,
        "message":    message[:500],
        "fires_at":   fires_at,
        "done":       False,
    }
    _get_reminders().append(reminder)
    save_json_db(BOT_DATABASE)
    embed = EmbedBuilder.success(
        "Reminder Set!",
        f"I'll DM you {discord.utils.format_dt(discord.utils.utcnow() + td, 'R')}.\n**Note:** {message[:200]}"
    )
    await inter.response.send_message(embed=embed, ephemeral=True)

@remind_group.command(name="list", description="List your active reminders.")
async def remind_list(inter: discord.Interaction):
    mine = [r for r in _get_reminders() if r["user_id"] == inter.user.id and not r["done"]]
    if not mine:
        return await inter.response.send_message("📭 You have no active reminders.", ephemeral=True)
    lines = []
    for i, r in enumerate(mine):
        try:
            dt = datetime.datetime.fromisoformat(r["fires_at"]).replace(tzinfo=datetime.timezone.utc)
            ts = discord.utils.format_dt(dt, "R")
        except Exception:
            ts = r["fires_at"]
        lines.append(f"`{i+1}.` [{r['id'][-6:]}] {ts} — {r['message'][:60]}")
    embed = EmbedBuilder.info("⏰ Your Reminders", "\n".join(lines))
    await inter.response.send_message(embed=embed, ephemeral=True)

@remind_group.command(name="cancel", description="Cancel a reminder by its short ID.")
@app_commands.describe(reminder_id="Last 6 chars of reminder ID (from /remind list)")
async def remind_cancel(inter: discord.Interaction, reminder_id: str):
    reminders = _get_reminders()
    for r in reminders:
        if r["user_id"] == inter.user.id and r["id"].endswith(reminder_id):
            r["done"] = True
            save_json_db(BOT_DATABASE)
            return await inter.response.send_message("✅ Reminder cancelled.", ephemeral=True)
    await inter.response.send_message("❌ Reminder not found.", ephemeral=True)

@tasks.loop(seconds=30)
async def _task_reminder_check():
    now = discord.utils.utcnow().isoformat()
    changed = False
    for r in _get_reminders():
        if r.get("done") or r["fires_at"] > now:
            continue
        r["done"] = True
        changed   = True
        user      = bot.get_user(r["user_id"])
        if not user:
            try:
                user = await bot.fetch_user(r["user_id"])
            except Exception:
                continue
        embed = EmbedBuilder.info(
            "⏰ Reminder!",
            r["message"],
            color=EMBED_COLOR_GOLD,
        )
        embed.set_footer(text="This was your reminder.")
        await send_dm(user, embed=embed)
    if changed:
        # Prune completed reminders older than 1 day
        cutoff = (discord.utils.utcnow() - datetime.timedelta(days=1)).isoformat()
        BOT_DATABASE["reminders"] = [
            r for r in _get_reminders() if not r["done"] or r["fires_at"] > cutoff
        ]
        save_json_db(BOT_DATABASE)

_task_reminder_check.before_loop(lambda: bot.wait_until_ready())

bot.tree.add_command(remind_group)


# =============================================================================
# §37 MUSIC-SKEL — Music Bot Skeleton
# =============================================================================
# GUIDE: Streams audio using yt-dlp + FFmpeg. Each guild has its own queue.
#
# DEPENDENCIES (install before use):
#   pip install yt-dlp PyNaCl
#   FFmpeg must be on system PATH: https://ffmpeg.org/download.html
#
# LEGAL NOTE: Ensure your usage complies with the Terms of Service of any
# platform you stream from. This skeleton is for educational purposes.
#
# ARCHITECTURE:
#   MusicQueue — per-guild queue + VoiceClient holder
#   YTDLSource — wraps yt-dlp to extract stream URLs
#   music_group — slash commands

try:
    youtube_dl = importlib.import_module("yt_dlp")
    YTDL_AVAILABLE = True
except ImportError:
    youtube_dl = None
    YTDL_AVAILABLE = False
    logger.warning("yt-dlp not installed. Music commands (§37) will be disabled. Run: pip install yt-dlp PyNaCl")

YTDL_FORMAT_OPTIONS = {
    "format":            "bestaudio/best",
    "noplaylist":        True,
    "nocheckcertificate":True,
    "ignoreerrors":      False,
    "quiet":             True,
    "no_warnings":       True,
    "default_search":    "ytsearch",
    "source_address":    "0.0.0.0",
    "postprocessors": [{
        "key":            "FFmpegExtractAudio",
        "preferredcodec": "opus",
    }],
}

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options":        "-vn",
}

class MusicTrack:
    """Holds metadata and stream URL for a single track."""
    __slots__ = ("title", "url", "stream_url", "duration", "thumbnail", "requester")

    def __init__(self, data: dict, requester: discord.Member):
        self.title      = data.get("title", "Unknown")
        self.url        = data.get("webpage_url", "")
        self.stream_url = data.get("url", "")
        self.duration   = data.get("duration", 0)
        self.thumbnail  = data.get("thumbnail", "")
        self.requester  = requester

    @property
    def duration_str(self) -> str:
        m, s = divmod(int(self.duration), 60)
        h, m = divmod(m, 60)
        return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

class MusicQueue:
    """Per-guild music state."""
    def __init__(self):
        self.queue:   List[MusicTrack]          = []
        self.current: Optional[MusicTrack]      = None
        self.vc:      Optional[discord.VoiceClient] = None
        self.volume:  float                     = 0.5
        self.loop:    bool                      = False

    def is_playing(self) -> bool:
        return self.vc is not None and self.vc.is_playing()

    def is_paused(self) -> bool:
        return self.vc is not None and self.vc.is_paused()

    def clear(self):
        self.queue.clear()
        self.current = None

# Per-guild music queues
_music_queues: Dict[int, MusicQueue] = {}

def get_music_queue(guild_id: int) -> MusicQueue:
    if guild_id not in _music_queues:
        _music_queues[guild_id] = MusicQueue()
    return _music_queues[guild_id]

async def _ytdl_extract(query: str) -> Optional[dict]:
    """Run yt-dlp in executor to avoid blocking event loop."""
    if not YTDL_AVAILABLE:
        return None
    opts = dict(YTDL_FORMAT_OPTIONS)

    def _extract():
        with youtube_dl.YoutubeDL(opts) as ydl:
            try:
                info = ydl.extract_info(query, download=False)
                if "entries" in info:
                    info = info["entries"][0]  # Take first search result
                return info
            except Exception as e:
                logger.error(f"yt-dlp extract error: {e}")
                return None

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _extract)

async def _play_next(guild_id: int, text_channel: discord.TextChannel = None):
    """Play the next track in queue. Called after each track finishes."""
    mq = get_music_queue(guild_id)
    if not mq.queue or not mq.vc:
        mq.current = None
        return

    track = mq.queue.pop(0)
    mq.current = track

    source = discord.PCMVolumeTransformer(
        discord.FFmpegPCMAudio(track.stream_url, **FFMPEG_OPTIONS),
        volume=mq.volume,
    )

    def after(error):
        if error:
            logger.error(f"Music player error in guild {guild_id}: {error}")
        fut = asyncio.run_coroutine_threadsafe(_play_next(guild_id, text_channel), bot.loop)
        try:
            fut.result()
        except Exception as e:
            logger.error(f"Error scheduling next track: {e}")

    mq.vc.play(source, after=after)

    if text_channel:
        embed = EmbedBuilder.info(
            "🎵 Now Playing",
            f"**[{track.title}]({track.url})**\nDuration: `{track.duration_str}` • Requested by: {track.requester.mention}",
            thumbnail_url=track.thumbnail,
            color=EMBED_COLOR_PURPLE,
        )
        try:
            await text_channel.send(embed=embed, delete_after=track.duration + 5)
        except discord.HTTPException:
            pass

music_group = app_commands.Group(name="music", description="Music player commands.")

@music_group.command(name="join", description="Join your voice channel.")
async def music_join(inter: discord.Interaction):
    if not inter.user.voice or not inter.user.voice.channel:
        return await inter.response.send_message("❌ You must be in a voice channel.", ephemeral=True)
    vc_channel = inter.user.voice.channel
    mq = get_music_queue(inter.guild_id)
    if mq.vc and mq.vc.is_connected():
        await mq.vc.move_to(vc_channel)
    else:
        mq.vc = await vc_channel.connect()
    await inter.response.send_message(f"✅ Joined **{vc_channel.name}**.", ephemeral=True)

@music_group.command(name="leave", description="Leave the voice channel and clear queue.")
async def music_leave(inter: discord.Interaction):
    mq = get_music_queue(inter.guild_id)
    if not mq.vc:
        return await inter.response.send_message("❌ Not in a voice channel.", ephemeral=True)
    mq.clear()
    await mq.vc.disconnect()
    mq.vc = None
    await inter.response.send_message("👋 Left voice channel and cleared queue.")

@music_group.command(name="play", description="Search and play a song.")
@app_commands.describe(query="Song name or URL")
async def music_play(inter: discord.Interaction, query: str):
    if not YTDL_AVAILABLE:
        return await inter.response.send_message("❌ yt-dlp not installed. Run: `pip install yt-dlp`", ephemeral=True)
    if not inter.user.voice or not inter.user.voice.channel:
        return await inter.response.send_message("❌ Join a voice channel first.", ephemeral=True)

    await inter.response.defer()
    mq = get_music_queue(inter.guild_id)

    # Auto-join if not connected
    if not mq.vc or not mq.vc.is_connected():
        mq.vc = await inter.user.voice.channel.connect()

    data = await _ytdl_extract(query)
    if not data:
        return await inter.followup.send("❌ Could not find or extract that track.", ephemeral=True)

    track = MusicTrack(data, inter.user)
    mq.queue.append(track)

    if not mq.is_playing() and not mq.is_paused():
        await _play_next(inter.guild_id, inter.channel)
        await inter.followup.send(embed=EmbedBuilder.success("Playing Now", f"**{track.title}**"))
    else:
        pos = len(mq.queue)
        await inter.followup.send(
            embed=EmbedBuilder.info("📥 Added to Queue", f"**{track.title}**\nPosition: #{pos}")
        )

@music_group.command(name="skip", description="Skip the current track.")
async def music_skip(inter: discord.Interaction):
    mq = get_music_queue(inter.guild_id)
    if not mq.is_playing():
        return await inter.response.send_message("❌ Nothing is playing.", ephemeral=True)
    mq.vc.stop()  # Triggers after() callback → plays next
    await inter.response.send_message("⏭️ Skipped.")

@music_group.command(name="pause", description="Pause the current track.")
async def music_pause(inter: discord.Interaction):
    mq = get_music_queue(inter.guild_id)
    if mq.is_playing():
        mq.vc.pause()
        await inter.response.send_message("⏸️ Paused.")
    elif mq.is_paused():
        mq.vc.resume()
        await inter.response.send_message("▶️ Resumed.")
    else:
        await inter.response.send_message("❌ Nothing is playing.", ephemeral=True)

@music_group.command(name="stop", description="Stop playback and clear the queue.")
async def music_stop(inter: discord.Interaction):
    mq = get_music_queue(inter.guild_id)
    if not mq.vc:
        return await inter.response.send_message("❌ Not connected.", ephemeral=True)
    mq.clear()
    mq.vc.stop()
    await inter.response.send_message("⏹️ Stopped and queue cleared.")

@music_group.command(name="volume", description="Set playback volume (0-100).")
@app_commands.describe(level="Volume level 0–100")
async def music_volume(inter: discord.Interaction, level: int):
    mq = get_music_queue(inter.guild_id)
    level = max(0, min(100, level))
    mq.volume = level / 100
    if mq.vc and mq.vc.source:
        mq.vc.source.volume = mq.volume
    await inter.response.send_message(f"🔊 Volume set to **{level}%**.")

@music_group.command(name="queue", description="Show the current queue.")
async def music_queue_cmd(inter: discord.Interaction):
    mq = get_music_queue(inter.guild_id)
    if not mq.current and not mq.queue:
        return await inter.response.send_message("📭 Queue is empty.", ephemeral=True)
    lines = []
    if mq.current:
        lines.append(f"▶️ **Now:** {mq.current.title} `{mq.current.duration_str}`")
    for i, t in enumerate(mq.queue[:15], 1):
        lines.append(f"`{i}.` {t.title} `{t.duration_str}` — {t.requester.display_name}")
    if len(mq.queue) > 15:
        lines.append(f"*...and {len(mq.queue)-15} more.*")
    pager = Paginator(inter.user.id, lines, title="🎵 Music Queue", per_page=10)
    await inter.response.send_message(embed=pager.get_embed(), view=pager)
    pager.message = await inter.original_response()

@music_group.command(name="nowplaying", description="Show the currently playing track.")
async def music_nowplaying(inter: discord.Interaction):
    mq = get_music_queue(inter.guild_id)
    if not mq.current:
        return await inter.response.send_message("❌ Nothing is playing.", ephemeral=True)
    t = mq.current
    embed = EmbedBuilder.info(
        "🎵 Now Playing",
        f"**[{t.title}]({t.url})**\nDuration: `{t.duration_str}` • Vol: {int(mq.volume*100)}%\nRequested by: {t.requester.mention}",
        thumbnail_url=t.thumbnail,
        color=EMBED_COLOR_PURPLE,
    )
    await inter.response.send_message(embed=embed)

bot.tree.add_command(music_group)


# =============================================================================
# §38 AUTOMOD — Anti-Spam / AutoMod
# =============================================================================
# GUIDE: Tracks messages per user per guild. Triggers on rate abuse, excessive
# caps, link spam, or mass-mentions. Action escalates: warn → timeout → ban.
# Whitelist roles are immune. All config stored per-guild in BOT_DATABASE.
# Add `await automod_check(message)` at the TOP of on_message.

class _SpamTracker:
    """Tracks recent message timestamps per user per guild."""
    def __init__(self):
        self._data: Dict[str, List[float]] = {}

    def record(self, guild_id: int, user_id: int) -> int:
        """Records a message and returns the count within the rolling window."""
        key = f"{guild_id}:{user_id}"
        now = time.time()
        timestamps = self._data.setdefault(key, [])
        timestamps.append(now)
        # Keep only last 10 seconds
        self._data[key] = [t for t in timestamps if now - t < 10]
        return len(self._data[key])

    def clear(self, guild_id: int, user_id: int):
        self._data.pop(f"{guild_id}:{user_id}", None)

_spam_tracker = _SpamTracker()

# Default automod config
_AUTOMOD_DEFAULTS = {
    "enabled":           True,
    "spam_threshold":    5,     # Messages per 10 seconds
    "caps_threshold":    70,    # Percentage of caps (0-100, 0 = disabled)
    "max_mentions":      5,     # Max @mentions per message (0 = disabled)
    "block_links":       False, # Block all URLs
    "whitelist_role_ids":[],    # Role IDs immune to automod
    "action_warn":       True,
    "action_timeout_m":  5,     # Timeout duration in minutes (0 = skip)
    "action_ban":        False, # Ban after timeout (dangerous — false by default)
}

def _get_automod_config(guild_id: int) -> dict:
    data = get_guild_data(guild_id)
    if "automod" not in data:
        data["automod"] = dict(_AUTOMOD_DEFAULTS)
    return data["automod"]

_URL_PATTERN = re.compile(r"https?://\S+|discord\.gg/\S+", re.IGNORECASE)

async def automod_check(message: discord.Message) -> bool:
    """
    GUIDE: Call at the start of on_message (after bot check).
    Returns True if the message was flagged and acted upon (so you can return early).

    Usage in on_message:
        if await automod_check(message):
            return
    """
    if not message.guild or message.author.bot:
        return False
    member = message.author
    if not isinstance(member, discord.Member):
        return False

    cfg = _get_automod_config(message.guild.id)
    if not cfg.get("enabled"):
        return False

    # Whitelist check
    whitelist_ids = set(cfg.get("whitelist_role_ids", []))
    if any(r.id in whitelist_ids for r in member.roles):
        return False
    if member.guild_permissions.administrator:
        return False

    content = message.content
    triggered_reason = None

    # ── Spam rate check ───────────────────────────────────────────────────
    count = _spam_tracker.record(message.guild.id, member.id)
    if count >= cfg.get("spam_threshold", 5):
        triggered_reason = f"spam ({count} msgs/10s)"
        _spam_tracker.clear(message.guild.id, member.id)

    # ── Caps filter ────────────────────────────────────────────────────────
    if not triggered_reason:
        caps_threshold = cfg.get("caps_threshold", 0)
        if caps_threshold > 0 and len(content) > 10:
            caps_pct = sum(1 for c in content if c.isupper()) / len(content) * 100
            if caps_pct >= caps_threshold:
                triggered_reason = f"excessive caps ({caps_pct:.0f}%)"

    # ── Link filter ────────────────────────────────────────────────────────
    if not triggered_reason and cfg.get("block_links") and _URL_PATTERN.search(content):
        triggered_reason = "link blocked"

    # ── Mass mention filter ────────────────────────────────────────────────
    if not triggered_reason:
        max_mentions = cfg.get("max_mentions", 0)
        if max_mentions > 0 and len(message.mentions) >= max_mentions:
            triggered_reason = f"mass mention ({len(message.mentions)})"

    if not triggered_reason:
        return False

    # ── Take action ────────────────────────────────────────────────────────
    try:
        await message.delete()
    except discord.Forbidden:
        pass

    logger.info(f"AutoMod triggered: {member} in {message.guild} — {triggered_reason}")

    if cfg.get("action_warn"):
        warning_embed = EmbedBuilder.warning(
            "AutoMod Warning",
            f"{member.mention}, your message was removed.\n**Reason:** {triggered_reason}"
        )
        try:
            warn_msg = await message.channel.send(embed=warning_embed, delete_after=8)
        except discord.Forbidden:
            pass
        db.execute(
            "INSERT INTO warnings (user_id, guild_id, mod_id, reason) VALUES (?,?,?,?)",
            (member.id, message.guild.id, bot.user.id, f"[AutoMod] {triggered_reason}")
        )

    timeout_min = cfg.get("action_timeout_m", 0)
    if timeout_min > 0:
        until = discord.utils.utcnow() + datetime.timedelta(minutes=timeout_min)
        try:
            await member.timeout(until, reason=f"AutoMod: {triggered_reason}")
        except discord.Forbidden:
            pass

    await send_log_to_channel(
        bot,
        "🛡️ AutoMod Action",
        f"**User:** {member.mention}\n**Reason:** {triggered_reason}\n**Channel:** {message.channel.mention}",
        EMBED_COLOR_WARNING,
    )
    return True

automod_group = app_commands.Group(
    name="automod",
    description="AutoMod configuration.",
    default_permissions=discord.Permissions(manage_guild=True),
)

@automod_group.command(name="status", description="Show current AutoMod config.")
async def automod_status(inter: discord.Interaction):
    cfg = _get_automod_config(inter.guild_id)
    fields = [
        ("Enabled",       str(cfg["enabled"]),                              True),
        ("Spam Threshold",f"{cfg['spam_threshold']} msgs / 10s",           True),
        ("Caps Filter",   f"{cfg['caps_threshold']}%" if cfg['caps_threshold'] else "Off", True),
        ("Max Mentions",  str(cfg['max_mentions']) if cfg['max_mentions'] else "Off", True),
        ("Block Links",   "Yes" if cfg['block_links'] else "No",            True),
        ("Auto-Timeout",  f"{cfg['action_timeout_m']}m" if cfg['action_timeout_m'] else "Off", True),
    ]
    embed = EmbedBuilder.info("🛡️ AutoMod Config", "", fields=fields, color=EMBED_COLOR_PURPLE)
    await inter.response.send_message(embed=embed, ephemeral=True)

@automod_group.command(name="toggle", description="Enable or disable AutoMod.")
async def automod_toggle(inter: discord.Interaction):
    cfg = _get_automod_config(inter.guild_id)
    cfg["enabled"] = not cfg["enabled"]
    save_json_db(BOT_DATABASE)
    status = "enabled ✅" if cfg["enabled"] else "disabled ❌"
    await inter.response.send_message(f"🛡️ AutoMod {status}.")

@automod_group.command(name="set", description="Adjust an AutoMod setting.")
@app_commands.describe(
    setting="The setting to change",
    value="New value (number or true/false)",
)
@app_commands.choices(setting=[
    app_commands.Choice(name="spam_threshold",   value="spam_threshold"),
    app_commands.Choice(name="caps_threshold",   value="caps_threshold"),
    app_commands.Choice(name="max_mentions",     value="max_mentions"),
    app_commands.Choice(name="action_timeout_m", value="action_timeout_m"),
    app_commands.Choice(name="block_links",      value="block_links"),
])
async def automod_set(inter: discord.Interaction, setting: str, value: str):
    cfg = _get_automod_config(inter.guild_id)
    bool_settings = {"block_links", "action_warn", "action_ban"}
    try:
        if setting in bool_settings:
            cfg[setting] = value.lower() in ("true", "yes", "1", "on")
        else:
            cfg[setting] = int(value)
    except ValueError:
        return await inter.response.send_message("❌ Invalid value.", ephemeral=True)
    save_json_db(BOT_DATABASE)
    await inter.response.send_message(f"✅ `{setting}` set to `{cfg[setting]}`.")

bot.tree.add_command(automod_group)


# =============================================================================
# §39 STATS-CHAN — Server Stats Voice Channels
# =============================================================================
# GUIDE: Creates voice channels that display live server stats in their names.
# Users cannot join them — they're display-only. Updated every 10 minutes.
# /stats setup creates the channels. Stores channel IDs in guild config.
# Voice channel names update via background task.

STATS_CATEGORY_NAME = "📊 Server Stats"

def _get_stats_config(guild_id: int) -> dict:
    return get_guild_data(guild_id).setdefault("stats_channels", {})

stats_group = app_commands.Group(
    name="stats",
    description="Server statistics channels.",
    default_permissions=discord.Permissions(manage_channels=True),
)

@stats_group.command(name="setup", description="Create server stats voice channels.")
async def stats_setup(inter: discord.Interaction):
    await inter.response.defer(ephemeral=True)
    guild  = inter.guild
    config = _get_stats_config(guild.id)

    # Find or create category
    category = discord.utils.get(guild.categories, name=STATS_CATEGORY_NAME)
    if not category:
        overwrites = {guild.default_role: discord.PermissionOverwrite(connect=False, view_channel=True)}
        category   = await guild.create_category(STATS_CATEGORY_NAME, overwrites=overwrites)

    async def _ensure_channel(key: str, name: str) -> discord.VoiceChannel:
        existing_id = config.get(key)
        ch = guild.get_channel(existing_id) if existing_id else None
        if not ch:
            ch = await guild.create_voice_channel(name, category=category)
            config[key] = ch.id
        return ch

    await _ensure_channel("members",  f"👥 Members: {guild.member_count}")
    await _ensure_channel("bots",     f"🤖 Bots: {sum(1 for m in guild.members if m.bot)}")
    await _ensure_channel("boosts",   f"⬆️ Boosts: {guild.premium_subscription_count}")
    await _ensure_channel("channels", f"🌐 Channels: {len(guild.channels)}")

    save_json_db(BOT_DATABASE)
    await inter.followup.send(embed=EmbedBuilder.success("Stats Channels Created", f"Category: **{STATS_CATEGORY_NAME}**\nUpdates every 10 minutes."), ephemeral=True)

@stats_group.command(name="remove", description="Delete the stats channels.")
async def stats_remove(inter: discord.Interaction):
    config = _get_stats_config(inter.guild_id)
    removed = 0
    for key in ["members", "bots", "boosts", "channels"]:
        ch_id = config.pop(key, None)
        if ch_id:
            ch = inter.guild.get_channel(ch_id)
            if ch:
                try:
                    await ch.delete(reason="Stats channels removed.")
                    removed += 1
                except discord.Forbidden:
                    pass
    save_json_db(BOT_DATABASE)
    await inter.response.send_message(f"✅ Removed {removed} stats channel(s).", ephemeral=True)

@tasks.loop(minutes=10)
async def _task_stats_update():
    """Update stats channel names across all guilds every 10 minutes."""
    for guild in bot.guilds:
        config = _get_stats_config(guild.id)
        if not config:
            continue
        stat_map = {
            "members":  f"👥 Members: {guild.member_count}",
            "bots":     f"🤖 Bots: {sum(1 for m in guild.members if m.bot)}",
            "boosts":   f"⬆️ Boosts: {guild.premium_subscription_count}",
            "channels": f"🌐 Channels: {len(guild.channels)}",
        }
        for key, name in stat_map.items():
            ch_id = config.get(key)
            if not ch_id:
                continue
            ch = guild.get_channel(ch_id)
            if ch and ch.name != name:
                try:
                    await ch.edit(name=name)
                    await asyncio.sleep(1)  # Respect rate limits (2 renames/10min per channel)
                except discord.Forbidden:
                    pass
                except discord.HTTPException:
                    pass

_task_stats_update.before_loop(lambda: bot.wait_until_ready())

bot.tree.add_command(stats_group)


# =============================================================================
# §40 SUGGEST-SYS — Suggestion System
# =============================================================================
# GUIDE: Users submit suggestions; they're posted to a channel with vote buttons.
# Staff can approve or deny suggestions. Votes tracked (no double-voting).
# Set SUGGESTIONS_CHANNEL_ID in .env.

SUGGESTIONS_CHANNEL_ID = int(os.getenv("SUGGESTIONS_CHANNEL_ID", "0") or "0")

def _get_suggestions(guild_id: int) -> dict:
    return get_guild_data(guild_id).setdefault("suggestions", {})

def _next_suggestion_id(guild_id: int) -> str:
    data = get_guild_data(guild_id)
    n    = data.get("suggestion_counter", 0) + 1
    data["suggestion_counter"] = n
    return f"#{n:04d}"

class SuggestionVoteView(View):
    """Persistent vote buttons on suggestion posts."""
    def __init__(self, suggestion_id: str, guild_id: int):
        super().__init__(timeout=None)
        self.suggestion_id = suggestion_id
        self.guild_id      = guild_id
        self.btn_up.custom_id   = f"suggest_up_{guild_id}_{suggestion_id}"
        self.btn_down.custom_id = f"suggest_dn_{guild_id}_{suggestion_id}"

    @discord.ui.button(label="👍 0", style=discord.ButtonStyle.success, custom_id="suggest_up_placeholder")
    async def btn_up(self, interaction: discord.Interaction, button: Button):
        await self._vote(interaction, "up")

    @discord.ui.button(label="👎 0", style=discord.ButtonStyle.danger, custom_id="suggest_dn_placeholder")
    async def btn_down(self, interaction: discord.Interaction, button: Button):
        await self._vote(interaction, "down")

    async def _vote(self, interaction: discord.Interaction, direction: str):
        suggestions = _get_suggestions(self.guild_id)
        sug = suggestions.get(self.suggestion_id)
        if not sug:
            return await interaction.response.send_message("❌ Suggestion not found.", ephemeral=True)
        if sug.get("status") in ("approved", "denied"):
            return await interaction.response.send_message("❌ Voting is closed.", ephemeral=True)

        uid    = str(interaction.user.id)
        votes  = sug.setdefault("votes", {})
        prev   = votes.get(uid)

        if prev == direction:
            # Toggle off
            del votes[uid]
        else:
            votes[uid] = direction

        ups   = sum(1 for v in votes.values() if v == "up")
        downs = sum(1 for v in votes.values() if v == "down")
        sug["ups"]   = ups
        sug["downs"] = downs
        save_json_db(BOT_DATABASE)

        # Update button labels
        self.btn_up.label   = f"👍 {ups}"
        self.btn_down.label = f"👎 {downs}"
        await interaction.response.edit_message(view=self)

def _build_suggestion_embed(sug: dict) -> discord.Embed:
    status_colors = {
        "pending":  EMBED_COLOR_DEFAULT,
        "approved": EMBED_COLOR_SUCCESS,
        "denied":   EMBED_COLOR_ERROR,
    }
    status_icons = {"pending": "⏳", "approved": "✅", "denied": "❌"}
    status = sug.get("status", "pending")
    embed  = discord.Embed(
        title=f"💡 Suggestion {sug['id']}",
        description=sug["content"],
        color=status_colors.get(status, EMBED_COLOR_DEFAULT),
        timestamp=discord.utils.utcnow(),
    )
    embed.add_field(name="Status",     value=f"{status_icons.get(status, '❓')} {status.capitalize()}", inline=True)
    embed.add_field(name="Submitted by", value=f"<@{sug['author_id']}>",                               inline=True)
    embed.add_field(name="Votes",      value=f"👍 {sug.get('ups', 0)} / 👎 {sug.get('downs', 0)}",    inline=True)
    if sug.get("staff_note"):
        embed.add_field(name="Staff Note", value=sug["staff_note"], inline=False)
    return embed

suggest_group = app_commands.Group(name="suggest", description="Suggestion system.")

@suggest_group.command(name="submit", description="Submit a suggestion.")
@app_commands.describe(content="Your suggestion (be detailed!)")
async def suggest_submit(inter: discord.Interaction, content: str):
    # Cooldown: 1 suggestion per 10 minutes
    remaining = cooldowns.check(inter.user.id, "suggest", 600)
    if remaining > 0:
        return await inter.response.send_message(
            f"⏳ Suggestion cooldown: **{format_remaining(remaining)}**", ephemeral=True
        )

    guild_id = inter.guild_id
    ch_id    = SUGGESTIONS_CHANNEL_ID

    # Fallback to guild-config if .env not set
    if not ch_id:
        row = db.fetchone("SELECT welcome_channel FROM guild_config WHERE guild_id=?", (guild_id,))
        if row and row["welcome_channel"]:
            ch_id = row["welcome_channel"]

    channel = bot.get_channel(ch_id)
    if not channel:
        return await inter.response.send_message("❌ Suggestions channel not configured. Ask an admin to set SUGGESTIONS_CHANNEL_ID.", ephemeral=True)

    sug_id = _next_suggestion_id(guild_id)
    sug_data = {
        "id":        sug_id,
        "content":   content[:1000],
        "author_id": inter.user.id,
        "status":    "pending",
        "ups":       0,
        "downs":     0,
        "votes":     {},
        "staff_note": "",
        "message_id": None,
    }
    cooldowns.reset(inter.user.id, "suggest")

    view  = SuggestionVoteView(sug_id, guild_id)
    embed = _build_suggestion_embed(sug_data)
    msg   = await channel.send(embed=embed, view=view)
    sug_data["message_id"] = msg.id

    _get_suggestions(guild_id)[sug_id] = sug_data
    save_json_db(BOT_DATABASE)

    await inter.response.send_message(
        embed=EmbedBuilder.success("Suggestion Submitted!", f"Your suggestion **{sug_id}** has been posted."),
        ephemeral=True,
    )

@suggest_group.command(name="approve", description="Approve a suggestion.")
@app_commands.describe(suggestion_id="Suggestion ID e.g. #0001", reason="Staff note")
@app_commands.default_permissions(manage_messages=True)
async def suggest_approve(inter: discord.Interaction, suggestion_id: str, reason: str = "Approved by staff."):
    await _update_suggestion_status(inter, suggestion_id, "approved", reason)

@suggest_group.command(name="deny", description="Deny a suggestion.")
@app_commands.describe(suggestion_id="Suggestion ID e.g. #0001", reason="Reason for denial")
@app_commands.default_permissions(manage_messages=True)
async def suggest_deny(inter: discord.Interaction, suggestion_id: str, reason: str = "Denied by staff."):
    await _update_suggestion_status(inter, suggestion_id, "denied", reason)

async def _update_suggestion_status(inter: discord.Interaction, sug_id: str, status: str, reason: str):
    suggestions = _get_suggestions(inter.guild_id)
    sug_id_clean = sug_id.strip().upper() if not sug_id.startswith("#") else sug_id.strip()
    sug = suggestions.get(sug_id_clean)
    if not sug:
        return await inter.response.send_message(f"❌ Suggestion `{sug_id_clean}` not found.", ephemeral=True)

    sug["status"]     = status
    sug["staff_note"] = reason
    save_json_db(BOT_DATABASE)

    # Edit original message
    channel = bot.get_channel(SUGGESTIONS_CHANNEL_ID)
    if channel and sug.get("message_id"):
        try:
            msg = await channel.fetch_message(sug["message_id"])
            await msg.edit(embed=_build_suggestion_embed(sug), view=None)
        except (discord.NotFound, discord.HTTPException):
            pass

    icon = "✅" if status == "approved" else "❌"
    await inter.response.send_message(
        embed=EmbedBuilder.success(f"Suggestion {icon}", f"**{sug_id_clean}** marked as **{status}**.\nNote: {reason}")
    )

    # DM the author
    try:
        author = await bot.fetch_user(sug["author_id"])
        dm_embed = EmbedBuilder.info(
            f"Your Suggestion Was {status.capitalize()}",
            f"**Suggestion {sug_id_clean}:** {sug['content'][:200]}\n\n**Staff note:** {reason}",
            color=EMBED_COLOR_SUCCESS if status == "approved" else EMBED_COLOR_ERROR,
        )
        await send_dm(author, embed=dm_embed)
    except Exception:
        pass

bot.tree.add_command(suggest_group)


# =============================================================================
# §30 RUNNER — Execution Entry Point
# =============================================================================

if __name__ == "__main__":
    """
    GUIDE: This block only runs when you execute this file directly.
    Never call bot.run() inside a function or cog.

    DEVELOPMENT TIPS:
    ─────────────────────────────────────────────────────────────
    • Sync to ONE guild for instant slash command updates during dev:
        TEST_GUILD = discord.Object(id=YOUR_GUILD_ID)
        bot.tree.copy_global_to(guild=TEST_GUILD)
        await bot.tree.sync(guild=TEST_GUILD)
      Add this to setup_hook instead of the global sync.

    • Keep your token in .env, NEVER hardcode it.

    • Use Python 3.10+ for match/case support and better async behavior.

    • discord.py 2.x requires Python 3.8+ (3.10+ recommended).

    • Run with:  python discord-bot-master-reference.py

    PRODUCTION CHECKLIST:
    ─────────────────────────────────────────────────────────────
    ✅  Token in .env, not in code
    ✅  Only privileged intents you actually use are enabled
    ✅  Persistent views registered in setup_hook
    ✅  Global slash command sync only when schema changes
    ✅  Error handling covers discord.Forbidden everywhere you make API calls
    ✅  Rate limits respected (don't mass-send messages in loops without sleep)
    ✅  Bot has only the Discord permissions it needs (principle of least privilege)
    ✅  Log channel set for audit trail
    ✅  Autosave running for JSON DB, or SQLite WAL mode enabled
    ✅  Bot does not respond to itself (if message.author.bot: return)
    ✅  All user inputs validated / clamped before use
    """

    if not validate_environment():
        exit(1)

    logger.info("🚀 Starting Master Bot...")
    bot.run(TOKEN, log_handler=None)  # log_handler=None = use our custom logger
