from discord import Message
from helpers.ollama import get_ollama_response

async def on_message(message: Message):
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.Thread) and message.channel.type == discord.ChannelType.private_thread:
        loading_emoji = discord.utils.get(message.guild.emojis, name="loading")
        initial_message = await message.channel.send(f"Generating response {loading_emoji}")
        response = await get_ollama_response(message.content, initial_message)
        await initial_message.edit(content=f"{message.author.mention}, here's the response:\n{response}")
