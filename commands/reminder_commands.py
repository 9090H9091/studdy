import discord
from discord.ext import commands
from discord import app_commands
from helpers.logger import get_logger

logger = get_logger(__name__)

class ReminderCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="remind", description="Set a reminder")
    async def remind(self, interaction: discord.Interaction, time: str, reminder: str):
        await interaction.response.send_message(f"I'll remind you about: {reminder} in {time}")
        # Add actual reminder functionality here

async def setup(bot):
    await bot.add_cog(ReminderCommands(bot))