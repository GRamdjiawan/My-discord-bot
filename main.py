import settings
import discord
import asyncio
import datetime
import random_topic
from discord.ext import commands

def run():
    now = datetime.datetime.now()
    specific_user_id = settings.DISCORD_USER
    channel_id = settings.DISCORD_CHANNEL
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"{bot.user} is ready")
        bot.loop.create_task(send_dm_based_on_time(specific_user_id, "Het weetje van vandaag is?", 20, 0))

    async def send_dm_based_on_time(user_id, message_content, hour, minute):
        topic = random_topic.get_topic()
        while True:
            current_time = datetime.datetime.now().time()
            if current_time.hour == hour and current_time.minute == minute:
                try:
                    channel = await bot.fetch_channel(channel_id)
                    user = await bot.fetch_user(user_id)
                    await user.send(f"{message_content} - onderwerp: ({topic})")
                    def check(m):
                        return m.author == user and isinstance(m.channel, discord.DMChannel)

                    response = await bot.wait_for('message', check=check, timeout=600)
                    print(f"Received response from user {user_id}: {response.content}")
                    embed = discord.Embed(title="Weetje van Peetje", description=response.content, color=0x00ff00, timestamp=datetime.datetime.now())
                    await channel.send(embed=embed)

                except discord.errors.NotFound:
                    print(f"User with ID {user_id} not found.")
                except discord.errors.Forbidden:
                    print(f"Bot does not have permission to message user {user_id}.")
                break
            await asyncio.sleep(60)

    bot.run(settings.DISCORD_API_SECRET)


if __name__ == "__main__":
    run()