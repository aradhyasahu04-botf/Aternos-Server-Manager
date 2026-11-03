import os
import discord
from discord.ext import commands
import requests

# Configuration - Loaded securely from environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ATERNOS_SESSION = os.getenv("ATERNOS_SESSION")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def aternos_request(endpoint):
    """Sends a lightweight direct request to the Aternos panel using your session cookie."""
    if not ATERNOS_SESSION:
        raise Exception("ATERNOS_SESSION is not set in environment variables.")
        
    url = f"https://aternos.org/panel/ajax/{endpoint}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://aternos.org/server/",
        "Cookie": f"ATERNOS_SESSION={ATERNOS_SESSION}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Request error: {e}")
        return {"success": False, "error": str(e)}

@bot.event
async def on_ready():
    print(f"========================================")
    print(f" SUCCESS: Bot is online as {bot.user}")
    print(f" Command Prefix: '!'")
    print(f"========================================")

@bot.command(name="start")
async def start_server(ctx):
    print(f"COMMAND EXECUTED: !start by {ctx.author}")
    await ctx.send("⌛ Sending start signal to Aternos...")
    
    data = aternos_request("start.php")
    if data.get("success") or data.get("done") or not data.get("error"):
        print("SUCCESS: Start signal sent successfully.")
        await ctx.send("🚀 **Server start command sent successfully!**")
    else:
        err = data.get("error", "Unknown error")
        print(f"EXCEPT: Failed to start - {err}")
        await ctx.send(f"❌ Error starting server: {err}")

@bot.command(name="status")
async def server_status(ctx):
    print(f"COMMAND EXECUTED: !status by {ctx.author}")
    
    data = aternos_request("status.php")
    # Aternos status responses can vary slightly in structure, extract safely
    info = data if "status" in data else data.get("data", {})
    status = info.get("status", "unknown")
    players = info.get("players", 0)
    slots = info.get("slots", 0)
    
    print(f"STATUS REPORT: Status -> {status} ({players}/{slots} players)")
    await ctx.send(f"📊 **Server Status:** `{status}` | **Players:** `{players}/{slots}`")

@bot.command(name="stop")
async def stop_server(ctx):
    print(f"COMMAND EXECUTED: !stop by {ctx.author}")
    await ctx.send("🛑 Sending stop signal to Aternos...")
    
    data = aternos_request("stop.php")
    print("SUCCESS: Stop signal sent.")
    await ctx.send("🛑 Server stop signal sent.")

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("FATAL ERROR: DISCORD_TOKEN is missing.")
    else:
        print("LOG: Starting Discord client connection...")
        bot.run(DISCORD_TOKEN)
