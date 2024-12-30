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
        self.hover_tax_type = {}

    @commands.command(name="t.manage", help="Manage your country's taxes")
    async def tmanage(self, ctx):
        if not ctx.author.guild_permissions.administrator:
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

        taxobj = tax.obj_checker(country)
        countryobj = clcountry.obj_checker(country)
        if not taxobj or not countryobj:
            await ctx.send(f"Could not find tax or country data for {country}.")
            return

        embed = self.create_embed(taxobj, countryobj, ctx.author.id)
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
                description += f"__{label} {value}__\n"
            else:
                description += f"{label} {value}\n"

        description += f"📈 **Projected Revenue:** {countryobj.funds}\n\n_Select an option below to manage your country's economy._"

        embed = nextcord.Embed(
            title="🏛️ Country Tax Manager",
            description=description,
            color=nextcord.Color.blue()
        )
        embed.set_thumbnail(url="https://img.freepik.com/premium-photo/medieval-florentine-banking-scene-illustration_818261-29255.jpg")
        embed.set_footer(text="Country Tax Manager | Powered by SamyorBOT")
        return embed

    def create_main_view(self, taxobj, countryobj, ctx):
        view = View()
        user_id = ctx.author.id  # Get the command initiator's ID

        increase_button = Button(label="Increase Tax", style=nextcord.ButtonStyle.primary, emoji="🔺")
        decrease_button = Button(label="Decrease Tax", style=nextcord.ButtonStyle.danger, emoji="🔻")
        collect_button = Button(label="Collect Annual Taxes", style=nextcord.ButtonStyle.success, emoji="💰")
        stats_button = Button(label="View Stats", style=nextcord.ButtonStyle.primary, emoji="📊")
        switch_button = Button(label="Switch to Tax Selector", style=nextcord.ButtonStyle.secondary, emoji="🔄")

        increase_button.callback = self.make_secure_callback(user_id, self.increase_tax_callback(taxobj, countryobj, ctx))
        decrease_button.callback = self.make_secure_callback(user_id, self.decrease_tax_callback(taxobj, countryobj, ctx))
        collect_button.callback = self.make_secure_callback(user_id, self.collect_taxes_callback(taxobj, countryobj, ctx))
        stats_button.callback = self.make_secure_callback(user_id, self.view_stats_callback(taxobj, countryobj, ctx))
        switch_button.callback = self.make_secure_callback(user_id, self.assign_switch_callback(taxobj, countryobj, ctx))

        view.add_item(increase_button)
        view.add_item(decrease_button)
        view.add_item(collect_button)
        view.add_item(stats_button)
        view.add_item(switch_button)
        return view

    def make_secure_callback(self, user_id, original_callback):
        async def callback(interaction):
            if interaction.user.id != user_id:
                await interaction.response.send_message("You are not allowed to interact with this menu.", ephemeral=True)
                return
            await original_callback(interaction)
        return callback

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
            await interaction.response.send_message("Taxes have been collected.")
        return callback

    def view_stats_callback(self, taxobj, countryobj, ctx):
        async def callback(interaction):
            await interaction.response.send_message(f"Current funds: {countryobj.funds}")
        return callback

def setup(bot):
    bot.add_cog(Taxation(bot))
