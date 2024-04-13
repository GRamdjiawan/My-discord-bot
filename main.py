import discord
from discord.ext import commands
import pytz
import asyncio
import datetime
from my_lib import settings
from my_lib import random_topic
from my_lib import Clear_cache

def run():
    amsterdam_timezone = pytz.timezone('Europe/Amsterdam')
    hour = 20
    specific_user_id = settings.DISCORD_USER
    channel_id = settings.DISCORD_CHANNEL
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        log = await bot.fetch_channel(settings.DISCORD_LOG)
        current_time = datetime.datetime.now(amsterdam_timezone).time().strftime("%H:%M:%S")
        await log.send(f"✅ - connected: {current_time}")
        bot.loop.create_task(send_dm_based_on_time(specific_user_id, "Het weetje van vandaag is?", hour))
    
    async def send_dm_based_on_time(user_id, message_content, hour):
        log = await bot.fetch_channel(settings.DISCORD_LOG)
        topic = random_topic.get_topic()
        fact_send = False
        while True:
            current_time_timedate = datetime.datetime.now(amsterdam_timezone).time()
            if current_time_timedate.minute == 0 and current_time_timedate.second == 0:
                try:
                    current_time = datetime.datetime.now(amsterdam_timezone).time().strftime("%H:%M:%S")
                    await log.send(f"✅ - {current_time}: on")
                    if current_time_timedate.hour == hour and current_time_timedate.minute == 0 and not fact_send:
                        fact_send = True               
                        try:
                            channel = await bot.fetch_channel(channel_id)
                            user = await bot.fetch_user(user_id)
                            await log.send(f"✅ - {current_time}: Message sent to {user.display_name}")
                            await user.send(f"{message_content} - onderwerp: [{topic}] - (weetje van peetje gemist? type: ?wvp)")
                            def check(m):
                                return m.author == user and isinstance(m.channel, discord.DMChannel)
                            response = await bot.wait_for('message', check=check, timeout=900)

                            if not response:
                                await log.send(f"⛔ - {current_time}: Message ignored")

                            await log.send(f"✅ - {current_time}: {user.display_name}: {response.content}")
                            embed = discord.Embed(title="Weetje van Peetje", description=response.content, color=0x00ff00, timestamp=datetime.datetime.now())
                            await channel.send(embed=embed)
                        except discord.errors.NotFound:
                            await log.send(f"⛔ - {current_time}: User with ID {user_id} not found.")
                            break
                        except discord.errors.Forbidden:
                            await log.send(f"⛔ - {current_time}: Bot does not have permission to message user {user_id}.")
                            break
                    elif current_time_timedate.hour > 20:
                        fact_send = False
                except Exception as e:
                    await log.send(f"⛔ - {current_time}: {e}")
                await asyncio.sleep(3600)
            else:
                await asyncio.sleep(60)

    @bot.event
    async def on_message(message):
        log = await bot.fetch_channel(settings.DISCORD_LOG)
        if message.author == bot.user:  
            return
        if isinstance(message.channel, discord.DMChannel):
            current_time = datetime.datetime.now(amsterdam_timezone).time().strftime("%H:%M:%S")
            if message.content == "?wvp":
                await message.author.send("Het weetje van peetje is? (stuur het weetje hieronder)")
                def check(m):
                    return m.author == message.author and m.channel == message.channel
                try:
                    channel = await bot.fetch_channel(channel_id)
                    user = await bot.fetch_user(specific_user_id)
                    response = await bot.wait_for('message', check=check, timeout=900)
                    await log.send(f"✅ - {current_time}: {user.display_name}: {response.content}")
                    embed = discord.Embed(title="Weetje van Peetje", description=response.content, color=0x00ff00, timestamp=datetime.datetime.now())
                    await channel.send(embed=embed)
                except asyncio.TimeoutError:
                    await message.author.send("You took too long to respond.")
    bot.run(settings.DISCORD_API_SECRET)

if __name__ == "__main__":
    Clear_cache.Clear_cache()
    run()