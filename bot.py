import sys

import discord
from discord.ext import commands
from dotenv import dotenv_values

from frontend import handle_command

try:
    DISCORD_TOKEN = dotenv_values(".env")["DISCORD_TOKEN"]
    if DISCORD_TOKEN is None or DISCORD_TOKEN == "":
        raise KeyError
except KeyError:
    print("Please enter your discord token in the .env file")
    sys.exit(0)


intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    print(str(client.user) + " is now running!")


@client.command(pass_context=True)
async def upscaler(ctx, *args):
    await ctx.send(handle_command(list(args)))


client.run(DISCORD_TOKEN)


"""def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(str(client.user) + " is now running!")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        print(message)

        username = str(message.author)
        user_id = str(message.author.id)
        user_message = str(message.content)
        channel = str(message.channel)

        print(
            "Got message '"
            + user_message
            + "' from user '"
            + username
            + "' in channel '"
            + channel
            + "'"
        )

        if user_message[0] == "!":
            user_message = user_message[1:]

            user_command = user_message.lower()

            response = handle_command(user_command)

            await message.channel.send(response)
        else:
            return
"""
