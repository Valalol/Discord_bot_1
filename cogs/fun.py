import discord, random, urllib.parse
from discord.ext import commands

'''Module for fun/meme commands'''

class Commandes_Funs(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases=['googleisfriend', 'lmgtfy'])
    async def ask2google(self, ctx, *, question: str):
        """Crée un lien lmgtfy"""
        lmgtfy = 'http://lmgtfy.com/?q='
        await ctx.send(lmgtfy + urllib.parse.quote_plus(question.lower().strip()))
        await ctx.message.delete()
    
    @commands.command(aliases=['dice'])
    async def roll(self, ctx, number_of_dice: int, number_of_sides: int):
        """Lance des dés"""
        if number_of_dice <= 100 : 
            dice = [
                str(random.choice(range(1, number_of_sides + 1)))
                for _ in range(number_of_dice)
            ]
            await ctx.send(', '.join(dice))
        else :
            await ctx.send('Houla, calmes-toi Didier !')
    
    @commands.command(aliases=['tg'])
    async def chut(self, ctx):
        """Chhhhhhhh"""
        await ctx.send('https://bit.ly/34wtm00')
    
    
    
def setup(client):
    client.add_cog(Commandes_Funs(client))