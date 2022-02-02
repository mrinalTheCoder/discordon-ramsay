import discord
from discord.ext import commands
from discord import Color
import os
import backend

TOKEN = 'OTI2MDEzNDcyNjk5OTczNjcy.Yc1fQA.6EX2T7g8DK3KmbstOEbsWEPgfJk'
bot = commands.Bot(command_prefix='!')

nonveg_list = ['chicken', 'pork', 'mutton', 'meat', 'lamb', 'beef', 'fish', 'prawn', 'shrimp', 'poultry', 'oyster', 'lobster', 'crab', 'sausage', 'pepperoni', 'ham', 'bacon']

@bot.command()
async def greet(ctx):
	embed = discord.Embed(colour=discord.Colour.red())
	embed.add_field(name="Hello, my name is Discordon Ramsay. ", value="_Type !cmds to see what I can do!_", inline=True)
	await ctx.channel.send(embed=embed)

@bot.command()
async def cmds(ctx):
	embed = discord.Embed(colour=discord.Colour.red())
	embed.set_author(name='COMMAND LIST')
	embed.add_field(name='!search', value='Place this keyword before you search for the recipe of your choice ',
					inline=False)
	embed.add_field(name='!greet', value='For a greeting message', inline=False)
	embed.add_field(name='!bfast', value='For a hearty breakfast recipe!', inline=False)
	embed.add_field(name='!lunch', value='For a handpicked sumptuous lunch recipe!', inline=False)
	embed.add_field(name='!dinner', value='For a delicious dinner!', inline=False)
	embed.add_field(name='!drink' , value = 'For a refreshing drink' , inline =False)
	embed.add_field(name='!dessert' , value = 'For a savory sweet' , inline =False)

	await ctx.channel.send(embed=embed)


@bot.command()
async def search(ctx, arg):
	recipes = backend.search_recipe(arg)
	for i in range(min(len(recipes), 5)):
		img = recipes[i]['img']
		img = img.replace('%3A', ':')
		img = img.replace('%2F', '/')
		embed = discord.Embed(title=f"{i + 1}. {recipes[i]['name']}", url=recipes[i]['link'], color=0xEA3A44,
							  description=recipes[i]['desc'])
		embed.set_image(url=img)
		await ctx.channel.send(embed=embed)

	msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
	idx = int(msg.content[0]) - 1
	await ctx.channel.send(f'`Confirmed, recipe {idx + 1}`')
	details = backend.get_recipe_details(recipes[idx])
	embed = discord.Embed(title="Ingredients (4 servings)")
	for i in range(len(details['ing'])):
		embed.add_field(name=f'{i + 1}', value=details['ing'][i], inline=False)
	await ctx.channel.send(embed=embed)

	embed = discord.Embed(title='Instructions')
	for i in range(len(details['steps'])):
		embed.add_field(name=f'{i + 1}', value=details['steps'][i], inline=False)
	await ctx.channel.send(embed=embed)

async def send_recipe(ctx, recipes, details):
	img = recipes['img']
	img = img.replace('%3A', ':')
	img = img.replace('%2F', '/')
	embed = discord.Embed(title=f" {recipes['name']}", url=recipes['link'], color=0xEA3A44, description=recipes["desc"])
	embed.set_image(url=img)
	await ctx.channel.send(embed=embed)

	veg = True
	egg = False
	for i in details['ing']:
		if 'egg' in i:
			egg = True
		for j in nonveg_list:
			if j in i:
				veg = False

	if egg and veg:
		embed = discord.Embed(title="Ingredients (4 servings)\nContains Egg", color=Color.greyple())
	elif not veg:
		embed = discord.Embed(title="Ingredients (4 servings)\nNon Veg Recipe", color=Color.red())
	else:
		embed = discord.Embed(title="Ingredients (4 servings)\nVeg Recipe", color=Color.green())
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
	await send_recipe(ctx, recipes, details)

@bot.command()
async def lunch(ctx):
	recipes, details = backend.random_lunch()
	await send_recipe(ctx, recipes, details)

@bot.command()
async def dinner(ctx):
	recipes, details = backend.random_dinner()
	await send_recipe(ctx, recipes, details)

@bot.command()
async def drink(ctx):
	recipes, details = backend.random_drink()
	await send_recipe(ctx, recipes, details)

@bot.command()
async def dessert(ctx):
	recipes, details = backend.random_dessert()
	await send_recipe(ctx, recipes, details)

bot.run(TOKEN)
