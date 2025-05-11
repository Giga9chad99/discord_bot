import disnake
from disnake.ext import commands
import json
import os

PREFIXES_FILE = "data/prefix.json"

def load_prefixes():
    if os.path.exists(PREFIXES_FILE):
        with open(PREFIXES_FILE, "r") as f:
            return json.load(f)
    return {}

def save_prefixes(prefixes):
    os.makedirs(os.path.dirname(PREFIXES_FILE), exist_ok=True)
    with open(PREFIXES_FILE, "w") as f:
        json.dump(prefixes, f, indent=4)

prefixes = load_prefixes()

def get_prefix(bot, message):
    guild_id = str(message.guild.id) if message.guild else "default"
    return prefixes.get(guild_id, "$")

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"Zalogowano jako {bot.user.name} ({bot.user.id})")
    await bot.change_presence(activity=disnake.Game(name="$help"))

@bot.command()
@commands.has_permissions(administrator=True)
async def setprefix(ctx, new_prefix: str):
    guild_id = str(ctx.guild.id)
    prefixes[guild_id] = new_prefix
    save_prefixes(prefixes)
    await ctx.send(f"Prefix ustawiony na `{new_prefix}`")

initial_extensions = [
    "cogs.admin",
    "cogs.economy",
    "cogs.fun",
    "cogs.help",
    "cogs.utils",
    "cogs.welcome"
]

for ext in initial_extensions:
    try:
        bot.load_extension(ext)
        print(f"Zaladowano {ext}")
    except Exception as e:
        print(f"Błąd ładowania {ext}: {e}")
bot.run("TOKEN")