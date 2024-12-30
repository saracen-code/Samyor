import nextcord
from nextcord.ext import commands
from nextcord.ui import Button, View
import classes.country as clcountry
from classes.country import Country
import classes.tax_settings as tax
from classes.tax_settings import Tax
import random
import text.tax_description as descriptions

class TaxationV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hover_tax_type = {}  # Tracks the selected tax type per user
        self.tax_data = {}        # Stores tax data for the current session

    @commands.command(name="taxation_manage", help="Rank: Leader | Descr.: Control panel to manage taxes for your country.")
    async def taxationmanage(self, ctx):
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

        # Create Country and Tax objects
        taxobj = tax.obj_checker(country)
        countryobj = clcountry.obj_checker(country)

        if taxobj and countryobj:
            self.tax_data = {
                "land_tax": taxobj.land_tax,
                "poll_tax": taxobj.poll_tax,
                "rent_tax": taxobj.rents,
                "customs": taxobj.customs,
                "tribute": taxobj.tribute,
                "ransoms": taxobj.ransoms,
                "central_demesne": taxobj.central_demesne,
                "extra_taxes": "unavailable at the moment",
                "annual_taxes": "unavailable at the moment"
            }

        # Start with the home page
        embed = self.create_embed(page=1, country=country)
        view = self.create_view(ctx, country)
        await ctx.send(embed=embed, view=view)

    def create_embed(self, page: int, country: str):
        """Creates an embed for the given page."""
        embed = nextcord.Embed(title=f"__Taxation Management:__ {country}", color=nextcord.Color(0xD3A839))
        country = clcountry.obj_checker(country)
        if page == 1:
            # Randomly choose a description and replace the placeholder with the country's king name
            description = random.choice(descriptions).format(king=country.king)
            
            # Split the description into smaller chunks for the fields
            field_length = 1024
            fields = [description[i:i+field_length] for i in range(0, len(description), field_length)]
            
            # Add each chunk of the description as a separate field
            for idx, field in enumerate(fields):
                embed.add_field(name=f"Page {page} - Part {idx+1}", value=field, inline=False)
            
            # Embed banner image
            embed.set_image(url="https://live.staticflickr.com/65535/54234146062_23aed5e9c8_b.jpg")  # Replace with your own image URL
            
            # Add a footer with the current page number
            embed.set_footer(text=f"Page {page}")

            return embed
        
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

        # Define the button callback for navigation and tax adjustment
        async def button_callback(interaction: nextcord.Interaction):
            if interaction.user != ctx.author:
                await interaction.response.send_message(
                    "Insufficient permission: You are not allowed to interact with this menu.",
                    ephemeral=True
                )
                return

            page = int(interaction.data["custom_id"].split("_")[1])
            embed = self.create_embed(page, country)
            new_view = self.create_view(ctx, country)
            embed = self.create_embed(page, country)
            new_view = self.create_view(ctx, country)
            taxobj = tax.obj_checker(country)  # Ensure taxobj is accessible here
            if 2 <= page <= 9:
                # Add tax adjustment buttons for tax pages
                tax_type = list(self.tax_data.keys())[page - 2]
                async def increase_callback(inter):
                    # Use the taxobj to call the increase_tax method
                    try:
                        taxobj.increase_tax(tax_type, 1)
                        self.tax_data[tax_type] = taxobj.get_key(tax_type)  # Update the dictionary value
                    except ValueError as e:
                        await inter.response.send_message(str(e), ephemeral=True)
                        return
                    embed_updated = self.create_embed(page, country)
                    await inter.response.edit_message(embed=embed_updated, view=self.create_view(ctx, country))
                
                async def decrease_callback(inter):
                    # Use the taxobj to call the decrease_tax method (assuming you have this method)
                    try:
                        taxobj.decrease_tax(tax_type, 1)
                        self.tax_data[tax_type] = taxobj.get_key(tax_type)  # Update the dictionary value
                    except ValueError as e:
                        await inter.response.send_message(str(e), ephemeral=True)
                        return
                    embed_updated = self.create_embed(page, country)
                    await inter.response.edit_message(embed=embed_updated, view=self.create_view(ctx, country))
                increase_button = Button(label="Increase", style=nextcord.ButtonStyle.success)
                decrease_button = Button(label="Decrease", style=nextcord.ButtonStyle.danger)
                
                increase_button.callback = increase_callback
                decrease_button.callback = decrease_callback
                
                new_view.add_item(increase_button)
                new_view.add_item(decrease_button)
                
            await interaction.response.edit_message(embed=embed, view=new_view)
        for i in range(1, 11):
            button = Button(label=f"Page {i}", style=nextcord.ButtonStyle.primary, custom_id=f"page_{i}")
            button.callback = button_callback
            view.add_item(button)

        return view


def setup(bot):
    bot.add_cog(TaxationV2(bot))

