import os
import discord
from discord.ext import commands, tasks
from datetime import datetime, timezone
from collections import defaultdict
from dotenv import load_dotenv
from .utils.helper import get_user_tier, create_private_thread, get_ollama_response

# Load environment variables
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))
DESIGNATED_CHANNEL_ID = int(os.getenv('DESIGNATED_CHANNEL_ID'))

# Initialize bot and global variables
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)

# Store user threads and response counts globally
bot.user_threads = {}
bot.response_counts = defaultdict(int)
bot.last_reset_time = datetime.now(timezone.utc)

# Reset response counts daily
@tasks.loop(hours=24)
async def reset_response_counts():
    bot.response_counts.clear()
    bot.last_reset_time = datetime.now(timezone.utc)
    print("Response counts have been reset.")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} and connected to Discord!')
    reset_response_counts.start()
    await bot.tree.sync()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.Thread) and message.channel.id in bot.user_threads.values():
        user_tier = get_user_tier(message.author)
        if user_tier == "Pal":
            bot.response_counts[message.author.id] += 1
            if bot.response_counts[message.author.id] > int(os.getenv('MAX_RESPONSES', 5)):
                await message.channel.send(f"You've reached your daily limit of {os.getenv('MAX_RESPONSES', 5)} responses. Please try again tomorrow.")
                return

        loading_emoji = discord.utils.get(message.guild.emojis, name="loading")
        async with message.channel.typing():
            initial_message = await message.channel.send(f"Generating response {loading_emoji}")
            response = await get_ollama_response(message.content, initial_message)
            await initial_message.edit(content=response)

# Load command extensions
async def load_extensions():
    await bot.load_extension('discord_bot.commands.moderation')
    await bot.load_extension('discord_bot.commands.fun')

def run_bot():
    asyncio.run(load_extensions())
    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    import asyncio
    run_bot()