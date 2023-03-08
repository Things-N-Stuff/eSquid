"""Self Serve Coge
Contains commands for users to serve themselves

color - apply any hex color to yourself
"""
import logging
from typing import cast

import discord
from discord import app_commands
from discord.ext import commands

# Setup logging
logger = logging.getLogger(__name__)


class SelfServe(commands.Cog):
    """Commands for users to serve themselves"""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Pick a color to apply to your name")
    @app_commands.describe(color="HEX color to apply")
    async def color(self, interaction: discord.Interaction, color: str):
        # Normalize hex value to #XXXXXX
        color = color.lower() if color.startswith("#") else f"#{color.lower()}"
        role_name = f"eSquid_{color}"

        # Turn input color into a discord color
        try:
            role_color = discord.Color.from_str(color)
        except ValueError as err:
            await interaction.response.send_message(f"{err}, '{color}'", ephemeral=True)
            return

        # Grab the guild and user
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message(
                "Command available ONLY in guilds", ephemeral=True
            )
            return

        user = cast(discord.Member, interaction.user)

        # Get the current color roles that the user has
        current_color_roles = tuple(
            filter(lambda role: role.name.startswith("eSquid_"), user.roles)
        )

        # Check if the color role is already assigned to the user
        if role_name in tuple(map(lambda role: role.name, current_color_roles)):
            await interaction.response.send_message(f"{color} is already assigned", ephemeral=True)
            return

        try:
            # Create the color role if it doesn't already exist
            maybe_role: tuple[discord.Role, ...] | None = tuple(
                filter(lambda role: role.name == role_name, guild.roles)
            )

            new_role: discord.Role = (
                await guild.create_role(
                    name=role_name, color=role_color, reason="eSquid color command"
                )
                if not maybe_role
                else maybe_role[0]
            )

            # Remove the user's current color roles
            await user.remove_roles(*current_color_roles, reason="eSquid color command")

            # Add the new color role
            await user.add_roles(new_role, reason="eSquid color command")
        except discord.Forbidden as err:
            await interaction.response.send_message(f"{err}", ephemeral=True)
            return

        await interaction.response.send_message(f"Assigned color, {color}", ephemeral=True)

        # Remove roles with no members
        empty_color_roles = tuple(
            filter(
                lambda role: role.name.startswith("eSquid_#") and len(role.members) == 0,
                guild.roles,
            )
        )

        for role in empty_color_roles:
            await role.delete(reason="eSquid color role clean up")


async def setup(bot):
    """Setup function for discord.py extensions."""
    await bot.add_cog(SelfServe(bot))
    logger.info("Loaded")
