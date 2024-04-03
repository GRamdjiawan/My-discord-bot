import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_API_SECRET = os.getenv("DISCORD_API_TOKEN")
DISCORD_USER = os.getenv("DISCORD_TARGET_USER")
DISCORD_CHANNEL = os.getenv("DISCORD_TARGET_CHANNEL")