# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
import discord
import os

TOKEN = os.environ['DISCORD_APP_USER_TOKEN']

client = discord.Client()


def get_channels(client):
    text_channel_list = list(client.get_all_channels())
    for channel in text_channel_list:
        print(channel.name, channel.type)
    return [channel for channel in text_channel_list if channel.type == discord.ChannelType.text]


@client.event
async def on_ready():
    channels = get_channels(client)
    print(channels)
    print(channels[0], channels[0].name)
    await client.send_message(channels[0], message)
    await client.close()


def post_announcement(msg):
    global message
    message = msg
    client.run(TOKEN)
