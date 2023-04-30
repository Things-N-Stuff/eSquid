"""Internals Cog
Contains commands for bot developers

- load - load cogs
- unload - unload cogs
- reload - reload cogs
"""
import logging

import discord
from discord.ext import commands

# Setup logging
logger = logging.getLogger(__name__)


class Internals(commands.Cog):
    """Commands for bot developers"""

    def __init__(self, bot):
        self.bot = bot

    async def dm_error(self, user: discord.User | discord.Member, error: Exception, message: str = ""):
        """helper function to direct messeage errors to users"""
        logger.error(error)
        user_dm = await user.create_dm()
        await user_dm.send(f"{message}\n{error}")

    @commands.command(description="Load cogs", hidden=True)
    @commands.is_owner()
    async def load(self, ctx: commands.Context, *args):
        """Load cogs"""
        for cog in args:
            try:
                await self.bot.load_extension(f".cogs.{cog}", package="esquid")
            except Exception as err:
                await self.dm_error(ctx.author, err)

        await self.bot.tree.sync()
        await ctx.message.add_reaction("\N{SQUARED OK}")

    @commands.command(description="Unload cogs", hidden=True)
    @commands.is_owner()
    async def unload(self, ctx: commands.Context, *args):
        """Unload cogs"""
        for cog in args:
            try:
                await self.bot.unload_extension(f".cogs.{cog}", package="esquid")
            except Exception as err:
                await self.dm_error(ctx.author, err)

        await self.bot.tree.sync()
        await ctx.message.add_reaction("\N{SQUARED OK}")

    @commands.command(description="Reload cogs", hidden=True)
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, *args):
        """Reload cogs"""
        for cog in args:
            try:
                await self.bot.reload_extension(f".cogs.{cog}", package="esquid")
            except Exception as err:
                await self.dm_error(ctx.author, err)

        await self.bot.tree.sync()
        await ctx.message.add_reaction("\N{SQUARED OK}")


async def setup(bot):
    """Setup function for discord.py extensions"""
    await bot.add_cog(Internals(bot))
    logger.info("Loaded")
