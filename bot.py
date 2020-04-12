
import discord, logging, json, os
from discord.ext import commands

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

try : 
    TOKEN = os.environ['DISCORD_TOKEN']
except : 
    from dotenv import load_dotenv
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")

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

@client.command(aliases=['prefix'])
@commands.has_permissions(manage_guild=True) 
async def changeprefix(ctx, prefix):
    """Permet de changer le préfixe"""
    with open('prefixes.json','r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json','w') as f:
        json.dump(prefixes, f, indent = 4)
    await ctx.message.delete()
    try :
        embed=discord.Embed(title='Préfix changé', color=0x00ff40)
        embed.add_field(name=f"--------------------------------------", value=f"Le préfixe est désormais : {prefix}", inline=True)
        await ctx.send(embed=embed)
    except :
        await ctx.send(f'Le préfixe est désormais {prefix}')

@client.command()
@commands.is_owner()
async def load(ctx, extension):
    """Permet de charger une extension"""
    await ctx.message.delete()
    try :
        client.load_extension(f'cogs.{extension}')
    except : 
        try :
            embed=discord.Embed(title='Extension non chargée', color=0xff0000)
            embed.add_field(name=f"L'extension sivante n'a pas pu être chargée.", value=f"{extension}", inline=True)
            await ctx.send(embed=embed)
        except :
            await ctx.send(f"L'extension {extension} n'a pas pu être chargée.")
        return
    try :
        embed=discord.Embed(title='Extension chargée', color=0x00ff40)
        embed.add_field(name=f"L'extension sivante est désormais chargée.", value=f"{extension}", inline=True)
        await ctx.send(embed=embed)
    except :
        await ctx.send(f"L'extension {extension} est désormais chargée.")

@client.command()
@commands.is_owner()
async def loadall(ctx):
    """Permet de charger toutes les extensions"""
    await ctx.message.delete()
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')
    try : 
        embed=discord.Embed(title='Extensions chargées', color=0x00ff40)
        embed.add_field(name=f"----------------------------------------------", value='Toutes les extensions ont été chargées.', inline=True)
        await ctx.send(embed=embed)
    except :
        await ctx.send('Toutes les extensions ont été chargées.')

@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    """Permet de recharger une extension"""
    await ctx.message.delete()
    try :
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
    except :
        try :
            embed=discord.Embed(title='Extension non rechargée', color=0xff0000)
            embed.add_field(name=f"L'extension sivante n'a pas pu être rechargée.", value=f"{extension}", inline=True)
            await ctx.send(embed=embed)
        except :
            await ctx.send(f"L'extension {extension} n'a pas pu être rechargée.")
        return
    try :
        embed=discord.Embed(title='Extension rechargée', color=0x00ff40)
        embed.add_field(name=f"L'extension suivante a été rechargée.", value=f"{extension}", inline=True)
        await ctx.send(embed=embed)
    except :
        await ctx.send(f"L'extension {extension} a été rechargée.")

@client.command()
@commands.is_owner()
async def reloadall(ctx):
    """Permet de recharger toutes les extensions"""
    await ctx.message.delete()
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.unload_extension(f'cogs.{filename[:-3]}')
            client.load_extension(f'cogs.{filename[:-3]}')
    try :
        embed=discord.Embed(title='Extensions rechargées', color=0x00ff40)
        embed.add_field(name=f"------------------------------------------------", value=f"Toutes les extensions ont été rechargées.", inline=True)
        await ctx.send(embed=embed)
    except :
        await ctx.send('Toutes les extensions ont été rechargées.')

@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    """Permet de décharger une extension"""
    await ctx.message.delete()
    try :
        client.unload_extension(f'cogs.{extension}')
    except :
        try :
            embed=discord.Embed(title='Extension non déchargée', color=0xff0000)
            embed.add_field(name=f"L'extension sivante n'a pas pu être déchargée.", value=f"{extension}", inline=True)
            await ctx.send(embed=embed)
        except :
            await ctx.send(f"L'extension {extension} n'a pas pu être déchargée.")
        return
    try :
        embed=discord.Embed(title='Extension déchargée', color=0x00ff40)
        embed.add_field(name=f"L'extension suivante a été déchargée.", value=f"{extension}", inline=True)
        await ctx.send(embed=embed)
    except :
        await ctx.send(f"L'extension {extension} a été déchargée.")

@client.command()
@commands.is_owner()
async def unloadall(ctx):
    """Permet de décharger toutes les extensions"""
    await ctx.message.delete()
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.unload_extension(f'cogs.{filename[:-3]}')
    try :
        embed=discord.Embed(title='Extensions déchargées', color=0x00ff40)
        embed.add_field(name=f"-------------------------------------------------", value=f"Toutes les extensions ont été déchargées.", inline=True)
        await ctx.send(embed=embed)
    except :
        await ctx.send('Toutes les extensions ont été déchargées.')

@client.command()
async def server_info(ctx):
    """Donne des informations sur le serveur"""
    emoji = []
    for i in ctx.guild.emojis:
        emoji.append(str(i))
    emojilist = ''.join(emoji)

    embed=discord.Embed(title=" ", color=0x00ffff, timestamp=ctx.message.created_at)
    embed.set_author(name=ctx.guild.name)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.add_field(name="Propriétaire          \u200b", value=ctx.guild.owner, inline=True)
    embed.add_field(name="ID          \u200b", value=ctx.guild.id, inline=True)
    embed.add_field(name="**ˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍˍ**", value="**¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯**", inline=False)
    embed.add_field(name="Membres          \u200b", value=ctx.guild.member_count, inline=True)
    embed.add_field(name="Roles          \u200b", value=len(ctx.guild.roles), inline=True)
    embed.add_field(name="Emojis          \u200b", value=len(ctx.guild.emojis), inline=True)
    embed.add_field(name="Salons textuels          \u200b", value=len(ctx.guild.text_channels), inline=True)
    embed.add_field(name="Salons vocaux          \u200b", value=len(ctx.guild.voice_channels), inline=True)
    embed.add_field(name="Région          \u200b", value=ctx.guild.region, inline=True)
    embed.add_field(name="Niveau de nitro          \u200b", value=ctx.guild.premium_tier, inline=True)
    embed.add_field(name="Nistro Boosters          \u200b", value=ctx.guild.premium_subscription_count, inline=True)
    embed.add_field(name="Création", value=str(ctx.guild.created_at)[:-7], inline=False)
    embed.add_field(name="Liste des Emojis", value=emojilist, inline=False)
    embed.set_footer(text=client.user, icon_url=client.user.avatar_url)
    await ctx.send(embed=embed)


client.run(TOKEN)