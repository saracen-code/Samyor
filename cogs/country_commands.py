import nextcord
from nextcord.ext import commands
import classes.country as clcountry
import classes.tax_settings as tax

'''
Commands pertaining to countries
'''

class CountryCmds(commands.Cog):
    @commands.command(name="budget", help="Check your country's budget")
    async def budget(self, ctx, country: str):  
        obj = clcountry.obj_checker(country)
        if not obj:
            await ctx.send(f'{country} does not exist in our database.')
            raise NameError(f'{country} does not exist in our database.')
        await ctx.send(f'{obj.name} has {obj.funds} coins left for use.')
    @commands.command(name="census", help="Conduct a census in your country")
    async def census(self, ctx, country: str):
        obj = clcountry.obj_checker(country)
        if not obj:
            await ctx.send(f'{country} does not exist in our database.')
            raise NameError(f'{country} does not exist in our database.')
        await ctx.send(embed=country.embedded())
    @commands.command(name="tax", help="View the country tax manager")
    async def tax(self, ctx):
        pass
    @commands.command(name="column", help="Check the country column")
    async def column(self, ctx, country: str):
        obj = clcountry.obj_checker(country)
        if not obj:
            await ctx.send(f'{country} does not exist in our database.')
            raise NameError(f'{country} does not exist in our database.')
        await ctx.send(f'{obj.name} is in column {obj.column}.')
    @commands.command(name="country_owner", help="Check the owner of a country")
    async def country_owner(self, ctx, country: str):
        obj = clcountry.obj_checker(country)
        if not obj:
            await ctx.send(f'{country} does not exist in our database.')
            raise NameError(f'{country} does not exist in our database.')
        await ctx.send(f'{obj.name} is owned by <@{obj.userid}>.')
    @commands.command(name="showtax", help="Show the tax manager")
    async def initializetax(self, ctx):
        tax.initialize()

def setup(bot):
    bot.add_cog(CountryCmds(bot))