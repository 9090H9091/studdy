from dotenv import load_dotenv
from config import bot, DISCORD_TOKEN

# Load the environment variables from the .env file
load_dotenv()

# Initialize and run the bot
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
