from pathlib import Path

import discord
from discord.ext import commands

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

l_handler = logging.StreamHandler()
l_handler.setLevel(logging.INFO)

l_format = logging.Formatter(
    fmt="%(asctime)s %(levelname)-8s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
l_handler.setFormatter(l_format)
logger.addHandler(l_handler)


class ESquid(commands.Bot):
    def __init__(
        self,
        admins_ids: tuple[int, ...],
        initial_cogs: tuple[str, ...],
        testing_guild_id: int | None = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.initial_cogs = initial_cogs
        self.admins = admins_ids
        self.testing_guild = testing_guild_id

    async def setup_hook(self):
        # Load intial cogs
        for cog in self.initial_cogs:
            await self.load_extension(f"cogs.{cog}")

        # Sync app commands to the testing guild if provided
        if self.testing_guild:
            guild = discord.Object(self.testing_guild)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)

    async def on_ready(self):
        logger.info(f"Ready as {self.user} (ID = {self.user.id})")
        logger.info(f"Serving {len(self.guilds)} guild(s)")


if __name__ == "__main__":
    # Get bot token, testing guild, and bot admins
    token = Path("./.bot_token").read_text()
    guild = int(Path("./.testing_guild_id").read_text())

    bot_admins = []
    with Path("./.bot_admin_ids").open("r") as f:
        bot_admins.append(int(f.readline()))


    # Setup bot
    intents = discord.Intents.default()
    cogs = ("Internals", "Fun", "Moderation", "SelfServe")
    bot = ESquid(
        admins_ids=tuple(bot_admins),
        initial_cogs=cogs,
        testing_guild_id=guild,
        command_prefix=commands.when_mentioned,
        intents=intents,
    )

    # Run bot
    bot.run(token)
