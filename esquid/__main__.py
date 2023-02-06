"""Entry point for eSquid"""
import logging
from pathlib import Path

import discord
from discord.ext import commands

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)


class Esquid(commands.Bot):
    """Setup bot"""

    def __init__(
        self,
        *args,
        initial_cogs: tuple[str, ...],
        testing_guild_id: int | None = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.initial_cogs = initial_cogs
        self.testing_guild = testing_guild_id

    async def setup_hook(self):
        """Setup and sync cogs"""
        # Load intial cogs
        for cog in self.initial_cogs:
            await self.load_extension(f"cogs.{cog}")

        # Sync app commands to the testing guild if provided
        if self.testing_guild:
            guild = discord.Object(self.testing_guild)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)

    async def on_ready(self):
        """Provide information when ready"""
        logger.info("Ready as %s (ID = %d)", self.user, self.user.id)
        logger.info("Serving %d guild(s)", len(self.guilds))


# Get bot token, testing guild, and bot admins
token = Path(".bot_token").read_text(encoding="utf-8")
testing_guild = int(Path(".testing_guild_id").read_text(encoding="utf-8"))

bot_admins = []
with Path(".bot_admin_ids").open("r", encoding="utf-8") as f:
    bot_admins.append(int(f.readline()))


# Setup bot
intents = discord.Intents.default()
cogs = ("internals", "fun", "moderation", "self_serve")
bot = Esquid(
    owner_ids=set(bot_admins),
    initial_cogs=cogs,
    testing_guild_id=testing_guild,
    command_prefix=commands.when_mentioned,
    intents=intents,
)

# Run bot
bot.run(token)
