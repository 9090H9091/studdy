


# Studdy


A simple Discord bot with features like using ollama's api to send messages in such channel that is designated.

## How to Use

1. Clone the repository:
   ```bash
   git clone https://github.com/9090H9091/studdy.git
   ```

2. Navigate to the project directory:
   ```bash
   cd studdy
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3.1 Non pip install
   `For users on linux based distros, whom experience PIP not working`
   ```bash
   sudo apt install < requirements.txt
   ```
   

4. Edit the `.env` file and add your Discord bot token, Ollama port (default 11434), Selected llm, server, channel:
   ```plaintext
   DISCORD_TOKEN=YOUR_DISCORD_TOKEN
   DISCORD_TOKEN=PUT DISCORD TOKEN HERE
   OLLAMA_API_URL=http://127.0.0.1:11434  # URL of the Ollama API
   OLLAMA_MODEL=llama3.2:1b  # Model name for Ollama, Can change if you want
   GUILD_ID=HERE  # Discord server ID theres multiple cuz i fucked up, just put in the same channel id on all of them, it    doesnt matter
   CHANNEL_ID=HERE # Discord channel ID for bot usage 
   PAL_ROLE_NAME=pal  # Role name for "pal" role
   SPECIAL_ROLES=bud,buddy,buddiest  # Comma-separated special roles
   MAX_RESPONSES=10  # Maximum responses for "pal" role without special roles
   THREAD_EXPIRATION_HOURS=2
   ALLOWED_CHANNEL_ID=HERE
   DESIGNATED_CHANNEL_ID=HERE
   ```

5. Run the bot:
   ```bash
   python bot.py
   ```

The bot will now be running and responding to the available commands.
```


