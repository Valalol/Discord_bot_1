import discord, random, urllib.parse, praw, os, json
from discord.ext import commands

'''Module pour meme/commandes fun'''

try : 
    REDDIT_CLIENT_ID = os.environ['REDDIT_CLIENT_ID']
except : 
    from dotenv import load_dotenv
    load_dotenv()
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")

try : 
    REDDIT_CLIENT_SECRET = os.environ['REDDIT_CLIENT_SECRET']
except : 
    from dotenv import load_dotenv
    load_dotenv()
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")

try : 
    REDDIT_USER_AGENT = os.environ['REDDIT_USER_AGENT']
except : 
    from dotenv import load_dotenv
    load_dotenv()
    REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                     client_secret=REDDIT_CLIENT_SECRET,
                     user_agent=REDDIT_USER_AGENT)


def extension_activated(ctx):
    with open('settings.json','r') as f:
        settings = json.load(f)
    return settings[str(ctx.guild.id)]["fun"] == "True"

class Commandes_Funs(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases=['googleisfriend', 'lmgtfy'])
    @commands.check(extension_activated)
    async def ask2google(self, ctx, *, question: str):
        """Crée un lien lmgtfy"""
        lmgtfy = 'http://lmgtfy.com/?q='
        await ctx.send(lmgtfy + urllib.parse.quote_plus(question.lower().strip()))
        await ctx.message.delete()
    
    @commands.command(aliases=['dice'])
    @commands.check(extension_activated)
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
    @commands.check(extension_activated)
    async def chut(self, ctx):
        """Chhhhhhhh"""
        await ctx.send('https://bit.ly/34wtm00')

    @commands.command()
    @commands.check(extension_activated)
    async def reddit(self, ctx, subreddit):
        """Publie une image aléatoire du subreddit spécifié"""
        memes_submissions = reddit.subreddit(subreddit).hot()
        post_to_pick = random.randint(1, 50)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)
        if submission.over_18:
            if ctx.channel.is_nsfw():
                await ctx.send(submission.url)
            else : 
                try :
                    embed=discord.Embed(title='Publication refusée', color=0xff0000)
                    embed.add_field(name=f"--------------------------------------", value=f"Cette publication ne peut apparaitre que dans un salon NSFW", inline=True)
                    await ctx.send(embed=embed)
                except :
                    await ctx.send(f"Cette publication ne peut apparaitre que dans un salon NSFW")
        else : 
            await ctx.send(submission.url)

    @commands.command()
    @commands.check(extension_activated)
    async def meme(self, ctx):
        """Publie un meme aléatoire"""
        memes_submissions = reddit.subreddit('memes').hot()
        post_to_pick = random.randint(1, 50)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)

        await ctx.send(submission.url)
    
    
    
def setup(client):
    client.add_cog(Commandes_Funs(client))