import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from datetime import datetime, timezone

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OLLAMA_API_URL = os.getenv('OLLAMA_API_URL')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL')
GUILD_ID = os.getenv('GUILD_ID')
CHANNEL_ID = os.getenv('CHANNEL_ID')
PAL_ROLE_NAME = os.getenv('PAL_ROLE_NAME')
SPECIAL_ROLES = os.getenv('SPECIAL_ROLES').split(',')
MAX_RESPONSES = int(os.getenv('MAX_RESPONSES', 10))
THREAD_EXPIRATION_HOURS = int(os.getenv('THREAD_EXPIRATION_HOURS', 2))
ALLOWED_CHANNEL_ID = os.getenv('ALLOWED_CHANNEL_ID')
DESIGNATED_CHANNEL_ID = os.getenv('DESIGNATED_CHANNEL_ID')
APPLICATION_ID = os.getenv('APPLICATION_ID')

# Set up intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Ensure that the bot can read message content
intents.members = True  # Required for member-based interactions

class BotClient(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='/',
            intents=intents,
            application_id=APPLICATION_ID
        )
        self.startup_time = None

    async def setup_hook(self):
        """Called when the bot is ready to set up commands and other async tasks."""
        self.startup_time = datetime.now(timezone.utc)
        await self.load_extensions()
        print("Syncing slash commands...")
        await self.tree.sync()
        print("Slash commands synced!")

    async def load_extensions(self):
        for filename in os.listdir('./commands'):
            if filename.endswith('.py') and not filename.startswith('_'):
                try:
                    await self.load_extension(f'commands.{filename[:-3]}')
                    print(f'Loaded extension: {filename[:-3]}')
                except Exception as e:
                    print(f'Failed to load extension {filename[:-3]}: {str(e)}')

    async def on_ready(self):
        """Triggered when the bot is connected and ready."""
        print(f'Logged in as {self.user.name} (ID: {self.user.id})')
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.playing,
                name="In development, Don't mind me"
            )
        )

# Instantiate the bot
bot = BotClient()

# Global variables
response_counts = {}  # Keep track of user response counts
last_reset_time = None  # Placeholder for tracking resets (if needed)
