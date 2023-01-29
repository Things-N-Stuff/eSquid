import logging

from discord.ext import commands

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

l_handler = logging.StreamHandler()
l_handler.setLevel(logging.INFO)

l_format = logging.Formatter(
    fmt="%(asctime)s %(levelname)-8s %(name)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
l_handler.setFormatter(l_format)
logger.addHandler(l_handler)


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Fun(bot))
