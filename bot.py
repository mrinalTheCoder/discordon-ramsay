import discord
import os
from backend import search_recipe

client = discord.Client()
TOKEN = 'OTI2MDEzNDcyNjk5OTczNjcy.Yc1fQA.6EX2T7g8DK3KmbstOEbsWEPgfJk'

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	print(message.content)
	if message.content.startswith('!greet'):
		await message.channel.send('Hello!')
	if message.content.startswith('!search'):
		recipes = search_recipe(message.content[len('!search'):])
		for i in range(min(len(recipes), 5)):
			await message.channel.send(recipes[i])

client.run(TOKEN)
