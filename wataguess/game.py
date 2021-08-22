import asyncio
import discord
from discord.ext import commands
from wataguess import utils


class game(commands.Cog):
    def __init__(self, db, logger):
        """
        Interests                                                                                                                                                                                                                                  List of commands that zz-8 has in order to give users
        a personalized experience from reddit
        """
        self.db = db
        self.logger = logger

    @commands.command()
    async def wataguess(self, ctx, url):
        await ctx.send("Got it! Give me one moment...")
        clean_url = utils.clean_url(url)
        item, price, item_id = utils.get_data(clean_url)
        self.db.update_item(item, price, item_id)
        await ctx.send("Come one! Come all!")
        await asyncio.sleep(1)
        await ctx.send("It's time for the next round of wataguess!")
        await asyncio.sleep(3)
        await ctx.send(f"The new item is {item}")
        await asyncio.sleep(3)
        await ctx.send("Good luck and have fun!")

    @commands.command()
    async def myguess(self, ctx, amt):
        user = ctx.message.author
        item_price = self.db.retrieve_recent_item()["price"]
        if int(float(item_price)) == int(float(amt)):
            await ctx.send("WATAGUESS!")
            await ctx.send(f"CONGRATULATIONS {user}! You win this round of Wataguess!")
        else:
            await ctx.send("Unforuntately, that is not correct.")
            await ctx.send("Better luck next round!")
            score = abs(int(float(item_price)) - int(float(amt)))
            self.db.update_score(user.id, score)
            await ctx.send(f"I have increased your score by {score}")

    @commands.command()
    async def myscore(self, ctx):
        user = ctx.message.author
        uuid = ctx.message.author.id

        score = self.db.retrieve_score(uuid)

        await ctx.send(f"{user}, your current score is {score}")

    @commands.command()
    async def rules(self, ctx):
        rules = "One person posts an ebay listing for a graded game\n Each person gets one chance to guess the price of the game per round.\nIf someone manages to guess the exact price (to the dollar) then that person gets a WATAGUESS!\nScores are bsaed on how far away from the value a guess is, the lower the score the better."
        note = "This game is played on the Honor System, the developer of this bot would greatly prefer it not have to be changed from that."
        embed = discord.Embed(
            title="WataGuess Rules",
            description="Official Rules for the Collector's Quest Discord WataGuess Game",
            color=ctx.message.author.color,
        )
        embed.add_field(name="Rules", value=rules)
        embed.add_field(name="Note", value=note)
        await ctx.send(embed=embed)
