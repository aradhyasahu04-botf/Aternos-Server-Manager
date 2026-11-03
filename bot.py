import os
import discord
from discord.ext import commands
from python_aternos import Client

# Configuration - Loaded securely from environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ATERNOS_SESSION = os.getenv("ATERNOS_SESSION")  # Paste your cookie value here or set it in your panel
SERVER_INDEX = int(os.getenv("SERVER_INDEX", 0))

# Optional: Replace with your actual Discord text channel ID if you want to restrict commands.
ALLOWED_CHANNEL_ID = None  # Example: 123456789012345678

# Enable Privileged Message Content Intent so the bot can read commands
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def get_aternos_server():
    """Logs into Aternos using the browser session cookie and retrieves the target server."""
    if not ATERNOS_SESSION:
        raise Exception("ATERNOS_SESSION is not set in environment variables.")
    
    aternos_client = Client()
    # Log in using the session cookie value you copied from Chrome
    aternos_client.login_with_session(ATERNOS_SESSION)
    
    servers = aternos_client.account.list_servers()
    if not servers:
        raise Exception("No servers found on this Aternos account.")
    return servers[SERVER_INDEX]

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.command(name="start")
async def start_server(ctx):
    """Command to start the Aternos server."""
    print(f"COMMAND RECEIVED: !start invoked by {ctx.author}")  # This will show up in your Bot-Hosting console
    
    if ALLOWED_CHANNEL_ID and ctx.channel.id != ALLOWED_CHANNEL_ID:
        await ctx.send(f"❌ You can only use this command in <#{ALLOWED_CHANNEL_ID}>!", delete_after=5)
        return

    await ctx.send("⌛ Connecting to Aternos and starting the server...")
    try:
        server = get_aternos_server()
        print(f"Successfully retrieved Aternos server status: {server.status}") # Console log
        
        if server.status == "online":
            await ctx.send("🟢 Server is already online!")
            return
        elif server.status == "starting":
            await ctx.send("🟡 Server is already starting or in queue!")
            return

        server.start()
        await ctx.send("🚀 **Server start command sent!** It may take a few minutes to boot up.")
    except Exception as e:
        print(f"ERROR starting server: {e}") # Console log for debugging
        await ctx.send(f"❌ Error: {e}")

@bot.command(name="status")
async def server_status(ctx):
    """Command to check server status."""
    if ALLOWED_CHANNEL_ID and ctx.channel.id != ALLOWED_CHANNEL_ID:
        await ctx.send(f"❌ You can only use this command in <#{ALLOWED_CHANNEL_ID}>!", delete_after=5)
        return

    try:
        server = get_aternos_server()
        await ctx.send(f"📊 **Server Status:** `{server.status}` | **Players:** {server.players_count}/{server.slots}")
    except Exception as e:
        await ctx.send(f"❌ Error fetching status: {e}")

@bot.command(name="stop")
async def stop_server(ctx):
    """Command to stop the server."""
    if ALLOWED_CHANNEL_ID and ctx.channel.id != ALLOWED_CHANNEL_ID:
        await ctx.send(f"❌ You can only use this command in <#{ALLOWED_CHANNEL_ID}>!", delete_after=5)
        return

    try:
        server = get_aternos_server()
        server.stop()
        await ctx.send("🛑 Server stop signal sent.")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("❌ Error: DISCORD_TOKEN environment variable is missing.")
    else:
        bot.run(DISCORD_TOKEN)
