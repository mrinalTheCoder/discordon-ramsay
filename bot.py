import discord
import os

client = discord.Client()
TOKEN = 'OTI2MDEzNDcyNjk5OTczNjcy.Yc1fQA.6EX2T7g8DK3KmbstOEbsWEPgfJk'

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!greet'):
        await message.channel.send('Hello!')
client.run(TOKEN)
