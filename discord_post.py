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
    channel = find_channel(channels, os.environ['DISCORD_CHANNEL'])
    if not channel:
        channel = channels[0]
    await client.send_message(channel, message)
    await client.close()


def find_channel(channels, name):
    for channel in channels:
        if channel.name == name:
            return channel
    return None


def post_announcement(msg):
    global message
    message = msg
    client.run(TOKEN)
