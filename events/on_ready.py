from config import bot, response_counts, last_reset_time

@bot.event
async def on_ready():
    """Triggered when the bot is connected and ready."""
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print("Bot is ready!")
    # Any additional functionality for on_ready
