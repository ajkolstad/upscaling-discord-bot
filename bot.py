from pathlib import Path

import discord

import upscaler
from upscale import Upscale


def run_discord_bot():
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

        # print("Got message '" + user_message + "' from user '" + username + "' in channel '" + channel + "'")

        if user_message[0] == "!":
            user_message = user_message[1:]

            p_message = user_message.lower()

            if p_message == "upscale v1":
                response = (
                    "Starting the upscaling process with the V1 upscaler. I'll let you when I'm done, <@"
                    + user_id
                    + ">"
                )
                await message.channel.send(response)
                await client.change_presence(
                    status=discord.Status.online,
                    activity=discord.Game("Looking for new files"),
                )

                new_files = upscaler.get_new_files()

                if len(new_files) == 0:
                    await client.change_presence(
                        status=discord.Status.online,
                        activity=discord.Game("No new files found"),
                    )
                    response = (
                        "Hey, <@"
                        + user_id
                        + ">,  I looked for new files to upscale, but I didn't find any. If you want me to try again, delete all of the images in the Output folder, then run `!upscale` again."
                    )
                    await message.channel.send(response)
                    return

                print(new_files)

                await client.change_presence(
                    status=discord.Status.online,
                    activity=discord.Game("Downloading new files"),
                )

                upscaler.download_new_files(new_files)

                await client.change_presence(
                    status=discord.Status.online,
                    activity=discord.Game(
                        "Upscaling " + str(len(new_files)) + "file(s)"
                    ),
                )

                upscale = Upscale(
                    model=upscaler.V1_PATH,
                    input=Path("input"),
                    output=Path("output"),
                    reverse=False,
                    skip_existing=True,
                    delete_input=False,
                    seamless=False,
                    cpu=False,
                    fp16=(upscaler.V1_PATH != upscaler.V2_PATH),
                    device_id=0,
                    cache_max_split_depth=False,
                    binary_alpha=False,
                    ternary_alpha=False,
                    alpha_threshold=0.5,
                    alpha_boundary_offset=0.2,
                    alpha_mode=None,
                )

                upscale.run()

                await client.change_presence(
                    status=discord.Status.online, activity=discord.Game("Finished up")
                )
                response = ""
                if len(new_files) == 1:
                    response = (
                        "Hey, <@"
                        + user_id
                        + ">,  I finished upscaling that image you wanted. It's in the Output folder now. Let me know if you want any more images upscaled."
                    )
                else:
                    response = (
                        "Hey, <@"
                        + user_id
                        + ">,  I finished upscaling those "
                        + str(len(new_files))
                        + " images you wanted. They're in the Output folder now. Let me know if you want any more images upscaled."
                    )
                await message.channel.send(response)
                return

            elif p_message == "upscale v2":
                response = (
                    "Starting the upscaling process with the V2 upscaler. I'll let you when I'm done, <@"
                    + user_id
                    + ">"
                )
                await message.channel.send(response)
                await client.change_presence(
                    status=discord.Status.online,
                    activity=discord.Game("Looking for new files"),
                )

                new_files = upscaler.get_new_files()

                if len(new_files) == 0:
                    await client.change_presence(
                        status=discord.Status.online,
                        activity=discord.Game("No new files found"),
                    )
                    response = (
                        "Hey, <@"
                        + user_id
                        + ">,  I looked for new files to upscale, but I didn't find any. If you want me to try again, delete all of the images in the Output folder, then run `!upscale` again."
                    )
                    await message.channel.send(response)
                    return

                await client.change_presence(
                    status=discord.Status.online,
                    activity=discord.Game("Downloading new files"),
                )

                upscaler.download_new_files(new_files)

                await client.change_presence(
                    status=discord.Status.online,
                    activity=discord.Game(
                        "Upscaling " + str(len(new_files)) + "file(s)"
                    ),
                )

                upscale = Upscale(
                    model=upscaler.V2_PATH,
                    input=Path("input"),
                    output=Path("output"),
                    reverse=False,
                    skip_existing=True,
                    delete_input=False,
                    seamless=False,
                    cpu=False,
                    fp16=(upscaler.V2_PATH != upscaler.V2_PATH),
                    device_id=0,
                    cache_max_split_depth=False,
                    binary_alpha=False,
                    ternary_alpha=False,
                    alpha_threshold=0.5,
                    alpha_boundary_offset=0.2,
                    alpha_mode=None,
                )

                upscale.run()

                await client.change_presence(
                    status=discord.Status.online, activity=discord.Game("Finished up")
                )
                response = ""
                if len(new_files) == 1:
                    response = (
                        "Hey, <@"
                        + user_id
                        + ">,  I finished upscaling that image you wanted. It's in the Output folder now. Let me know if you want any more images upscaled."
                    )
                else:
                    response = (
                        "Hey, <@"
                        + user_id
                        + ">,  I finished upscaling those "
                        + str(len(new_files))
                        + " images you wanted. They're in the Output folder now. Let me know if you want any more images upscaled."
                    )
                await message.channel.send(response)
                return

            elif p_message == "help":
                response = "Commands:\n- `!upscale v1` Upscales images using the V1 upscaling model\n- `!upscale v2` Upscales images using the V2 upscaling model"
                await message.channel.send(response)

            else:
                response = "Sorry, I didn't understand that command. Here's what I can do:\n- `!upscale v1` Upscales images using the V1 upscaling model\n- `!upscale v2` Upscales images using the V2 upscaling model\nIf none of these commands do what you want to do, ask <@140270240562020352> if they can add that functionality for you."
                await message.channel.send(response)
        else:
            return

    client.run(DISCORD_TOKEN)
