import discum
import os
from keep_alive import keep_alive
import time
import discord
from dotenv import load_dotenv

config = load_dotenv(".env")




serverId = os.environ['SERVER_ID']
channelId = os.environ['CHANNEL_ID']
delay = os.environ['DELAY']
keep_alive()
token = os.environ['TOKEN']

bot = discum.Client(token)

print("Start")

def close_after_fetching(resp, guild_id):
    if bot.gateway.finishedMemberFetching(guild_id):
        lenmembersfetched = len(bot.gateway.session.guild(guild_id).members)
        print(str(lenmembersfetched)+' members fetched')
        bot.gateway.removeCommand({'function': close_after_fetching, 'params': {'guild_id': guild_id}})
        bot.gateway.close()

def get_members(guild_id, channel_id):
    bot.gateway.fetchMembers(guild_id, channel_id, keep="all", wait=1)
    bot.gateway.command({'function': close_after_fetching, 'params': {'guild_id': guild_id}})
    bot.gateway.run()
    bot.gateway.resetSession()
    return bot.gateway.session.guild(guild_id).members

members = get_members(serverId, channelId)
memberslist = []

for memberID in members:
    memberslist.append(memberID)
    print(memberID)

f = open('users.txt', "a")
for element in memberslist:
    f.write(element + '\n')
f.close()





client = discord.Client()

ids = open('users.txt', 'r')

print("Start Invites")

@client.event
async def on_connect():
    for id in ids:
        try:
            time.sleep(delay)
            user = await client.fetch_user(id)

            await user.send('f"send DM to: {id}"')
            print(f"send DM to: {id}")

        except ValueError:
            print(f"couldnt message: {user.name}, {ValueError} ")

keep_alive()
client.run(os.environ['TOKEN'], bot=False)
