import discord
from discord.ext import commands
from helpers.ai_helper import get_ai_response
from config import bot  # Import the bot instance from config.py

class ChatCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.tree.command(name="ask", description="Ask a question to the AI assistant")
    async def ask(self, interaction: discord.Interaction, *, question: str):
        """Ask the AI a question and get a response."""
        response = await get_ai_response(question)
        await interaction.response.send_message(response)

async def setup(bot):
    await bot.add_cog(ChatCommands(bot))
