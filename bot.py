
   import os
import discord
from discord.ext import commands
from py_aternos import Client

# Configuration - Loaded securely from environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ATERNOS_SESSION = os.getenv("ATERNOS_SESSION")
SERVER_INDEX = int(os.getenv("SERVER_INDEX", 0))

# Optional: Restrict commands to a specific channel ID (Leave None for all channels)
ALLOWED_CHANNEL_ID = None  

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def get_aternos_server():
    """Logs into Aternos using the py-aternos client and your session cookie."""
    if not ATERNOS_SESSION:
        raise Exception("ATERNOS_SESSION is not set in environment variables.")
    
    print("LOG: Initializing py-aternos client...")
    aternos_client = Client()
    aternos_client.login_with_session(ATERNOS_SESSION)
    
    servers = aternos_client.account.list_servers()
    if not servers:
        raise Exception("No servers found on this Aternos account.")
    
    return servers[SERVER_INDEX]

@bot.event
async def on_ready():
    print(f"========================================")
    print(f" SUCCESS: Bot is online as {bot.user}")
    print(f" Command Prefix: '!'")
    print(f"========================================")

@bot.command(name="start")
async def start_server(ctx):
    print(f"COMMAND EXECUTED: !start by {ctx.author}")
    
    if ALLOWED_CHANNEL_ID and ctx.channel.id != ALLOWED_CHANNEL_ID:
        await ctx.send(f"❌ You can only use this command in <#{ALLOWED_CHANNEL_ID}>!", delete_after=5)
        return

    await ctx.send("⌛ Connecting to Aternos...")
    try:
        server = get_aternos_server()
        if server.status == "online":
            await ctx.send("🟢 Server is already online!")
            return
        elif server.status == "starting":
            await ctx.send("🟡 Server is already starting!")
            return
            
        server.start()
        print("SUCCESS: Start signal sent successfully via py-aternos.")
        await ctx.send("🚀 **Server start command sent successfully!**")
    except Exception as e:
        print(f"EXCEPT: Failed to start - {e}")
        await ctx.send(f"❌ Error: {e}")

@bot.command(name="status")
async def server_status(ctx):
    print(f"COMMAND EXECUTED: !status by {ctx.author}")
    
    if ALLOWED_CHANNEL_ID and ctx.channel.id != ALLOWED_CHANNEL_ID:
        await ctx.send(f"❌ You can only use this command in <#{ALLOWED_CHANNEL_ID}>!", delete_after=5)
        return

    try:
        server = get_aternos_server()
        status_msg = f"📊 **Server Status:** `{server.status}` | **Players:** {server.players_count}/{server.slots}"
        print(f"STATUS REPORT: {server.status} ({server.players_count}/{server.slots} players)")
        await ctx.send(status_msg)
    except Exception as e:
        print(f"EXCEPT: Failed to fetch status - {e}")
        await ctx.send(f"❌ Error fetching status: {e}")

@bot.command(name="stop")
async def stop_server(ctx):
    print(f"COMMAND EXECUTED: !stop by {ctx.author}")
    
    if ALLOWED_CHANNEL_ID and ctx.channel.id != ALLOWED_CHANNEL_ID:
        await ctx.send(f"❌ You can only use this command in <#{ALLOWED_CHANNEL_ID}>!", delete_after=5)
        return

    try:
        server = get_aternos_server()
        server.stop()
        print("SUCCESS: Stop signal sent successfully via py-aternos.")
        await ctx.send("🛑 Server stop signal sent.")
    except Exception as e:
        print(f"EXCEPT: Failed to stop - {e}")
        await ctx.send(f"❌ Error: {e}")

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("FATAL ERROR: DISCORD_TOKEN is missing.")
    else:
        print("LOG: Starting Discord client connection...")
        bot.run(DISCORD_TOKEN)
