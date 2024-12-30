import nextcord
from nextcord.ext import commands
from nextcord.ui import Button, View
import classes.country as clcountry
from classes.country import Country
import classes.tax_settings as tax
from classes.tax_settings import Tax
import random

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
        if page == 1:
            # List of different randomized descriptions
            descriptions = [
                f"**Welcome to the Bureau of Taxation, Your Excellency, Egden {country.king}**\n\n"
                "You stand in a grand office, surrounded by towering shelves filled with ancient scrolls, dusty ledgers, and the faint scent of ink and parchment. A flickering candle illuminates the stone walls as the clattering of quills fills the air.\n\n"
                "At the far end of the room, an aged desk is cluttered with official documents awaiting your careful scrutiny. Before you lies the esteemed **Tax Management System**, a tool to ensure the prosperity and order of your domain.\n\n"
                "Use the buttons below to navigate through the various tax levies that keep the kingdom's coffers full and its people content.\n\n"
                "**Table of Contents**:\n"
                "2. **Land Tax** – A fair tribute for the vast stretches of fertile fields and grand estates.\n"
                "3. **Poll Tax** – A simple yet crucial levy upon all subjects of the realm.\n"
                "4. **Rent Tax** – For those who reside in the castles, towns, and cottages of the kingdom.\n"
                "5. **Customs** – The tariffs upon goods imported from foreign lands.\n"
                "6. **Tribute** – The honored dues owed by neighboring realms, securing alliances and peace.\n"
                "7. **Ransoms** – For those noble or otherwise who fall into the hands of captors.\n"
                "8. **Central Demesne** – The royal holdings from which all good subjects draw sustenance.\n"
                "9. **Extra Taxes** – Uncommon yet vital taxes to address unforeseen needs.\n"
                "10. **Collect Annual Taxes** – A solemn ritual to gather the fruits of the year's labor.",

                f"**Greetings, Noble Ruler, Egden {country.king}**\n\n"
                "Within the stone-clad walls of your grand office, a cold breeze sweeps through the towering windows. Ancient tomes and parchments line the walls, and the muffled sound of scribes furiously working can be heard from the adjoining chambers.\n\n"
                "At your desk sits the **Tax Management System**, the key to your kingdom's financial prosperity. As you survey the documents, you must make decisions that affect the very foundation of your realm.\n\n"
                "**Table of Contents**:\n"
                "2. **Land Tax** – A fair tribute for the vast stretches of fertile fields and grand estates.\n"
                "3. **Poll Tax** – A simple yet crucial levy upon all subjects of the realm.\n"
                "4. **Rent Tax** – For those who reside in the castles, towns, and cottages of the kingdom.\n"
                "5. **Customs** – The tariffs upon goods imported from foreign lands.\n"
                "6. **Tribute** – The honored dues owed by neighboring realms, securing alliances and peace.\n"
                "7. **Ransoms** – For those noble or otherwise who fall into the hands of captors.\n"
                "8. **Central Demesne** – The royal holdings from which all good subjects draw sustenance.\n"
                "9. **Extra Taxes** – Uncommon yet vital taxes to address unforeseen needs.\n"
                "10. **Collect Annual Taxes** – A solemn ritual to gather the fruits of the year's labor.",

                f"**Your Majesty, Egden {country.king}**\n\n"
                "The flickering firelight casts long shadows on the stone walls of your chambers. Piles of ledgers, scrolls, and quills fill the vast wooden desk, where only the faint scratch of the pen can be heard as you pore over the kingdom's finances.\n\n"
                "Before you lies the **Tax Management System**, an essential tool for keeping your kingdom’s economy flourishing and your people in check.\n\n"
                "**Table of Contents**:\n"
                "2. **Land Tax** – A fair tribute for the vast stretches of fertile fields and grand estates.\n"
                "3. **Poll Tax** – A simple yet crucial levy upon all subjects of the realm.\n"
                "4. **Rent Tax** – For those who reside in the castles, towns, and cottages of the kingdom.\n"
                "5. **Customs** – The tariffs upon goods imported from foreign lands.\n"
                "6. **Tribute** – The honored dues owed by neighboring realms, securing alliances and peace.\n"
                "7. **Ransoms** – For those noble or otherwise who fall into the hands of captors.\n"
                "8. **Central Demesne** – The royal holdings from which all good subjects draw sustenance.\n"
                "9. **Extra Taxes** – Uncommon yet vital taxes to address unforeseen needs.\n"
                "10. **Collect Annual Taxes** – A solemn ritual to gather the fruits of the year's labor.",

                f"**Welcome, Egden {country.king}**\n\n"
                "You sit in the dimly lit chamber, surrounded by towering shelves filled with dusty scrolls and the faint sound of a distant bell tolling. The air is thick with the weight of decisions yet to be made, and your desk is piled high with papers of great importance.\n\n"
                "Before you lies the **Tax Management System**, your trusted tool to uphold the kingdom's treasury and ensure the balance of power.\n\n"
                "**Table of Contents**:\n"
                "2. **Land Tax** – A fair tribute for the vast stretches of fertile fields and grand estates.\n"
                "3. **Poll Tax** – A simple yet crucial levy upon all subjects of the realm.\n"
                "4. **Rent Tax** – For those who reside in the castles, towns, and cottages of the kingdom.\n"
                "5. **Customs** – The tariffs upon goods imported from foreign lands.\n"
                "6. **Tribute** – The honored dues owed by neighboring realms, securing alliances and peace.\n"
                "7. **Ransoms** – For those noble or otherwise who fall into the hands of captors.\n"
                "8. **Central Demesne** – The royal holdings from which all good subjects draw sustenance.\n"
                "9. **Extra Taxes** – Uncommon yet vital taxes to address unforeseen needs.\n"
                "10. **Collect Annual Taxes** – A solemn ritual to gather the fruits of the year's labor.",

                f"**Greetings, Honorable Egden {country.king}**\n\n"
                "You are seated in a well-lit office, adorned with maps of your lands and intricate paintings of your ancestors. The scent of parchment and ink fills the air, and the faint sound of scribes’ quills can be heard from the adjoining chambers.\n\n"
                "Your trusted **Tax Management System** lies before you, ready to assist in managing the kingdom’s finances and ensuring that all subjects contribute their due share.\n\n"
                "**Table of Contents**:\n"
                "2. **Land Tax** – A fair tribute for the vast stretches of fertile fields and grand estates.\n"
                "3. **Poll Tax** – A simple yet crucial levy upon all subjects of the realm.\n"
                "4. **Rent Tax** – For those who reside in the castles, towns, and cottages of the kingdom.\n"
                "5. **Customs** – The tariffs upon goods imported from foreign lands.\n"
                "6. **Tribute** – The honored dues owed by neighboring realms, securing alliances and peace.\n"
                "7. **Ransoms** – For those noble or otherwise who fall into the hands of captors.\n"
                "8. **Central Demesne** – The royal holdings from which all good subjects draw sustenance.\n"
                "9. **Extra Taxes** – Uncommon yet vital taxes to address unforeseen needs.\n"
                "10. **Collect Annual Taxes** – A solemn ritual to gather the fruits of the year's labor."
            ]

            # Randomly choose a description
            embed.description = random.choice(descriptions)
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

