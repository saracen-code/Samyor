import nextcord
from nextcord.ext import commands, tasks
import os
import json
import sys
import utils.operations_writer as ow
import utils.operations_executer as oe
import classes.country as clcountry
import asyncio
from keys import TOKEN

operations_refresh_time = 20  # seconds
single_operation_time = 0.5  # seconds

# Create a bot instance with a command prefix
intents = nextcord.Intents.default()
intents.message_content = True  # Required for reading message content
bot = commands.Bot(command_prefix="!", intents=intents)

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    # Start the operations task once the bot is ready
    execute_operations.start()

# Initialize the spreadsheet
@bot.command()
async def initialize(ctx):
    clcountry.initializeExistingCountries_asOBJ()

clcountry.initializeExistingCountries_asOBJ()

# Load and unload cogs
if __name__ == "__main__":
    cwd = os.getcwd()
    for file in os.listdir(cwd + "/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")

# Async function to handle operations continuously
@tasks.loop(seconds=operations_refresh_time)
async def execute_operations():
    operations = oe.read_operations('operations.txt')
    if operations:
        for operation in operations:
            await execute_single_operation(operation)
            await asyncio.sleep(single_operation_time)
            oe.remove_operation_from_file(operation["ID"])

# Define the async operation function
async def execute_single_operation(operation):
    # This should be the async version of executing the operation
    oe.execute_single_operation(operation)

# Run the bot
bot.run(TOKEN)
