from discord import app_commands, Interaction, utils
from helpers.ollama import get_ollama_response
from helpers.roles import has_role, get_user_tier
from config import ALLOWED_CHANNEL_ID, MAX_RESPONSES, SPECIAL_ROLES, PAL_ROLE_NAME, bot, response_counts, APPLICATION_ID

@bot.tree.command(name="ask", description="Ask a question to the AI assistant")
async def ask(interaction: Interaction, *, question: str):
    member = interaction.user
    if has_role(member, SPECIAL_ROLES):
        print(f'{member.display_name} has a special role and can chat freely.')
    elif has_role(member, [PAL_ROLE_NAME]):
        response_counts.setdefault(member.id, 0)
        if response_counts[member.id] >= MAX_RESPONSES:
            await interaction.response.send_message(f"You've reached your daily limit of {MAX_RESPONSES} responses.", ephemeral=True)
            return
        response_counts[member.id] += 1
        print(f'{member.display_name} has {MAX_RESPONSES - response_counts[member.id]} responses left today.')
    else:
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
        return

    await interaction.response.defer(thinking=True)

    loading_emoji = utils.get(interaction.guild.emojis, name="loading")
    thread_message = await interaction.followup.send(f"Generating response {loading_emoji}", wait=True)
    thread_response = await get_ollama_response(question, thread_message)

    final_message = f"{interaction.user.mention}\n\n{thread_response}"

    if len(final_message) > 2000:
        parts = [final_message[i:i+1900] for i in range(0, len(final_message), 1900)]
        await thread_message.edit(content=parts[0])
        for part in parts[1:]:
            await interaction.followup.send(part)
    else:
        await thread_message.edit(content=final_message)

def setup(bot):
    bot.add_command(ask)
