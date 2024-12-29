import nextcord
from nextcord.ext import commands
import classes.country as clcountry

'''
Commands pertaining to countries
'''

class CountryCmds(commands.Cog):
    @commands.command(name="budget_show", help="Check your country's budget")
    async def budget(self, ctx, country: str):  
        obj = clcountry.obj_checker(country)
        if not obj:
            await ctx.send(f'{country} does not exist in our database.')
            raise NameError(f'{country} does not exist in our database.')
        await ctx.send(f'{obj.name} has {obj.funds} coins left for use.')
def setup(bot):
    bot.add_cog(CountryCmds(bot))