import nextcord
from nextcord.ext import commands

class Market(commands.Cog):
    """Cog for the Markets."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def market(self, ctx):
        """Displays the Market."""
        embed = nextcord.Embed(
            title="Ghallab Market",
            description=(
                "Welcome to the bustling **Ghallab Market**! Here, you can find items essential for "
                "your adventures and daily life. Browse the categories below and make your purchases wisely!"
            ),
            color=nextcord.Color.gold()
        )

        # Weapons Section
        embed.add_field(
            name="**Weapons**",
            value=(
                "![⚔️](https://example.com/sword_icon.png) **Iron Sword**: 50 gold\n"
                "![🪓](https://example.com/axe_icon.png) **Steel Axe**: 75 gold\n"
                "![🏹](https://example.com/bow_icon.png) **Bow & Arrows**: 60 gold\n"
                "![🗡️](https://example.com/dagger_icon.png) **Enchanted Dagger**: 150 gold"
            ),
            inline=False
        )

        # Armor Section
        embed.add_field(
            name="**Armor**",
            value=(
                "![🛡️](https://example.com/shield_icon.png) **Leather Armor**: 100 gold\n"
                "![⚙️](https://example.com/chainmail_icon.png) **Chainmail**: 200 gold\n"
                "![🛡️](https://example.com/shield_icon2.png) **Iron Shield**: 120 gold\n"
                "![🧥](https://example.com/cloak_icon.png) **Mage's Cloak**: 180 gold"
            ),
            inline=False
        )

        # Food & Supplies Section
        embed.add_field(
            name="**Food & Supplies**",
            value=(
                "!🍞**Flour (0.45 kg)**: 5 gold\n"
                "!🧪https://example.com/potion_icon.png **Healing Potion**: 20 gold\n"
                "!🎒https://example.com/rations_icon.png **Travel Rations**: 10 gold\n"
                "!🔥https://example.com/torch_icon.png **Torch**: 2 gold"
            ),
            inline=False
        )

        # Special Items Section
        embed.add_field(
            name="**Special Items**",
            value=(
                "![💍](https://i.ibb.co/wzSyGDC/gem-4752251.png) **Jewel**: 300 gold\n"
                "![⚡](https://example.com/amulet_icon.png) **Amulet of Strength**: 400 gold\n"
                "![👁️](https://example.com/invisibility_icon.png) **Potion of Invisibility**: 500 gold\n"
                "![📜](https://example.com/scroll_icon.png) **Mystic Scroll**: 350 gold"
            ),
            inline=False
        )
        embed.set_author(
            name="Ghallab Market",
            icon_url="https://i.ibb.co/rpKG9Rw/stall-10492800.png")  # Replace with your castle image URL
        embed.set_footer(text="Type '!buy [item name]' to purchase an item.")
        embed.set_thumbnail(url="https://live.staticflickr.com/65535/54235510505_83546d60fa_b.jpg")  # Replace with your image URL
        embed.set_image(url="https://cdna.artstation.com/p/assets/images/images/056/537/630/large/jama-jurabaev-shot1.jpg?1669500016")  # Replace with your banner image URL

        await ctx.send(embed=embed)

# Setup function to add the cog to the bot
def setup(bot):
    bot.add_cog(Market(bot))