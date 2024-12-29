import nextcord
from nextcord.ext import commands
from nextcord.ui import Button, View
import classes.country as clcountry
from classes.country import Country
import asyncio
import classes.tax_settings as tax
from classes.tax_settings import Tax

class Taxation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="t.manage", help="Manage your country's taxes")
    async def tmanage(self, ctx):
        # Check if the user is an admin
        if not ctx.author.guild_permissions.administrator:
            # Search for the country object with the queryer's discordID
            country = clcountry.get_country_by_id(ctx.author.id)
            print(ctx.author.id)
            if not country:
                await ctx.send("You do not have a country assigned to you.")
                return
            country = country.name
        else:
            await ctx.send("You are an admin. Please provide the name of the country you want to manage:")
            
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            msg = await self.bot.wait_for('message', check=check, timeout=60)
            country = clcountry.obj_checker(msg.content)
            if not country:
                await ctx.send(f'{country} does not exist in our database.')
                raise NameError(f'{country} does not exist in our database.')
            country = msg.content

        # Create the embed
        taxobj = tax.obj_checker(country)
        countryobj = clcountry.obj_checker(country)
        if not taxobj or not countryobj:
            await ctx.send(f"Could not find tax or country data for {country}.")
            return
        print(f"Successfully found {countryobj} and {taxobj}")
        embed = self.create_embed(taxobj, countryobj)

        # Create buttons
        increase_button = Button(label="Increase Land Tax", style=nextcord.ButtonStyle.primary, emoji="🔺")
        decrease_button = Button(label="Decrease Land Tax", style=nextcord.ButtonStyle.danger, emoji="🔻")
        collect_button = Button(label="Collect Annual Taxes", style=nextcord.ButtonStyle.success, emoji="💰")
        stats_button = Button(label="View Stats", style=nextcord.ButtonStyle.primary, emoji="📊")

        # Add callbacks to buttons
        increase_button.callback = self.increase_tax_callback(taxobj, countryobj, ctx)
        decrease_button.callback = self.decrease_tax_callback(taxobj, countryobj, ctx)
        collect_button.callback = self.collect_taxes_callback(taxobj, countryobj, ctx)
        stats_button.callback = self.view_stats_callback(taxobj, countryobj, ctx)

        # Create a view and add buttons to it
        view = View()
        view.add_item(increase_button)
        view.add_item(decrease_button)
        view.add_item(collect_button)
        view.add_item(stats_button)

        # Send the embed with the view
        await ctx.send(embed=embed, view=view)

    def create_embed(self, taxobj, countryobj):
        embed = nextcord.Embed(
            title="🏛️ Country Tax Manager",
            description=(
                "Manage taxes for your country with ease! Use the buttons below to perform actions.\n\n"
                "**Current Status:**\n"
                f"📊 **Land Tax:** {str(taxobj.land_tax)}\n"
                f"📊 **Poll Tax:** {str(taxobj.poll_tax)}\n"
                f"📊 **Rents:** {str(taxobj.rents)}\n"
                f"📊 **Customs:** {str(taxobj.customs)}\n"
                f"📊 **Tribute:** {str(taxobj.tribute)}\n"
                f"📊 **Ransoms:** {str(taxobj.ransoms)}\n"
                f"📊 **Central Demesne:** {str(taxobj.central_demesne)}\n"
                f"📈 **Projected Revenue:** {str(countryobj.funds)}\n\n"
                "_Select an option below to manage your country's economy._"
            ),
            color=nextcord.Color.blue()
        )
        embed.set_thumbnail(url="https://img.freepik.com/premium-photo/medieval-florentine-banking-scene-illustration_818261-29255.jpg")  # Replace with a relevant image URL
        embed.set_footer(text="Country Tax Manager | Powered by SamyorBOT")
        return embed

    def increase_tax_callback(self, taxobj, countryobj, ctx):
        async def callback(interaction):
            taxobj.increase_tax("land_tax", 1)
            await interaction.response.edit_message(embed=self.create_embed(taxobj, countryobj))
        return callback

    def decrease_tax_callback(self, taxobj, countryobj, ctx):
        async def callback(interaction):
            taxobj.decrease_tax("land_tax", 1)
            await interaction.response.edit_message(embed=self.create_embed(taxobj, countryobj))
        return callback

    def view_stats_callback(self, taxobj, countryobj, ctx):
        async def callback(interaction):
            await interaction.response.send_message(f"Current funds: {countryobj.funds}")
        return callback

def setup(bot):
    bot.add_cog(Taxation(bot))