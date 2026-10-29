import discord
from discord.ext import commands
from python_aternos import Client, ClientError

# Configuration - Replace with your actual details
DISCORD_TOKEN = "YOUR_DISCORD_BOT_TOKEN"
ATERNOS_USERNAME = "YOUR_ATERNOS_USERNAME"
ATERNOS_PASSWORD = "YOUR_ATERNOS_PASSWORD"
SERVER_INDEX = 0  # 0 is your first server on Aternos

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

def get_aternos_server():
    """Logs into Aternos and retrieves the target server."""
    aternos_client = Client.from_credentials(ATERNOS_USERNAME, ATERNOS_PASSWORD)
    servers = aternos_client.list_servers()
    if not servers:
        raise Exception("No servers found on this Aternos account.")
    return servers[SERVER_INDEX]

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.command(name="start")
async def start_server(ctx):
    """Command to start the Aternos server."""
    await ctx.send("⌛ Connecting to Aternos and starting the server...")
    try:
        server = get_aternos_server()
        if server.status == "online":
            await ctx.send("🟢 Server is already online!")
            return
        elif server.status == "starting":
            await ctx.send("🟡 Server is already starting or in queue!")
            return

        server.start()
        await ctx.send("🚀 **Server start command sent!** It may take a few minutes to boot up.")
    except ClientError as e:
        await ctx.send(f"❌ Aternos Client Error: {e}")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@bot.command(name="status")
async def server_status(ctx):
    """Command to check server status."""
    try:
        server = get_aternos_server()
        await ctx.send(f"📊 **Server Status:** `{server.status}` | **Players:** {server.players_count}/{server.slots}")
    except Exception as e:
        await ctx.send(f"❌ Error fetching status: {e}")

@bot.command(name="stop")
async def stop_server(ctx):
    """Command to stop the server."""
    try:
        server = get_aternos_server()
        server.stop()
        await ctx.send("🛑 Server stop signal sent.")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

bot.run(DISCORD_TOKEN)
