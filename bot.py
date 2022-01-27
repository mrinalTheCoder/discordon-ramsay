import discord
from discord.ext import commands
import os
from backend import search_recipe

TOKEN = 'OTI2MDEzNDcyNjk5OTczNjcy.Yc1fQA.6EX2T7g8DK3KmbstOEbsWEPgfJk'
bot = commands.Bot(command_prefix='!')

@bot.command()
async def greet(ctx):
	await ctx.channel.send('hello')

@bot.command()
async def search(ctx, arg):
	recipes = search_recipe(arg)
	for i in range(min(len(recipes), 5)):
		img = recipes[i]['img']
		img = img.replace('%3A', ':')
		img = img.replace('%2F', '/')
		embed = discord.Embed(title=f"{i+1}. {recipes[i]['name']}", url=recipes[i]['link'], color=0xEA3A44)
		embed.set_image(url=img) 
		await ctx.channel.send(embed=embed)
	
	msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
	await ctx.channel.send(f'`Confirmed, recipe {msg.content}`')

bot.run(TOKEN)
'''import discord
from discord.ext import commands
import os
from backend import search_recipe
import emoji

TOKEN = 'OTI2MDEzNDcyNjk5OTczNjcy.Yc1fQA.6EX2T7g8DK3KmbstOEbsWEPgfJk'
bot = commands.Bot(command_prefix='!')

@bot.command()
async def greet(ctx):
	await ctx.channel.send('hello')

@bot.command()
async def search(ctx, arg):
	recipes = search_recipe(arg)
	for i in range(min(len(recipes), 5)):
		img = recipes[i]['img']
		img = img.replace('%3A', ':')
		img = img.replace('%2F', '/')
		embed = discord.Embed(title=f"{i+1}. {recipes[i]['name']}", url=recipes[i]['link'], color=0xEA3A44)
		embed.set_image(url=img) 
		await ctx.channel.send(embed=embed)
	
	msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
	await ctx.channel.send(f'`Confirmed, recipe {msg.content}`')
@bot.command()
async def cmds(ctx):
    embed = discord.Embed(
        colour = discord.Colour.red() )
    embed.set_author(name = 'COMMAND LIST')
    embed.add_field(name = '!search', value = 'place this keyword before you search for any recipe',inline=True)
    embed.add_field(name = '!greet', value = 'for a greeting message',inline=False)
    
    await ctx.channel.send( embed=embed)
bot.run(TOKEN)'''
