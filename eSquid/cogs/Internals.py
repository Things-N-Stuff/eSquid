import discord
from discord import app_commands
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


class Internals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Load a cog")
    async def load_cog(self, interaction: discord.Interaction, cog: str):
        """Syncs CommandTree globally"""
        if interaction.user.id in self.bot.admins:
            await self.bot.load_extension(f"cogs.{cog}")
            await self.bot.tree.sync()
            await interaction.response.send_message(f"Loaded Cog: {cog}", ephemeral=True)
        else:
            await interaction.response.send_message("You are not a bot admin", ephemeral=True)

    @app_commands.command(description="Unload a cog")
    async def unload_cog(self, interaction: discord.Interaction, cog: str):
        """Syncs CommandTree globally"""
        if interaction.user.id in self.bot.admins:
            await self.bot.unload_extension(f"cogs.{cog}")
            await self.bot.tree.sync()
            await interaction.response.send_message(f"Unloaded Cog: {cog}", ephemeral=True)
        else:
            await interaction.response.send_message("You are not a bot admin", ephemeral=True)

    @app_commands.command(description="Reload a cog")
    async def reload_cog(self, interaction: discord.Interaction, cog: str):
        """Syncs CommandTree globally"""
        if interaction.user.id in self.bot.admins:
            await self.bot.reload_extension(f"cogs.{cog}")
            await self.bot.tree.sync()
            await interaction.response.send_message(f"Reloaded Cog: {cog}", ephemeral=True)
        else:
            await interaction.response.send_message("You are not a bot admin", ephemeral=True)

    @commands.command()
    async def sync(self, ctx: commands.Context):
        """Syncs CommandTree locally to current server"""
        if ctx.author.id in self.bot.admins:
            sync_guild = discord.Object(ctx.guild.id)
            self.bot.tree.copy_global_to(guild=sync_guild)
            await self.bot.tree.sync(guild=sync_guild)
            await ctx.message.add_reaction("✅")

    @commands.command()
    async def sync_global(self, ctx: commands.Context):
        """Syncs CommandTree globally"""
        if ctx.author.id in self.bot.admins:
            await self.bot.tree.sync()
            await ctx.message.add_reaction("✅")


async def setup(bot):
    await bot.add_cog(Internals(bot))
    logger.info("Loaded")
