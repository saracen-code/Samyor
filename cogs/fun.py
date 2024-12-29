import nextcord
from nextcord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='roll', help='Rolls a dice.')
    async def roll(self, ctx, sides: int = 6):
        result = random.randint(1, sides)
        await ctx.send(f'🎲 You rolled a {result}!')

    @commands.command(name='flip', help='Flips a coin.')
    async def flip(self, ctx):
        result = random.choice(['Heads', 'Tails'])
        await ctx.send(f'🪙 {result}')
    @commands.command(name='rps', help='Play rock, paper, scissors')
    async def rps(self, ctx, choice: str):
        choices = ['rock', 'paper', 'scissors']
        if choice.lower() not in choices:
            await ctx.send('Please choose rock, paper, or scissors!')
            return
        bot_choice = random.choice(choices)
        if choice.lower() == bot_choice:
            result = "It's a tie!"
        elif (choice.lower() == 'rock' and bot_choice == 'scissors') or (choice.lower() == 'paper' and bot_choice == 'rock') or (choice.lower() == 'scissors' and bot_choice == 'paper'):
            result = 'You win!'
        else:
            result = 'I win!'
        await ctx.send(f'You chose {choice}, I chose {bot_choice}. {result}')

    @commands.command(name='choose', help='Let the bot choose between options')
    async def choose(self, ctx, *options):
        if len(options) < 2:
            await ctx.send('Please provide at least 2 options to choose from!')
            return
        await ctx.send(f'I choose: {random.choice(options)}')
def setup(bot):
    bot.add_cog(Fun(bot))