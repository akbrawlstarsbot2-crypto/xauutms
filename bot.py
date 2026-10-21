import logging
import re

import discord
from discord.ext import commands

from utils.config import Settings, load_settings
from utils.storage import init_db

# Quick customization options:
# - Add or remove cogs in ENABLED_EXTENSIONS.
# - Uncomment optional intent flags if your features need them.
# - Change DEFAULT_PRESENCE_TEXT to match your project branding.
# - Uncomment the optional event stubs at the bottom to extend behavior quickly.
ENABLED_EXTENSIONS = (
    "cogs.general",
    "cogs.admin",
    "cogs.fun",
    "cogs.community",
    "cogs.moderation",
    "cogs.economy",
    "cogs.levels",
    "cogs.tickets",
    "cogs.suggestions",
    "cogs.starboard",
    "cogs.stats",
    "cogs.music",
)

DEFAULT_PRESENCE_TEXT = "XAU Marks The Spot | /help"

# Optional presence examples (uncomment one in on_ready):
# await self.change_presence(activity=discord.Game("Use /help to get started"))
# await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="/help"))
# await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="your server"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("XauMarksTheSpot")


class XauMarksTheSpot(commands.Bot):
    def __init__(self, settings: Settings):
        intents = discord.Intents.default()

        # Core intents used by this template.
        intents.guilds = True
        intents.messages = True
        intents.message_content = True
        intents.members = True
        init_db()

        # Optional intent toggles (uncomment if your bot needs these).
        # intents.reactions = True
        # intents.typing = False
        # intents.presences = True  # Requires privileged intent in Discord developer portal.

        super().__init__(
            command_prefix=settings.prefix,
            intents=intents,
            help_command=None,
        )
        self.settings = settings

    async def setup_hook(self) -> None:
        for extension in ENABLED_EXTENSIONS:
            try:
                await self.load_extension(extension)
                logger.info("Loaded extension: %s", extension)
            except Exception:
                logger.exception("Failed to load extension: %s", extension)

        if self.settings.test_guild_id:
            guild = discord.Object(id=self.settings.test_guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            logger.info("Synced commands to test guild %s", self.settings.test_guild_id)
        else:
            await self.tree.sync()
            logger.info("Synced commands globally")

    async def on_ready(self) -> None:
        if self.user is None:
            return
        logger.info("Logged in as %s (%s)", self.user, self.user.id)
        await self.change_presence(activity=discord.Game(DEFAULT_PRESENCE_TEXT))

    async def on_message(self, message: discord.Message) -> None:
        # Ignore bots to prevent reply loops.
        if message.author.bot:
            return

        # Only respond to the bot's creator when they mention the bot.
        creator_id = 768837002069409863
        if (
            message.author.id == creator_id
            and self.user is not None
            and self.user in message.mentions
        ):
            # Remove the bot mention, then normalize punctuation and spacing.
            prompt = re.sub(r"<@!?\d+>", "", message.content)
            prompt = re.sub(r"[^a-z0-9' ]+", " ", prompt.lower())
            prompt = " ".join(prompt.split())
            if prompt in {"whos your daddy", "who's your daddy", "who is your daddy"}:
                await message.reply("You are, ak!", mention_author=False)
            elif prompt in {"whos your owner", "who's your owner", "who is your owner"}:
                await message.reply("You are, ak!", mention_author=False)
            else:
                await message.reply("hello creator!", mention_author=False)

        # Preserve prefix-command processing.
        await self.process_commands(message)

    # Optional quick stubs (uncomment and customize):
    # async def on_guild_join(self, guild: discord.Guild) -> None:
    #     logger.info("Joined guild: %s (%s)", guild.name, guild.id)

    # async def on_guild_remove(self, guild: discord.Guild) -> None:
    #     logger.info("Removed from guild: %s (%s)", guild.name, guild.id)

    # async def on_command_error(self, ctx: commands.Context, error: Exception) -> None:
    #     logger.exception("Command error in %s: %s", ctx.command, error)

    # async def on_message(self, message: discord.Message) -> None:
    #     if message.author.bot:
    #         return
    #     # Add custom message handling here, then keep command processing.
    #     await self.process_commands(message)


if __name__ == "__main__":
    settings = load_settings()
    bot = XauMarksTheSpot(settings)
    bot.run(settings.token, log_handler=None)
