import discord
from discord.ext import commands
import os
import backend

TOKEN = 'OTI2MDEzNDcyNjk5OTczNjcy.Yc1fQA.6EX2T7g8DK3KmbstOEbsWEPgfJk'
bot = commands.Bot(command_prefix='!')

@bot.command()
async def greet(ctx):
	await ctx.channel.send('hello')

@bot.command()
async def cmds(ctx):
	embed = discord.Embed(colour=discord.Colour.red())
	embed.set_author(name='COMMAND LIST')
	embed.add_field(name='!search', value='Place this keyword before you search for the recipe of your choice ', inline=True)
	embed.add_field(name='!greet', value='For a greeting message', inline=True)
	embed.add_field(name= '!bfast', value='For a hearty breakfast recipe!' , inline = True)
	embed.add_field(name= '!lunch', value='For a handpicked sumptuous lunch recipe!' , inline = True)
	embed.add_field(name= '!dinner', value='For a delicious dinner!' , inline = True)
	
	await ctx.channel.send(embed=embed)

@bot.command()
async def search(ctx, arg):
	recipes = backend.search_recipe(arg)
	for i in range(min(len(recipes), 5)):
		img = recipes[i]['img']
		img = img.replace('%3A', ':')
		img = img.replace('%2F', '/')
		embed = discord.Embed(title=f"{i + 1}. {recipes[i]['name']}", url=recipes[i]['link'], color=0xEA3A44, description=recipes[i]['desc'])
		embed.set_image(url=img)
		await ctx.channel.send(embed=embed)

	msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
	idx = int(msg.content[0]) - 1
	await ctx.channel.send(f'`Confirmed, recipe {idx + 1}`')
	details = backend.get_recipe_details(recipes[idx])
	embed = discord.Embed(title="Ingredients(4 servings)")
	for i in range(len(details['ing'])):
		embed.add_field(name=f'{i + 1}', value=details['ing'][i], inline=False)
	await ctx.channel.send(embed=embed)

	embed = discord.Embed(title='Instructions')
	for i in range(len(details['steps'])):
		embed.add_field(name=f'{i + 1}', value=details['steps'][i], inline=False)
	await ctx.channel.send(embed=embed)

@bot.command()
async def bfast(ctx):
	recipes, details = backend.random_bfast()
	img = recipes['img']
	img = img.replace('%3A', ':')
	img = img.replace('%2F', '/')
	embed = discord.Embed(title=f" {recipes['name']}", url=recipes['link'], color=0xEA3A44, description=recipes["desc"])
	embed.set_image(url=img)
	await ctx.channel.send(embed=embed)

	embed = discord.Embed(title="Ingredients (4 servings)")
	for i in range(len(details['ing'])):
		embed.add_field(name=f'{i + 1}', value=details['ing'][i], inline=False)
	await ctx.channel.send(embed=embed)

	embed = discord.Embed(title='Instructions')
	for i in range(len(details['steps'])):
		embed.add_field(name=f'{i + 1}', value=details['steps'][i], inline=False)
	await ctx.channel.send(embed=embed)

bot.run(TOKEN)
