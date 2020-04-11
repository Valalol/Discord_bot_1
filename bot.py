
import discord, logging, json, os
from discord.ext import commands

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

def get_prefix(client, message):
    with open('prefixes.json','r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_guild_join(guild):
    with open('prefixes.json','r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '?'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)

@client.event
async def on_guild_remove(guild):
    with open('prefixes.json','r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))
    
    with open('prefixes.json','w') as f:
        json.dump(prefixes, f, indent = 4)

@client.command()
@commands.is_owner()
async def changeprefix(ctx, prefix):
    """Permet de changer le préfixe"""
    with open('prefixes.json','r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json','w') as f:
        json.dump(prefixes, f, indent = 4)
    await ctx.send(f'Le préfixe est désormais {prefix}')

@client.command()
@commands.is_owner()
async def load(ctx, extension):
    """Permet de charger une extension"""
    try :
        client.load_extension(f'cogs.{extension}')
    except : 
        await ctx.send(f"L'extension {extension} n'a pas pu être chargée.", delete_after=4)
        return
    await ctx.send(f"L'extension {extension} est désormais chargée.", delete_after=4)

@client.command()
@commands.is_owner()
async def loadall(ctx):
    """Permet de charger toutes les extensions"""
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')
    await ctx.send('Toutes les extensions ont été chargées.', delete_after=4)

@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    """Permet de recharger une extension"""
    try :
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
    except :
        await ctx.send(f"L'extension {extension} n'a pas pu être rechargée.", delete_after=4)
        return
    await ctx.send(f"L'extension {extension} a été rechargée.", delete_after=4)

@client.command()
@commands.is_owner()
async def reloadall(ctx):
    """Permet de recharger toutes les extensions"""
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.unload_extension(f'cogs.{filename[:-3]}')
            client.load_extension(f'cogs.{filename[:-3]}')
    await ctx.send('Toutes les extensions ont été rechargées.', delete_after=4)

@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    """Permet de décharger une extension"""

    try :
        client.unload_extension(f'cogs.{extension}')
    except :
        await ctx.send(f"L'extension {extension} n'a pas pu être déchargée.", delete_after=4)
        return
    await ctx.send(f"L'extension {extension} est désormais déchargée.", delete_after=4)

@client.command()
@commands.is_owner()
async def unloadall(ctx):
    """Permet de décharger toutes les extensions"""
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.unload_extension(f'cogs.{filename[:-3]}')
    await ctx.send('Toutes les extensions ont été déchargées.', delete_after=4)

@client.command()
async def server_info(ctx):
    """Donne des informations sur le serveur"""
    await ctx.send(f'{ctx.guild.name} {ctx.guild.region} {ctx.guild.channels} {ctx.guild.id} {ctx.guild.owner} {ctx.guild.description}')


client.run(TOKEN)