import discord
from discord.ext import commands
from helpers.ai_helper import get_ai_response
from threads.private_thread import create_private_thread
from config import bot  # Import the bot instance from config.py

class ChatCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.tree.command(name="chat", description="Start a private chat with the AI assistant")
    async def chat(self, interaction: discord.Interaction):
        """Start a private chat with the AI assistant."""
        thread = await create_private_thread(interaction)
        await interaction.response.send_message(f"Private chat created! Please continue in {thread.mention}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ChatCommand(bot))
