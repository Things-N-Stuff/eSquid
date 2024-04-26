"""Entry point for eSquid"""
import argparse
import logging
import os
import sys
from pathlib import Path

import discord
from discord.ext import commands


def main():
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
                await self.load_extension(f".cogs.{cog}", package="esquid")

            # Sync app commands to the testing guild if provided
            if self.testing_guild:
                guild = discord.Object(self.testing_guild)
                self.tree.copy_global_to(guild=guild)
                await self.tree.sync(guild=guild)

            if not self.testing_guild:
                await self.tree.sync()

        async def on_ready(self):
            """Provide information when ready"""
            logger.info("Ready as %s (ID = %d)", self.user, self.user.id)
            logger.info("Serving %d guild(s)", len(self.guilds))

    token: str | None = None
    testing_guild: int | None = None
    admin_ids: list[int] | None = None
    data_dir: str | os.PathLike = Path("./")

    # Parse arguments for token, guild, and admin ids
    parser = argparse.ArgumentParser(description="Quality of life discord bot for small servers")
    parser.add_argument("-a", "--admins", help="Comma seperated list of user ids for bot admins")
    parser.add_argument("-d", "--data", help="Directory to contain bot data")
    parser.add_argument("-g", "--guild", help="Testing guild to add commands to")
    parser.add_argument("-t", "--token", help="Token for the Discord bot")
    args = parser.parse_args()

    # If the token, guild, or admin ids weren't given as arguments, use environment variables
    ids = args.admins if args.admins is not None else os.environ.get("ESQUID_ADMINS")
    admin_ids = list(ids.split(",")) if ids is not None else None

    if args.data is not None:
        data_dir = Path(args.data)
    elif (env := os.environ.get("ESQUID_DATA_DIR")) is not None:
        data_dir = Path(env)

    testing_guild = args.guild if args.guild is not None else os.environ.get("ESQUID_TESTING_GUILD")
    token = args.token if args.token is not None else os.environ.get("ESQUID_TOKEN")

    # If neither arguments or environment variables are available, use files
    admin_ids_file = data_dir / ".admin_ids"
    testing_guild_file = data_dir / ".testing_guild_id"
    token_file = data_dir / ".bot_token"

    if admin_ids_file.exists() and admin_ids is None:
        ids_list = admin_ids_file.read_text(encoding="utf-8").strip().split("\n")
        admin_ids = [int(id.strip()) for id in ids_list]

    if token_file.exists() and token is None:
        token = token_file.read_text(encoding="utf-8")

    if testing_guild_file.exists() and testing_guild is None:
        testing_guild = testing_guild_file.read_text(encoding="utf-8")

    # If we still don't have a token, guild, or admin ids then exit
    if token is None:
        logger.critical("Unable to start bot")
        logger.critical("Missing token")
        logger.critical(f"token: {token}")
        logger.critical(f"guild: {testing_guild}")
        logger.critical(f"admin_ids: {admin_ids}")
        sys.exit(1)

    # Setup bot
    intents = discord.Intents.default()
    intents.members = True
    cogs = ("internals", "fun", "moderation", "self_serve")
    bot = Esquid(
        owner_ids=set(admin_ids) if admin_ids else None,
        initial_cogs=cogs,
        testing_guild_id=testing_guild if testing_guild else None,
        command_prefix=commands.when_mentioned,
        intents=intents,
    )

    # Run bot
    bot.run(token)


if __name__ == "__main__":
    main()
