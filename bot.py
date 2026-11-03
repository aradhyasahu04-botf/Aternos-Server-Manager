import os
import discord
from discord.ext import commands
from python_aternos import Client

# Configuration - Loaded securely from environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ATERNOS_SESSION = os.getenv("ATERNOS_SESSION")
SERVER_INDEX = int(os.getenv("SERVER_INDEX", 0))

# Optional: Replace with your actual Discord text channel ID to restrict commands
ALLOWED_CHANNEL_ID = None  # Example: 123456789012345678

# Enable Privileged Message Content Intent so the bot can read commands
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def get_aternos_server():
    """Logs into Aternos using the browser session cookie and retrieves the target server."""
    if not ATERNOS_SESSION:
        print("ERROR: ATERNOS_SESSION environment variable is missing!")
        raise Exception("ATERNOS_SESSION is not set in environment variables.")
    
    print("LOG: Attempting to log into Aternos using session cookie...")
    aternos_client = Client()
    aternos_client.login_with_session(ATERNOS_SESSION)
    
    print("LOG: Fetching server list from Aternos...")
    servers = aternos_client.account.list_servers()
    if not servers:
        print("ERROR: No servers found on this Aternos account.")
        raise Exception("No servers found on this Aternos account.")
    
    target_server = servers[SERVER_INDEX]
    print(f"LOG: Target server loaded successfully: {target_server.address} (Status: {target_server.status})")
    return target_server

@bot.event
async def on_ready():
    print(f"========================================")
    print(f" SUCCESS: Bot is online as {bot.user}")
    print(f" Command Prefix: '!'")
    print(f" Listening for commands...")
    print(f"========================================")

@bot.command(name="start")
async def start_server(ctx):
    """Command to start the Aternos server."""
    print(f"COMMAND EXECUTED: !start by {ctx.author} (Channel: {ctx.channel.name})")
    
    if ALLOWED_CHANNEL_ID and ctx.channel.id != ALLOWED_CHANNEL_ID:
