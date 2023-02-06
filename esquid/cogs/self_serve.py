import logging

from discord.ext import commands

# Setup logging
logger = logging.getLogger(__name__)


class SelfServe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(SelfServe(bot))
    logger.info("Loaded")
