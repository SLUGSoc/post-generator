# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
import os
import requests

def post_announcement(msg):
    r = requests.post(os.environ['DISCORD_WEBHOOK_URL'], data={'content': msg})
    print(r.status_code, r.reason)
    return r
