#Unifox Discord Bot
#FurryCommands.py

#---Imports Section---
from googleSearch import GoogleSearch
import aiohttp
import ssl
import certifi
import random
from main import Main
import discord
from discord.ext import commands
import json

#---furry commands class---
#houses all the commands for furries :)
class Furry(commands.Cog, name="Furry Commands", description="Commands for furries ;)"):

	#command to glomp on someone lol
	@commands.command(name='glomp', help='glomp on someone ;)')
	async def glomp(self, ctx, *, user: discord.Member):
		try:
			await ctx.send(f'{ctx.author.mention} jumps at {user.mention}, knocking the to the ground in a hug UwU')
		except:
			await ctx.send('Sorry, idk that person.')

	#a basic hug uwu
	@commands.command(name='hug', help='hug someone')
	async def hug(self, ctx, *, user: discord.Member):
		try:
			await ctx.send(f'{ctx.author.mention} hugs {user.mention}.')
		except:
			await ctx.send('Sorry, idk them.')

	#pet someone
	@commands.command(name='pet', help='pet someone')
	async def pet(self, ctx, *, user: discord.Member):
		try:
			await ctx.send(f'{ctx.author.mention} gently pats {user.mention} on the head.')
		except:
			await ctx.send('Couldn\'t find the person to pet...')

	#make everyone deaf lol
	@commands.command(name='scream', help='just fox scream lol')
	async def scree(self, ctx):
		await ctx.send(f'{ctx.author.mention}, if not already, turns into a fox. They then let out a loud screeeeeee. Everyone at this channel is now temporarily deaf, and the scream can be heard in all channels through this server. Don\'t be mad at me, it was {ctx.author.mention} who did it.')

	#furpile tracking vars
	furpilestarted = False
	furpilecount = 0

	#start, join, or bring someone to a furpile
	#I still need to add a timeout to end the pile if no one does anything with it
	@commands.command(name='furpile', help='Join or make a furpile :)')
	async def furpile(self, ctx, *, user: discord.Member=None):
		if user == None and FurryCommands.furpilestarted == False:
			await ctx.send('you have to start it with someone')
		elif user == None:
			await ctx.send(f'{ctx.author.mention} has joined the furpile')
			FurryCommands.furpilecount += 1
		elif not user == None and FurryCommands.furpilestarted == False:
			await ctx.send(f'{ctx.author.mention} started a furpile with {user.mention}')
			FurryCommands.furpilestarted = True
			FurryCommands.furpilecount = 2
		elif not user == None and FurryCommands.furpilestarted == True:
			await ctx.send(f'{ctx.author.mention} joined, bringing {user.mention} with them')
			FurryCommands.furpilecount += 2

#---NSFW furry commands class ;)---
#houses all the fun furry commands
class NSFWFurryCommands(commands.Cog, name="NSFW Furry Commands", description="The fun commands for furries ;)"):

	#a yiff command for searching e621
	#gets a big list of posts that have tag(s) that were searched for from e621
	#if the list is empty is says so
	#but if its not, it selects a random post and sends it
	#makes sure the post isn't a webm, because I couldn't get it working with webm video
	@commands.command(name='yiff', help='Searches e621.net based off a search term')
	async def yiff(self, ctx, *, search='gay'):
		if ctx.channel.is_nsfw():
			tosearch=search
			keywords, searchwords = GoogleSearch.key_words_search_words(GoogleSearch, user_message=tosearch)
			print(f'got keywords: {keywords}\n from {search}')
			cs = aiohttp.ClientSession()
			print('got client session')
			headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
			r = await cs.get(f'https://e621.net/posts.json?tags={keywords}+-watersports+-scat+-vore+-gore+-loli+-shota+order:score+type:jpg+type:png&limit=50', headers=headers)
			print('got e6 link')
			print(r.status)
			if r.status == 200:
				data = await r.json(content_type=None)
				print(len(data['posts']))
				if len(data['posts']) == 0:
					return await ctx.send('No results!')
				post = random.choice(data['posts'])
				file = post['file']
				embed = discord.Embed(title="e621: "+search, color = ctx.author.color)
				embed.set_image(url=file['url'])
				await ctx.send(embed=embed)
				print(file['url'])
			else:
				await ctx.send(f'Problem status: {r.status}')
			await cs.close()
		else:
			await ctx.send('Command must be used in nsfw channel!!!')

#---setup function---
#sets up the cogs ig idk
def setup(bot):
	bot.add_cog(Furry(bot))
	bot.add_cog(NSFWFurryCommands(bot))
