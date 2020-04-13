import discord, json
from discord.ext import commands

'''Module pour commandes admin'''

def extension_activated(ctx):
    with open('settings.json','r') as f:
        settings = json.load(f)
    return settings[str(ctx.guild.id)]["admin"] == "True"


class Commandes_Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        return extension_activated(ctx)

    @commands.command(aliases=['clean','removemsg'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount : int, author : discord.Member = None):
        """Supprime un certain nombre de messages"""
        await ctx.message.delete()
        if author == None:
            await ctx.channel.purge(limit=amount)
            await ctx.send(f'I have deleted {amount} messages. :unicorn:', delete_after=4)
        else:
            def author_check(m):
                return m.author == author
            await ctx.channel.purge(limit=amount+1, check = author_check)
            await ctx.send(f'I have deleted {amount} messages of {author}. :unicorn:', delete_after=4)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance (error, commands.MissingRequiredArgument):
            await ctx.send(f"Veuillez spécifier le nombre de message à supprimer.\nPour l'utilisation correcte de cette commande, tapez {ctx.prefix}help clear.")
    
    @commands.command()
    @commands.has_permissions(kick_members=True) 
    async def kick(self, ctx, user : discord.Member, *, reason=None):
        """Expulse un membre du serveur"""
        await user.kick(reason=reason)
        try :
            embed=discord.Embed(title=f'{user} a été expulsé du serveur', color=0xff0000)
            embed.add_field(name=f"Modérateur", value=ctx.message.author)
            embed.add_field(name=f"Raison", value=reason)
            await ctx.send(embed=embed)
        except :
            await ctx.send(f'{user} a été expulsé du serveur par {ctx.message.author}.\nLa raison de cette explusion est la suivante : {reason}')
    
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance (error, commands.MissingRequiredArgument):
            try :
                embed=discord.Embed(title='Utilisateur non spécifié', color=0xC0C0C0)
                embed.add_field(name=f"Pour l'utilisation correcte de cette commande,", value=f"Tapez {ctx.prefix}help kick.", inline=True)
                await ctx.send(embed=embed)
            except :
                await ctx.send(f"Veuillez spécifier l'utilisateur à expulser.\nPour l'utilisation correcte de cette commande, tapez {ctx.prefix}help kick.")
        else:
            print(error)

    @commands.command()
    @commands.has_permissions(ban_members=True) 
    async def ban(self, ctx, user : discord.Member, *, reason=None):
        """Bannit un membre du serveur"""
        await user.ban(reason=reason)
        try :
            embed=discord.Embed(title=f'{user} a été banni du serveur', color=0xff0000)
            embed.add_field(name=f"Modérateur", value=ctx.message.author)
            embed.add_field(name=f"Raison", value=reason)
            await ctx.send(embed=embed)
        except :
            await ctx.send(f'{user} a été banni du serveur par {ctx.message.author}.\nLa raison de ce bannissement est la suivante : {reason}')
    
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance (error, commands.MissingRequiredArgument):
            try :
                embed=discord.Embed(title='Utilisateur non spécifié', color=0xC0C0C0)
                embed.add_field(name=f"Pour l'utilisation correcte de cette commande,", value=f"Tapez {ctx.prefix}help ban.", inline=True)
                await ctx.send(embed=embed)
            except :
                await ctx.send(f"Veuillez spécifier l'utilisateur à bannir.\nPour l'utilisation correcte de cette commande, tapez {ctx.prefix}help ban.")
        else:
            print(error)
    
    @commands.command()
    @commands.has_permissions(ban_members=True) 
    async def unban(self, ctx, *, user):
        """Débannit un membre du serveur"""
        banned_users = await ctx.guild.bans()
        user_name, user_discriminator = user.split('#')
        for ban_entry in banned_users:
            if (user_name, user_discriminator) == (ban_entry.user.name, ban_entry.user.discriminator):
                await ctx.guild.unban(ban_entry.user)
        try :
            embed=discord.Embed(title=f'{user} a été débanni du serveur', color=0x00ff00)
            embed.add_field(name=f"Modérateur", value=ctx.message.author)
            await ctx.send(embed=embed)
        except :
            await ctx.send(f'{user} a été débanni du serveur par {ctx.message.author}.')
    
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance (error, commands.MissingRequiredArgument):
            try :
                embed=discord.Embed(title='Utilisateur non spécifié', color=0xC0C0C0)
                embed.add_field(name=f"Pour l'utilisation correcte de cette commande,", value=f"Tapez {ctx.prefix}help unban.", inline=True)
                await ctx.send(embed=embed)
            except :
                await ctx.send(f"Veuillez spécifier l'utilisateur à débannir.\nPour l'utilisation correcte de cette commande, tapez {ctx.prefix}help unban.")
        else:
            print(error)

    @commands.command()
    @commands.has_permissions(manage_messages=True) 
    async def mute(self, ctx, user : discord.Member, *, reason=None):
        """Mute un membre du serveur"""
        for role in ctx.guild.roles: 
            if role.name == "Muted":
                await user.add_roles(role)
                try :
                    embed=discord.Embed(title=f'{user} a été mute du serveur', color=0xFFBD00)
                    embed.add_field(name=f"Modérateur", value=ctx.message.author)
                    embed.add_field(name=f"Raison", value=reason)
                    await ctx.send(embed=embed)
                except :
                    await ctx.send(f'{user} a été mute du serveur par {ctx.message.author}.\nLa raison de ce mute est la suivante : {reason}')
                return
        
        overwrite = discord.PermissionOverwrite(send_messages=False, add_reactions=False)
        newRole = await ctx.guild.create_role(name="Muted")

        for channel in ctx.guild.text_channels:
            await channel.set_permissions(newRole, overwrite=overwrite)
        await user.add_roles(newRole)
        try :
            embed=discord.Embed(title=f'{user} a été mute du serveur', color=0xFFBD00)
            embed.add_field(name=f"Modérateur", value=ctx.message.author)
            embed.add_field(name=f"Raison", value=reason)
            await ctx.send(embed=embed)
        except :
            await ctx.send(f'{user} a été mute du serveur par {ctx.message.author}.\nLa raison de ce mute est la suivante : {reason}')

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance (error, commands.MissingRequiredArgument):
            try :
                embed=discord.Embed(title='Utilisateur non spécifié', color=0xC0C0C0)
                embed.add_field(name=f"Pour l'utilisation correcte de cette commande,", value=f"Tapez {ctx.prefix}help mute.", inline=True)
                await ctx.send(embed=embed)
            except :
                await ctx.send(f"Veuillez spécifier l'utilisateur à muter.\nPour l'utilisation correcte de cette commande, tapez {ctx.prefix}help mute.")
        else:
            print(error)


    @commands.command()
    @commands.has_permissions(manage_messages=True) 
    async def unmute(self, ctx, user : discord.Member):
        """Unmute un membre du serveur"""
        for role in ctx.guild.roles: 
            if role.name == "Muted":
                await user.remove_roles(role)
                try :
                    embed=discord.Embed(title=f'{user} a été unmute du serveur', color=0x00ff00)
                    embed.add_field(name=f"Modérateur", value=ctx.message.author)
                    await ctx.send(embed=embed)
                except :
                    await ctx.send(f'{user} a été unmute du serveur par {ctx.message.author}.')
                return

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance (error, commands.MissingRequiredArgument):
            try :
                embed=discord.Embed(title='Utilisateur non spécifié', color=0xC0C0C0)
                embed.add_field(name=f"Pour l'utilisation correcte de cette commande,", value=f"Tapez {ctx.prefix}help unmute.", inline=True)
                await ctx.send(embed=embed)
            except :
                await ctx.send(f"Veuillez spécifier l'utilisateur à unmuter.\nPour l'utilisation correcte de cette commande, tapez {ctx.prefix}help unmute.")
        else:
            print(error)

    @commands.Cog.listener()
    async def on_message(self, message):
        if extension_activated(message.channel):
            with open('settings.json','r') as f:
                settings = json.load(f)
            banwords = settings[str(message.guild.id)]["banwords"]
            for word in banwords:
                if message.content.count(word) > 0:
                    await message.delete()
                    await message.channel.send('Nope')
        
    @commands.command()
    @commands.has_permissions(manage_messages=True) 
    async def banword(self, ctx, word):
        """Bloque une série de caractères"""
        await ctx.message.delete()
        with open('settings.json','r') as f:
            settings = json.load(f)

        settings[str(ctx.guild.id)]['banwords'].append(str(word))

        with open('settings.json','w') as f:
            json.dump(settings, f, indent = 4)

        try :
            embed=discord.Embed(title=f'{word} a été ajouté aux mots bloqués', color=0x00ff00)
            embed.add_field(name=f"Modérateur", value=ctx.message.author)
            await ctx.send(embed=embed)
        except :
            await ctx.send(f'{word} a été ajouté aux mots bloqués par {ctx.message.author}.')
    
    @commands.command()
    @commands.has_permissions(manage_messages=True) 
    async def unbanword(self, ctx, word):
        """Débloque une série de caractères"""
        with open('settings.json','r') as f:
            settings = json.load(f)

        settings[str(ctx.guild.id)]['banwords'].remove(str(word))

        with open('settings.json','w') as f:
            json.dump(settings, f, indent = 4)

        try :
            embed=discord.Embed(title=f'{word} a été retiré des mots bloqués', color=0x00ff00)
            embed.add_field(name=f"Modérateur", value=ctx.message.author)
            await ctx.send(embed=embed)
        except :
            await ctx.send(f'{word} a été retiré des mots bloqués par {ctx.message.author}.')
        await ctx.message.delete()

def setup(client):
    client.add_cog(Commandes_Admin(client))