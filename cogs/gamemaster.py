import nextcord
from nextcord.ext import commands
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils.operations_executer as oe
import utils.operations_writer as ow
import utils.sheetoperations as so
import classes.country as clcountry
from classes.country import Country

'''
Commands pertaining to countries
'''

'''
1. Must check that every country has their revenues calculated
2. Must check that every country has their population calculated
^ We know the above two happened by checking the country's "current year" which is row 13 on the spreadsheet
3. If not, ping the player and ask them to do so and not complete this command
4. If yes, then go on with the command and move on to next year
'''

class GameMasterCmds(commands.Cog):
    def __init__(self, bot):  # Add the bot parameter to initialize the bot
        self.bot = bot  # Assign bot to self.bot

    @commands.command(name="next_year", help="Move to next year, permitting players to calculate their revenues and more.")
    async def create(self, ctx):  
        print("hey")

    @commands.command(name="c.create", help="Create a country")
    async def country_create(self, ctx, country: str):
        obj = clcountry.obj_checker(country)
        if obj:
            await ctx.send(f'{country} already exists in our database.')
            raise NameError(f'{country} already exists in our database.')
        new_country = Country(country, ctx.author.id)
        col = clcountry.latest_unused_column()
        print(col)
        id = ow.append_country_col(col, new_country.list_archive(), "Countries")
        oe.execute_single_operation(id)
        await ctx.send(f'{country} has been created.')
    @commands.command(name="c.change", help="Change a country's value")
    async def country_change(self, ctx, country: str, key: str, value):
        obj = clcountry.obj_checker(country)
        if not obj:
            await ctx.send(f'{country} does not exist in our database.')
            raise NameError(f'{country} does not exist in our database.')
        # Update the object values
        obj.update_values(key, value)
        row = clcountry.get_attr_row(key)
        location = so.convert_to_A1(row, obj.column)
        # request updating spreadsheet values
        id = ow.update_cell(location, value, "Countries")
        # executing operation
        oe.execute_single_operation(id)
        await ctx.send(f'{key} has been updated to {value} for {country}.')
    @commands.command(name="c.events", help="View the admin panel for events")
    async def country_events(self, ctx):
        pass
    @commands.command(name="c.assign", help="Assign a player to a country")
    async def country_assign(self, ctx, country: str, player: str):
        obj = clcountry.obj_checker(country)
        if not obj:
            await ctx.send(f'{country} does not exist in our database.')
            raise NameError(f'{country} does not exist in our database.')
        try:
            player_id = int(player.strip('<@!>'))
            user = await self.bot.fetch_user(player_id)
            obj.assign(player)
            await ctx.send(f'{player} has been assigned to {country}.')
            await ctx.send(f'Sent request to update the spreadsheet at column {obj.column}.')
            await ctx.send('Please wait a minute before using the country commands.')
            location = so.convert_to_A1(clcountry.get_attr_row("userid"), obj.column)
            ow.update_cell(location, player_id, "Countries")
        except (ValueError, nextcord.NotFound):
            await ctx.send(f'{player} is not a valid Discord user.')
            return
def setup(bot):
    bot.add_cog(GameMasterCmds(bot))