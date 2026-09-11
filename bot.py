import discord

# pyrefly: ignore [missing-import]
import requests
import os
from discord.ext import commands
from dotenv import load_dotenv
import webbrowser

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)


def get_meme():
    try:
        response = requests.get("https://meme-api.com/gimme")
        response.raise_for_status()
        data = response.json()
        return data.get("url", "Could not fetch meme.")
    except Exception as e:
        return f"Error: {str(e)}"


@bot.event
async def on_ready():
    print(f"Logged on as {bot.user}!")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)


@bot.command(name="meme")
async def meme_command(ctx):
    """Fetches and sends a random meme."""
    meme_url = get_meme()
    await ctx.send(meme_url)


@bot.command(name="boykisser")
async def boykisser_command(ctx):
    """prints boykisser"""
    bk = """  
  ⣽⣿⣿⣿⣧⠀⠀⠀⠠⣤⣄⡀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⡆⠀
⢀⣿⣿⣿⣿⣿⣷⡀⠀⠀⢿⣿⣿⣦⡀⠀⣰⣿⣿⣿⣿⣿⣿⡇⠀
⢸⣿⣿⣿⣿⣿⣿⡿⠄⣠⣤⣿⣿⣿⣿⣄⣿⣿⣿⣿⣿⣿⣿⡇⠀
⢸⣿⣿⣿⣿⣿⣿⣤⣬⣭⣬⣬⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀
⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⠿⣿⣿⡿⠀⠀
⠀⠸⣿⣧⠀⣴⡆⠀⠀⢸⣿⣿⣿⣿⠀⠀⢸⣿⡌⣶⣿⠟⠁⠀⠀
⠀⠀⠹⡿⢸⣿⡇⠀⠀⢸⣿⣿⣿⣿⠀⠀⢈⣿⡇⢸⣯⣤⣤⠀⠀
⠙⣿⣿⣇⢸⣿⣇⠀⢀⣾⡿⢿⣿⣿⣀⣀⣼⣿⡇⣸⣿⡿⠁⠀⠀
⠀⢀⡟⡉⠞⢻⣿⣿⣿⣿⣶⣾⣿⣿⣿⣿⣿⠋⠘⣹⣿⡄⠀⠀⠀
⠀⣼⣿⣧⣶⣿⣿⣿⣟⠻⢋⣍⣉⣋⣼⣿⣿⣿⣶⢿⣿⣿⡄⠀⠀
⠀⠉⠉⠀⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠁⠀⠉⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠠⣬⣭⣽⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠙⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠼⢿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀"""
    await ctx.send(bk)


@bot.command(name="about")
async def about_command(ctx):
    """gives info about the bot"""
    await ctx.send(
        "i am divabot, boop beep\ni do random shit lol, boop beep\ni am so sigma"
    )


@bot.command(name="rickroll")
async def youtube_command(ctx):
    """rickroll!!"""
    print("you just got rickrolled!")
    webbrowser.open(
        "https://www.youtube.com/watch?v=wZMue5I8qn8&pp=ygUIcmlja3JvbGzSBwkJKAsBhyohjO8%3D"
    )


@bot.command(name="list")
async def list_command(ctx):
    """lists all commands"""
    commandlist = {
        "meme": "sends a random meme",
        "boykisser": "prints an ascii boykisser",
        "about": "a joke command",
        "rickroll": "rickroll parker",
    }

    max_cmd_len = max(len(cmd) for cmd in commandlist)

    for cmd, desc in commandlist.items():
        await ctx.send(f"{cmd:<{max_cmd_len}} | {desc}")


# pyrefly: ignore [bad-argument-type]
bot.run(TOKEN)
