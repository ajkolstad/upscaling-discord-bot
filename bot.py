import asyncio
import functools
import os
from typing import Callable, Coroutine, List

import discord
from discord.ext import commands, tasks
from dotenv import dotenv_values

import frontend
from lib import (
    initialize_settings_file,
    read_status_from_settings_file,
    write_status_to_settings_file,
)

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="!", intents=intents)


def to_thread(func: Callable) -> Coroutine:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.to_thread(func, *args, **kwargs)

    return wrapper


@to_thread
def handle_command(message_args: List[str]) -> str:
    print(message_args, flush=True)

    if message_args[0] == "set":
        if message_args[1] == "model":
            if message_args[2] == "blackwhite":
                return frontend.set_default_bw_model(message_args[3])
            if message_args[2] == "color":
                return frontend.set_default_c_model(message_args[3])
        if message_args[1] == "bitmap":
            return frontend.set_bitmap_mode(message_args[2])
    if message_args[0] == "show":
        if message_args[1] == "models":
            if message_args[2] == "all":
                return frontend.list_all_models()
            if message_args[2] == "blackwhite":
                return frontend.list_bw_models()
            if message_args[2] == "color":
                return frontend.list_c_models()
        if message_args[1] == "settings":
            return frontend.list_settings()
    if message_args[0] == "help":
        return frontend.list_commands()
    if message_args[0] == "upscale":
        if (
                read_status_from_settings_file() != frontend.IDLE_STATUS
                and read_status_from_settings_file() != frontend.FAIL_STATUS
        ):
            return "The upscaler is already working on a batch. Please wait for it to finish before starting a new one."
        else:
            return frontend.upscale_process(message_args[1], status_to_file=True)
    return (
        "I'm sorry, but I did not understand that command\n" + frontend.list_commands()
    )


@client.event
async def on_ready():
    print(str(client.user) + " is now running!", flush=True)
    status_loop.start()


@tasks.loop(seconds=5)  # repeat after every 5 seconds
async def status_loop():
    initialize_settings_file()
    status = read_status_from_settings_file()
    await client.change_presence(activity=discord.CustomActivity(name=status))


@client.command(pass_context=True)
async def upscaler(ctx, *args):
    res = await handle_command(args)
    print(res, flush=True)
    await ctx.send(res)


write_status_to_settings_file("Idle")

try:
    DISCORD_TOKEN = dotenv_values(".env")["DISCORD_TOKEN"]
except KeyError:
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
client.run(DISCORD_TOKEN)
