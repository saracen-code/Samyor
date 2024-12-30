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
        self.hover_tax_type = {}  # Dictionary to track the selected tax type per user

    @commands.command(name="t.manage", help="Manage your country's taxes")
    async def tmanage(self, ctx):
        # Check if the user is an admin
        if not ctx.author.guild_permissions.administrator:
            # Search for the country object with the queryer's discordID
            country = clcountry.get_country_by_id(ctx.author.id)
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
                return
            country = msg.content

        # Create the embed
        taxobj = tax.obj_checker(country)
        countryobj = clcountry.obj_checker(country)
        if not taxobj or not countryobj:
            await ctx.send(f"Could not find tax or country data for {country}.")
            return

        embed = self.create_embed(taxobj, countryobj, ctx.author.id)

        # Send the embed with the view
        await ctx.send(embed=embed, view=self.create_main_view(taxobj, countryobj, ctx))

    def create_embed(self, taxobj, countryobj, user_id):
        hover_tax = self.hover_tax_type.get(user_id, "land_tax")
        taxes = {
            "land_tax": "📊 **Land Tax:**",
            "poll_tax": "📊 **Poll Tax:**",
            "rents": "📊 **Rents:**",
            "customs": "📊 **Customs:**",
            "tribute": "📊 **Tribute:**",
            "ransoms": "📊 **Ransoms:**",
            "central_demesne": "📊 **Central Demesne:**",
        }

        description = "Manage taxes for your country with ease! Use the buttons below to perform actions.\n\n**Current Status:**\n"
        for key, label in taxes.items():
            value = getattr(taxobj, key)
            if key == hover_tax:
                description += f"__{label} {str(value)}__\n"
            else:
                description += f"{label} {str(value)}\n"

        description += f"📈 **Projected Revenue:** {str(countryobj.funds)}\n\n_Select an option below to manage your country's economy._"

        embed = nextcord.Embed(
            title="🏛️ Country Tax Manager",
            description=description,
            color=nextcord.Color.blue()
        )
        embed.set_thumbnail(url="https://img.freepik.com/premium-photo/medieval-florentine-banking-scene-illustration_818261-29255.jpg")  # Replace with a relevant image URL
        embed.set_footer(text="Country Tax Manager | Powered by SamyorBOT")
        return embed

    async def switch_to_tax_selector_callback(self, taxobj, countryobj, ctx, interaction):
        embed = nextcord.Embed(
            title="🔄 Select Tax Type",
            description=(
                "Choose which tax type to hover over. Use the buttons below to select a tax type:\n\n"
                "**Available Taxes:**\n"
                "1️⃣ **Land Tax**\n"
                "2️⃣ **Poll Tax**\n"
                "3️⃣ **Rents**\n"
                "4️⃣ **Customs**\n"
                "5️⃣ **Tribute**\n"
                "6️⃣ **Ransoms**\n"
                "7️⃣ **Central Demesne**\n"
            ),
            color=nextcord.Color.green()
        )

        # Buttons for selecting tax type
        view = View()
        taxes = ["land_tax", "poll_tax", "rents", "customs", "tribute", "ransoms", "central_demesne"]
        for idx, tax_type in enumerate(taxes, start=1):
            button = Button(label=f"{tax_type.replace('_', ' ').title()}", style=nextcord.ButtonStyle.secondary, emoji=f"{idx}️⃣")

            async def tax_callback(interaction, tax_type=tax_type):
                self.hover_tax_type[ctx.author.id] = tax_type
                embed = self.create_embed(taxobj, countryobj, ctx.author.id)
                await interaction.response.edit_message(embed=embed, view=self.create_main_view(taxobj, countryobj, ctx))

            button.callback = tax_callback
            view.add_item(button)

        # Add a button to return to the main page
        back_button = Button(label="Back to Main Page", style=nextcord.ButtonStyle.primary, emoji="⬅️")

        async def back_callback(interaction):
            embed = self.create_embed(taxobj, countryobj, ctx.author.id)
            await interaction.response.edit_message(embed=embed, view=self.create_main_view(taxobj, countryobj, ctx))

        back_button.callback = back_callback
        view.add_item(back_button)

        # Send the tax selector embed with buttons
        await interaction.response.edit_message(embed=embed, view=view)

    def create_main_view(self, taxobj, countryobj, ctx):
        view = View()
        increase_button = Button(label="Increase Tax", style=nextcord.ButtonStyle.primary, emoji="🔺")
        decrease_button = Button(label="Decrease Tax", style=nextcord.ButtonStyle.danger, emoji="🔻")
        collect_button = Button(label="Collect Annual Taxes", style=nextcord.ButtonStyle.success, emoji="💰")
        stats_button = Button(label="View Stats", style=nextcord.ButtonStyle.primary, emoji="📊")
        switch_button = Button(label="Switch to Tax Selector", style=nextcord.ButtonStyle.secondary, emoji="🔄")

        # Add callbacks to buttons
        increase_button.callback = self.increase_tax_callback(taxobj, countryobj, ctx)
        decrease_button.callback = self.decrease_tax_callback(taxobj, countryobj, ctx)
        collect_button.callback = self.collect_taxes_callback(taxobj, countryobj, ctx)
        stats_button.callback = self.view_stats_callback(taxobj, countryobj, ctx)
        switch_button.callback = self.assign_switch_callback(taxobj, countryobj, ctx)

        # Add buttons to the view
        view.add_item(increase_button)
        view.add_item(decrease_button)
        view.add_item(collect_button)
        view.add_item(stats_button)
        view.add_item(switch_button)
        return view

    def assign_switch_callback(self, taxobj, countryobj, ctx):
        async def callback(interaction):
            await self.switch_to_tax_selector_callback(taxobj, countryobj, ctx, interaction)
        return callback

    def increase_tax_callback(self, taxobj, countryobj, ctx):
        async def callback(interaction):
            hover_tax = self.hover_tax_type.get(ctx.author.id, "land_tax")
            taxobj.increase_tax(hover_tax, 1)
            await interaction.response.edit_message(embed=self.create_embed(taxobj, countryobj, ctx.author.id), view=self.create_main_view(taxobj, countryobj, ctx))
        return callback

    def decrease_tax_callback(self, taxobj, countryobj, ctx):
        async def callback(interaction):
            hover_tax = self.hover_tax_type.get(ctx.author.id, "land_tax")
            taxobj.decrease_tax(hover_tax, 1)
            await interaction.response.edit_message(embed=self.create_embed(taxobj, countryobj, ctx.author.id), view=self.create_main_view(taxobj, countryobj, ctx))
        return callback

    def collect_taxes_callback(self, taxobj, countryobj, ctx):
        async def callback(interaction):
            # Implement the logic for collecting taxes here
            await interaction.response.send_message("Taxes have been collected.")
        return callback

    def view_stats_callback(self, taxobj, countryobj, ctx):
        async def callback(interaction):
            await interaction.response.send_message(f"Current funds: {countryobj.funds}")
        return callback


def setup(bot):
    bot.add_cog(Taxation(bot))
