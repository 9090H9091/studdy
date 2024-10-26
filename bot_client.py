import os
import discord
from discord.ext import commands
from datetime import datetime, timezone

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True

class BotClient(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='/',
            intents=intents,
            application_id=os.getenv('APPLICATION_ID')
        )

    async def setup_hook(self):
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
        print(f'Logged in as {self.user.name} (ID: {self.user.id})')
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.playing,
                name="In development, Don't mind me"
            )
        )
