import nextcord
from nextcord.ext import commands
from nextcord.ui import Button, View

class CountryTaxManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tax_manager(self, ctx):
        # Create the embed
        embed = nextcord.Embed(
            title="🏛️ Country Tax Manager",
            description=(
                "Manage taxes for your country with ease! Use the buttons below to perform actions.\n\n"
                "**Current Status:**\n"
                "📊 **Land Tax:** 15%\n"
                "📊 **Poll Tax:** 15%\n"
                "📊 **Rents:** 15%\n"
                "📊 **Customs:** 15%\n"
                "📊 **Tribute:** 15%\n"
                "📊 **Ransoms:** 15%\n"
                "📊 **Central Demesne:** 15%\n"
                "📈 **Projected Revenue:** 750,000 Gold\n\n"
                "_Select an option below to manage your country's economy._"
            ),
            color=nextcord.Color.blue()
        )
        embed.set_thumbnail(url="https://example.com/tax_icon.png")  # Replace with a relevant image URL
        embed.set_footer(text="Country Tax Manager | Powered by SamyorBOT")

        # Create buttons
        increase_button = Button(label="Increase Land Tax", style=nextcord.ButtonStyle.primary, emoji="🔺")
        decrease_button = Button(label="Decrease Land Tax", style=nextcord.ButtonStyle.primary, emoji="🔻")
        collect_button = Button(label="Collect Annual Taxes", style=nextcord.ButtonStyle.success, emoji="💰")
        stats_button = Button(label="View Stats", style=nextc
