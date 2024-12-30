import nextcord
from nextcord.ext import commands
from nextcord.ui import Button, View
from nextcord import embeds
import classes.country as clcountry
from classes.country import Country
import asyncio
import classes.tax_settings as tax
from classes.tax_settings import Tax

class TaxationV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hover_tax_type = {}  # Dictionary to track the selected tax type per user
        self.tax_data = {
            "land_tax": 10,
            "poll_tax": 5,
            "rent_tax": 7,
            "customs": 8,
            "tribute": 6,
            "ransoms": 3,
            "central_demesne": 12,
            "extra_taxes": 4,
            "annual_taxes": 15
        }

    @commands.command(name="t.manage", help="Rank: Leader | Descr.: Control panel to manage taxes for your country.")
    async def tmanage(self, ctx):
        country = None
        
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
            
            try:
                msg = await self.bot.wait_for('message', check=check, timeout=60)
                country = clcountry.obj_checker(msg.content)
                if not country:
                    await ctx.send(f"{msg.content} does not exist in our database.")
                    return
                country = msg.content
            except nextcord.errors.TimeoutError:
                await ctx.send("Command timed out. Please try again.")
                return

        # Start with the home page
        embed = self.create_embed(page=1, country=country)
        view = self.create_view(ctx, country)
        await ctx.send(embed=embed, view=view)

    def create_embed(self, page: int, country: str):
        """Creates an embed for the given page."""
        embed = nextcord.Embed(title=f"Taxation Management - {country}", color=nextcord.Color.blue())
        if page == 1:
            embed.description = (
                "**Home Page**\n\n"
                "Welcome to the Tax Management System. Use the buttons below to navigate to specific tax types.\n\n"
                "__Table of Contents__:\n"
                "2. Land Tax\n"
                "3. Poll Tax\n"
                "4. Rent Tax\n"
                "5. Customs\n"
                "6. Tribute\n"
                "7. Ransoms\n"
                "8. Central Demesne\n"
                "9. Extra Taxes\n"
                "10. Collect Annual Taxes"
            )
        elif 2 <= page <= 9:
            tax_type = list(self.tax_data.keys())[page - 2]
            tax_value = self.tax_data[tax_type]
            embed.description = (
                f"**{tax_type.replace('_', ' ').title()}**\n\n"
                f"Current Tax Percentage: {tax_value}%\n\n"
                "Use the buttons below to adjust the tax percentage."
            )
        elif page == 10:
            embed.description = (
                "**Collect Annual Taxes**\n\n"
                "Here you can finalize and collect the annual taxes for your country."
            )
        return embed

    def create_view(self, ctx, country):
        """Creates a view with navigation buttons and tax adjustment buttons."""
        view = View()
        for i in range(1, 11):
            view.add_item(Button(label=f"Page {i}", style=nextcord.ButtonStyle.primary, custom_id=f"page_{i}"))

        def button_callback(interaction: nextcord.Interaction):
            if interaction.user != ctx.author:
                return
            page = int(interaction.data["custom_id"].split("_")[1])
        async def button_callback(interaction: nextcord.Interaction):
            new_view = self.create_view(ctx, country)
            if 2 <= page <= 9:
                new_view.add_item(Button(label="Increase", style=nextcord.ButtonStyle.success, custom_id="increase"))
                new_view.add_item(Button(label="Decrease", style=nextcord.ButtonStyle.danger, custom_id="decrease"))
            await interaction.response.edit_message(embed=embed, view=new_view)

        for button in view.children:
            button.callback = button_callback

        return view
def setup(bot):
    bot.add_cog(TaxationV2(bot))