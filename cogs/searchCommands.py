from googleSearch import GoogleSearch
import aiohttp
import os
import random
from main import Main
import discord
from discord.ext import commands

class SearchCommands(commands.Cog, name="Search Commands", description='Commands for searching images or links'):

	@commands.command(name='image', help='used to get an image from google, based off a search term')
	async def image(self, ctx, *, search):
		keywords, searchwords = GoogleSearch.key_words_search_words(GoogleSearch, user_message=search)
		links = GoogleSearch.imagesearch(GoogleSearch, additional=True, keywords=keywords)
		image = random.choice(links)
		embed = discord.Embed(title=f"Google Images: {search}", color = ctx.author.color)
		embed.set_image(url=image)
		await ctx.send(embed=embed)

	no_result_message = 'either no results, or sumn happened'
	
	@commands.command(name='search', help='to search using a search term')
	async def search(self, ctx, *, content):
		key_words, search_words = GoogleSearch.key_words_search_words(GoogleSearch, user_message=content)
		result_links = GoogleSearch.search(GoogleSearch, keywords=key_words)
		links = GoogleSearch.send_link(GoogleSearch, result_links, search_words)

		x = 0
		if len(links) > 0:
			while x != 5:
				await ctx.send(links[x])
				x += 1
		else:
		  await ctx.send(SearchCommands.no_result_message)

	@commands.command(name='dog', help='gets a random dog')
	async def random_dog(self, ctx):
		async with aiohttp.ClientSession() as cs:
			async with cs.get("https://random.dog/woof.json") as r:
				data = await r.json()
				embed = discord.Embed(title="Doggo", color = ctx.author.color)
				embed.set_image(url=data['url'])
				await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(SearchCommands(bot))