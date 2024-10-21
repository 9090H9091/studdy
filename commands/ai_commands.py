import discord
from discord.ext import commands
from discord import app_commands
from ai.ai import get_ai_response
from helpers.rate_limit import RateLimiter
from helpers.logger import get_logger

logger = get_logger(__name__)

class AICommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rate_limiter = RateLimiter()
        self.user_threads = {}

    @app_commands.command(name="chat", description="Start a private chat with the AI assistant")
    async def chat(self, interaction: discord.Interaction):
        if not self.rate_limiter.can_process(interaction.user.id):
            await interaction.response.send_message("Please wait before using this command again.", ephemeral=True)
            return

        try:
            thread = await self._create_or_get_thread(interaction)
            if thread:
                await interaction.response.send_message(
                    f"Continue our conversation here: {thread.mention}", 
                    ephemeral=True
                )
        except Exception as e:
            logger.error(f"Error in chat command: {e}")
            await interaction.response.send_message("An error occurred. Please try again later.", ephemeral=True)

    @app_commands.command(name="ask", description="Ask a question to the AI assistant")
    async def ask(self, interaction: discord.Interaction, question: str):
        if not self.rate_limiter.can_process(interaction.user.id):
            await interaction.response.send_message("Please wait before using this command again.", ephemeral=True)
            return

        await interaction.response.defer(thinking=True)
        try:
            response = await get_ai_response(question)
            thread = self.user_threads.get(interaction.user.id)
            
            if thread:
                await thread.send(f"**Question:** {question}\n**Response:** {response}")
                await interaction.followup.send(f"Response sent to your thread: {thread.mention}", ephemeral=True)
            else:
                await interaction.followup.send(response)
        except Exception as e:
            logger.error(f"Error in ask command: {e}")
            await interaction.followup.send("An error occurred. Please try again later.", ephemeral=True)

    async def _create_or_get_thread(self, interaction: discord.Interaction):
        if interaction.user.id in self.user_threads:
            return self.user_threads[interaction.user.id]

        thread = await interaction.channel.create_thread(
            name=f"AI Chat - {interaction.user.name}",
            type=discord.ChannelType.private_thread,
            auto_archive_duration=1440  # 24 hours
        )
        
        self.user_threads[interaction.user.id] = thread
        await thread.add_user(interaction.user)
        
        # Send welcome message
        embed = discord.Embed(
            title="Welcome to Your AI Chat",
            description="I'm here to help you with your questions!",
            color=discord.Color.blue()
        )
        await thread.send(embed=embed)
        
        return thread

async def setup(bot):
    await bot.add_cog(AICommands(bot))
