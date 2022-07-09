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
			if ctx.author == user:
				await ctx.send("You can't glomp yourself")
			else:
				await ctx.send(f'{ctx.author.mention} jumps at {user.mention}, knocking them to the ground in a hug, whispering "I love you" UwU')
		except:
			await ctx.send('Sorry, idk that person.')

	#a basic hug uwu
	@commands.command(name='hug', help='hug someone')
	async def hug(self, ctx, *, user: discord.Member):
		try:
			if ctx.author == user:
				await ctx.send("You can't hug yourself")
			else:
				await ctx.send(f'{ctx.author.mention} hugs {user.mention}.')
		except:
			await ctx.send('Sorry, idk them.')

	#pet someone
	@commands.command(name='pet', aliases=['pat'], help='pet someone, also (prefix)pat')
	async def pet(self, ctx, *, user: discord.Member):
		try:
			if ctx.author == user:
				await ctx.send("You can't pet yourself")
			else:
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
	fursinpile = list()

	#start, join, or bring someone to a furpile
	#I still need to add a timeout to end the pile if no one does anything with it
	@commands.command(name='furpile', help='Join or make a furpile :)')
	async def furpile(self, ctx, *, user: discord.Member=None):
		if user == None and Furry.furpilestarted == False:
			await ctx.send('you have to start it with someone')
		elif Furry.furpilestarted == True and ctx.author in Furry.fursinpile and not Main.bot.author_id == ctx.author.id:
			await ctx.send('you are already in the pile!')
		elif Furry.furpilestarted == True and ctx.author in Furry.fursinpile and Main.bot.author_id == ctx.author.id and not user in Furry.fursinpile:
			Furry.furpilecount += 1
			await ctx.send(f'You somehow get {user.mention} on the pile \nThere are {Furry.furpilecount} furs in the pile.')
		elif Furry.furpilestarted == True and ctx.author in Furry.fursinpile and Main.bot.author_id == ctx.author.id and user in Furry.fursinpile:
			await ctx.send(f'{user.mention} is on the pile')
		elif Furry.furpilestarted == True and user in Furry.fursinpile and not ctx.author in Furry.fursinpile:
			Furry.furpilecount += 1
			await ctx.send(f'{user.mention} is already in the pile, but {ctx.author.mention} joins the pile \nThere are {Furry.furpilecount} furs in the pile.')
			Furry.fursinpile.append(ctx.author)
		elif user == None:
			Furry.furpilecount += 1
			await ctx.send(f'{ctx.author.mention} has joined the furpile \nThere are {Furry.furpilecount} furs in the pile.')
			Furry.fursinpile.append(ctx.author)
		elif not user == None and Furry.furpilestarted == False:
			Furry.furpilecount = 2
			await ctx.send(f'{ctx.author.mention} started a furpile with {user.mention} \nThere are {Furry.furpilecount} furs in the pile.')
			Furry.furpilestarted = True
			Furry.fursinpile.append(ctx.author)
			Furry.fursinpile.append(user)
		elif not user == None and Furry.furpilestarted == True:
			Furry.furpilecount += 2
			await ctx.send(f'{ctx.author.mention} joined, bringing {user.mention} with them \nThere are {Furry.furpilecount} furs in the pile.')
			Furry.fursinpile.append(ctx.author)
			Furry.fursinpile.append(user)

	@commands.command(name='leavepile', help='leave the furpile :(')
	async def leavepile(self, ctx):
		if not ctx.author in Furry.fursinpile:
			return await ctx.send('You are not in the pile')
		if Furry.furpilecount > 1:
			if Furry.fursinpile[len(Furry.fursinpile)-1] == ctx.author:
				await ctx.send('You hop off the pile')
				Furry.fursinpile.pop(len(Furry.fursinpile)-1)
			else:
				await ctx.send('You manage to wiggle out of the pile')
				Furry.fursinpile.pop(Furry.fursinpile.index(ctx.author))
		else:
			await ctx.send('You are the last person, You get up and leave')
			Furry.fursinpile.pop(0)
			Furry.furpilestarted = False
		Furry.furpilecount -= 1
		await ctx.send(f'There are {Furry.furpilecount} furs in the pile.')

	congastarted = False
	congacount = 0
	fursinconga = list()

	@commands.command(name='conga', help='Join or make a conga line!')
	async def conga(self, ctx, *, user: discord.Member=None):
		if user == None and Furry.congastarted == False:
			await ctx.send('you have to start it with someone')
		elif Furry.congastarted == True and ctx.author in Furry.fursinconga and not Main.bot.author_id == ctx.author.id:
			await ctx.send('you are already in the conga!')
		elif Furry.congastarted == True and ctx.author in Furry.fursinconga and Main.bot.author_id == ctx.author.id and not user in Furry.fursinconga:
			Furry.congacount += 1
			await ctx.send(f'You leave and bring {user.mention} to the conga \nThere are {Furry.congacount} furs in the conga.' + (f'{Main.bot.get_emoji(950891145339220048)}'*Furry.congacount))
		elif Furry.congastarted == True and ctx.author in Furry.fursinconga and Main.bot.author_id == ctx.author.id and user in Furry.fursinconga:
			await ctx.send(f'{user.mention} is in the conga')
		elif Furry.congastarted == True and user in Furry.fursinconga and not ctx.author in Furry.fursinconga:
			Furry.congacount += 1
			await ctx.send(f'{user.mention} is already in the conga, but {ctx.author.mention} joins the conga \nThere are {Furry.congacount} furs in the conga.' + (f'{Main.bot.get_emoji(950891145339220048)}'*Furry.congacount))
			Furry.fursinconga.append(ctx.author)
		elif user == None:
			Furry.congacount += 1
			await ctx.send(f'{ctx.author.mention} has joined the conga \nThere are {Furry.congacount} furs in the conga.' + (f'{Main.bot.get_emoji(950891145339220048)}'*Furry.congacount))
			Furry.fursinconga.append(ctx.author)
		elif not user == None and Furry.congastarted == False:
			Furry.congacount = 2
			await ctx.send(f'{ctx.author.mention} started a conga with {user.mention} \nThere are {Furry.congacount} furs in the conga.' + (f'{Main.bot.get_emoji(950891145339220048)}'*Furry.congacount))
			Furry.congastarted = True
			Furry.fursinconga.append(ctx.author)
			Furry.fursinconga.append(user)
		elif not user == None and Furry.congastarted == True:
			Furry.congacount += 2
			await ctx.send(f'{ctx.author.mention} joined, bringing {user.mention} with them \nThere are {Furry.congacount} furs in the conga.' + (f'{Main.bot.get_emoji(950891145339220048)}'*Furry.congacount))
			Furry.fursinconga.append(ctx.author)
			Furry.fursinconga.append(user)

	@commands.command(name='leaveconga', help='leave the conga line')
	async def leaveconga(self, ctx):
		if not ctx.author in Furry.fursinconga:
			return await ctx.send('You are not in the conga')
		if Furry.congacount > 1:
			if Furry.fursinconga[len(Furry.fursinconga)-1] == ctx.author:
				await ctx.send('You leave the end of the conga')
				Furry.fursinconga.pop(len(Furry.fursinconga)-1)
			else:
				await ctx.send('You leave the conga, the person behind you fills the gap.')
				Furry.fursinconga.pop(Furry.fursinconga.index(ctx.author))
		else:
			await ctx.send('You are the last person, You get up and leave')
			Furry.fursinconga.pop(0)
			Furry.congastarted = False
		Furry.congacount -= 1
		await ctx.send(f'There are {Furry.congacount} furs in the conga.' + (f'{Main.bot.get_emoji(950891145339220048)}'*Furry.congacount))

#---NSFW furry commands class ;)---
#houses all the fun furry commands
class NSFWFurryCommands(commands.Cog, name="NSFW Furry Commands", description="The fun commands for furries ;)"):

	async def nsfwcheck(channel):
		if isinstance(channel, discord.channel.DMChannel):
			return True
		elif channel.is_nsfw():
			return True
		else:
			return False

	#a yiff command for searching e621
	#gets a big list of posts that have tag(s) that were searched for from e621
	#if the list is empty is says so
	#but if its not, it selects a random post and sends it
	#makes sure the post isn't a webm, because I couldn't get it working with webm video
	@commands.command(name='yiff', help='Searches e621.net based off a search term')
	async def yiff(self, ctx, *, search='gay'):
		if await NSFWFurryCommands.nsfwcheck(ctx.channel):
			tosearch=search
			keywords, searchwords = GoogleSearch.key_words_search_words(GoogleSearch, user_message=tosearch)
			print(f'got keywords: {keywords}\n from {search}')
			cs = aiohttp.ClientSession()
			print('got client session')
			headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
			r = await cs.get(f'https://e621.net/posts.json?tags={keywords}+-watersports+-scat+-vore+-gore+-loli+-shota+-urine+-peeing+-bdsm+-bondage+-rating:s+order:score+-type:webm&limit=50', headers=headers)
			print('got e6 link')
			print(r.status)
			if r.status == 200:
				data = await r.json(content_type=None)
				print(len(data['posts']))
				if len(data['posts']) == 0:
					return await ctx.send('No results!')
				post = random.choice(data['posts'])
				file = post['file']
				embed = discord.Embed(title=f"e621: {search}, id: {post['id']}", color = ctx.author.color)
				if file['url'] == None:
					embed.set_image(url=post['sources'][len(post['sources'])-1])
				else:
					embed.set_image(url=file['url'])
				await ctx.send(embed=embed)
				print(file['url'])
			else:
				await ctx.send(f'Problem status: {r.status}')
			await cs.close()
		else:
			await ctx.send('Command must be used in nsfw channel!!!')

	@commands.command(name='post', help='tries to get the post with the given id')
	async def post(self, ctx, postid: int):
		if await NSFWFurryCommands.nsfwcheck(ctx.channel):
			cs = aiohttp.ClientSession()
			print('got client session')
			headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
			r = await cs.get(f'https://e621.net/posts.json?tags=id:{postid}', headers=headers)
			print('got e6 link')
			print(r.status)
			if r.status == 200:
				data = await r.json(content_type=None)
				print(len(data['posts']))
				if len(data['posts']) == 0:
					return await ctx.send('No results!')
				post = data['posts'][0]
				print(post)
				file = post['file']
				print(file)
				embed = discord.Embed(title=f"e621: post {postid}", color = ctx.author.color)
				print(embed)
				if file['url'] == None:
					embed.set_image(url=post['sources'][len(post['sources'])-1])
				else:
					embed.set_image(url=file['url'])
				await ctx.send(embed=embed)
				print(file['url'])
			else:
				await ctx.send(f'Problem status: {r.status}')
			await cs.close()
		else:
			await ctx.send('Command must be used in nsfw channel!!!')
			
	@commands.command(name='animpost', help='tries to get the post with the given id. for animations bc post only works for images/gif')
	async def post(self, ctx, postid: int):
		if await NSFWFurryCommands.nsfwcheck(ctx.channel):
			cs = aiohttp.ClientSession()
			print('got client session')
			headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
			r = await cs.get(f'https://e621.net/posts.json?tags=id:{postid}', headers=headers)
			print('got e6 link')
			print(r.status)
			if r.status == 200:
				data = await r.json(content_type=None)
				print(len(data['posts']))
				if len(data['posts']) == 0:
					return await ctx.send('No results!')
				post = data['posts'][0]
				print(post)
				file = post['sample']['alternates']['original']['urls'][1]
				embed = discord.Embed(title=f"e621: {search}, id: {post['id']}", color = ctx.author.color)
				await ctx.send(embed=embed)
				await ctx.send(file)
			else:
				await ctx.send(f'Problem status: {r.status}')
			await cs.close()
		else:
			await ctx.send('Command must be used in nsfw channel!!!')

	@commands.command(name='e6anim', help='searches e621 for videos based off a search term')
	async def e6anim(self, ctx, *, search='gay'):
		if await NSFWFurryCommands.nsfwcheck(ctx.channel):
			tosearch=search
			keywords, searchwords = GoogleSearch.key_words_search_words(GoogleSearch, user_message=tosearch)
			print(f'got keywords: {keywords}\n from {search}')
			cs = aiohttp.ClientSession()
			print('got client session')
			headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
			r = await cs.get(f'https://e621.net/posts.json?tags={keywords}+-watersports+-scat+-vore+-gore+-loli+-shota+-urine+-peeing+-bdsm+-bondage+-rating:s+order:score+type:webm&limit=50', headers=headers)
			print('got e6 link')
			print(r.status)
			if r.status == 200:
				data = await r.json(content_type=None)
				print(len(data['posts']))
				if len(data['posts']) == 0:
					return await ctx.send('No results!')
				post = random.choice(data['posts'])
				file = post['sample']['alternates']['original']['urls'][1]
				embed = discord.Embed(title=f"e621: {search}, id: {post['id']}", color = ctx.author.color)
				await ctx.send(embed=embed)
				await ctx.send(file)
			else:
				await ctx.send(f'Problem status: {r.status}')
			await cs.close()
		else:
			await ctx.send('Command must be used in nsfw channel!!!')

	@commands.command(name='randyiff', help='Searches e621.net based off a search term, sorts randomly')
	async def randyiff(self, ctx, *, search='gay'):
		if await NSFWFurryCommands.nsfwcheck(ctx.channel):
			tosearch=search
			keywords, searchwords = GoogleSearch.key_words_search_words(GoogleSearch, user_message=tosearch)
			print(f'got keywords: {keywords}\n from {search}')
			cs = aiohttp.ClientSession()
			print('got client session')
			headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
			r = await cs.get(f'https://e621.net/posts.json?tags={keywords}+-watersports+-scat+-vore+-gore+-loli+-shota+-urine+-peeing+-bdsm+-bondage+-rating:s+order:random+-type:webm&limit=50', headers=headers)
			print('got e6 link')
			print(r.status)
			if r.status == 200:
				data = await r.json(content_type=None)
				print(len(data['posts']))
				if len(data['posts']) == 0:
					return await ctx.send('No results!')
				post = random.choice(data['posts'])
				file = post['file']
				embed = discord.Embed(title=f"e621: {search}, id: {post['id']}", color = ctx.author.color)
				if file['url'] == None:
					embed.set_image(url=post['sources'][len(post['sources'])-1])
				else:
					embed.set_image(url=file['url'])
				await ctx.send(embed=embed)
				print(file['url'])
			else:
				await ctx.send(f'Problem status: {r.status}')
			await cs.close()
		else:
			await ctx.send('Command must be used in nsfw channel!!!')

	@commands.command(name='rande6anim', help='searches e621 for videos based off a search term, sorts randomly')
	async def rande6anim(self, ctx, *, search='gay'):
		if await NSFWFurryCommands.nsfwcheck(ctx.channel):
			tosearch=search
			keywords, searchwords = GoogleSearch.key_words_search_words(GoogleSearch, user_message=tosearch)
			print(f'got keywords: {keywords}\n from {search}')
			cs = aiohttp.ClientSession()
			print('got client session')
			headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
			r = await cs.get(f'https://e621.net/posts.json?tags={keywords}+-watersports+-scat+-vore+-gore+-loli+-shota+-urine+-peeing+-bdsm+-bondage+-rating:s+order:random+type:webm&limit=50', headers=headers)
			print('got e6 link')
			print(r.status)
			if r.status == 200:
				data = await r.json(content_type=None)
				print(len(data['posts']))
				if len(data['posts']) == 0:
					return await ctx.send('No results!')
				post = random.choice(data['posts'])
				file = post['sample']['alternates']['original']['urls'][1]
				embed = discord.Embed(title=f"e621: {search}, id: {post['id']}", color = ctx.author.color)
				await ctx.send(embed=embed)
				await ctx.send(file)
			else:
				await ctx.send(f'Problem status: {r.status}')
			await cs.close()
		else:
			await ctx.send('Command must be used in nsfw channel!!!')

	@commands.command(name='uwu', help='uwu copypasta lol')
	async def uwu(self, ctx):
		if await NSFWFurryCommands.nsfwcheck(ctx.channel):
			await ctx.send("Rawr x3 nuzzles how are you pounces on you you're so warm o3o notices you have a bulge o: someone's happy (; nuzzles your necky wecky~ murr~ hehehe rubbies your bulgy wolgy you're so big :oooo rubbies more on your bulgy wolgy it doesn't stop growing ·///· kisses you and lickies your necky daddy likies (; nuzzles wuzzles I hope daddy really likes $: wiggles butt and squirms I want to see your big daddy meat~ wiggles butt I have a little itch o3o wags tail can you please get my itch~ puts paws on your chest nyea~ its a seven inch itch rubs your chest can you help me pwease squirms pwetty pwease sad face I need to be punished runs paws down your chest and bites lip like I need to be punished really good~ paws on your bulge as I lick my lips I'm getting thirsty. I can go for some milk unbuttons your pants as my eyes glow you smell so musky :v licks shaft mmmm~ so musky drools all over your cock your daddy meat I like fondles Mr. Fuzzy Balls hehe puts snout on balls and inhales deeply oh god im so hard~ licks balls punish me daddy~ nyea~ squirms more and wiggles butt I love your musky goodness bites lip please punish me licks lips nyea~ suckles on your tip so good licks pre of your cock salty goodness~ eyes role back and goes balls deep mmmm~ moans and suckles")
		else:
			await ctx.send('Command must be used in nsfw channel!!!')

#---NSFW+ furry commands class ;)---
#houses all the fun furry extras commands
class NSFWFurryCommandsplus(commands.Cog, name="NSFW Furry Commands+", description="The fun extras commands for furries ;)"):

	async def nsfwcheck(channel):
		if isinstance(channel, discord.channel.DMChannel):
			return True
		elif channel.is_nsfw():
			return True
		else:
			return False

	#a yiff command for searching e621
	#gets a big list of posts that have tag(s) that were searched for from e621
	#if the list is empty is says so
	#but if its not, it selects a random post and sends it
	#makes sure the post isn't a webm, because I couldn't get it working with webm video
	@commands.command(name='yiff+', help='Searches e621.net based off a search term extra')
	async def yiffplus(self, ctx, *, search='gay'):
		if await NSFWFurryCommands.nsfwcheck(ctx.channel):
			tosearch=search
			keywords, searchwords = GoogleSearch.key_words_search_words(GoogleSearch, user_message=tosearch)
			print(f'got keywords: {keywords}\n from {search}')
			cs = aiohttp.ClientSession()
			print('got client session')
			headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
			r = await cs.get(f'https://e621.net/posts.json?tags={keywords}+-loli+-shota+-rating:s+order:score+-type:webm&limit=50', headers=headers)
			print('got e6 link')
			print(r.status)
			if r.status == 200:
				data = await r.json(content_type=None)
				print(len(data['posts']))
				if len(data['posts']) == 0:
					return await ctx.send('No results!')
				post = random.choice(data['posts'])
				file = post['file']
				embed = discord.Embed(title=f"e621: {search}, id: {post['id']}", color = ctx.author.color)
				if file['url'] == None:
					embed.set_image(url=post['sources'][len(post['sources'])-1])
				else:
					embed.set_image(url=file['url'])
				await ctx.send(embed=embed)
				print(file['url'])
			else:
				await ctx.send(f'Problem status: {r.status}')
			await cs.close()
		else:
			await ctx.send('Command must be used in nsfw channel!!!')

	@commands.command(name='e6anim+', help='searches e621 for videos based off a search term')
	async def e6animplus(self, ctx, *, search='gay'):
		if await NSFWFurryCommands.nsfwcheck(ctx.channel):
			tosearch=search
			keywords, searchwords = GoogleSearch.key_words_search_words(GoogleSearch, user_message=tosearch)
			print(f'got keywords: {keywords}\n from {search}')
			cs = aiohttp.ClientSession()
			print('got client session')
			headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
			r = await cs.get(f'https://e621.net/posts.json?tags={keywords}+-loli+-shota+-rating:s+order:score+type:webm&limit=50', headers=headers)
			print('got e6 link')
			print(r.status)
			if r.status == 200:
				data = await r.json(content_type=None)
				print(len(data['posts']))
				if len(data['posts']) == 0:
					return await ctx.send('No results!')
				post = random.choice(data['posts'])
				file = post['sample']['alternates']['original']['urls'][1]
				embed = discord.Embed(title=f"e621: {search}, id: {post['id']}", color = ctx.author.color)
				await ctx.send(embed=embed)
				await ctx.send(file)
			else:
				await ctx.send(f'Problem status: {r.status}')
			await cs.close()
		else:
			await ctx.send('Command must be used in nsfw channel!!!')

	@commands.command(name='randyiff+', help='Searches e621.net based off a search term, sorts randomly')
	async def randyiffplus(self, ctx, *, search='gay'):
		if await NSFWFurryCommands.nsfwcheck(ctx.channel):
			tosearch=search
			keywords, searchwords = GoogleSearch.key_words_search_words(GoogleSearch, user_message=tosearch)
			print(f'got keywords: {keywords}\n from {search}')
			cs = aiohttp.ClientSession()
			print('got client session')
			headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
			r = await cs.get(f'https://e621.net/posts.json?tags={keywords}+-loli+-shota+-rating:s+order:random+-type:webm&limit=50', headers=headers)
			print('got e6 link')
			print(r.status)
			if r.status == 200:
				data = await r.json(content_type=None)
				print(len(data['posts']))
				if len(data['posts']) == 0:
					return await ctx.send('No results!')
				post = random.choice(data['posts'])
				file = post['file']
				embed = discord.Embed(title=f"e621: {search}, id: {post['id']}", color = ctx.author.color)
				if file['url'] == None:
					embed.set_image(url=post['sources'][len(post['sources'])-1])
				else:
					embed.set_image(url=file['url'])
				await ctx.send(embed=embed)
				print(file['url'])
			else:
				await ctx.send(f'Problem status: {r.status}')
			await cs.close()
		else:
			await ctx.send('Command must be used in nsfw channel!!!')

	@commands.command(name='rande6anim+', help='searches e621 for videos based off a search term, sorts randomly')
	async def rande6anim(self, ctx, *, search='gay'):
		if await NSFWFurryCommands.nsfwcheck(ctx.channel):
			tosearch=search
			keywords, searchwords = GoogleSearch.key_words_search_words(GoogleSearch, user_message=tosearch)
			print(f'got keywords: {keywords}\n from {search}')
			cs = aiohttp.ClientSession()
			print('got client session')
			headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
			r = await cs.get(f'https://e621.net/posts.json?tags={keywords}+-loli+-shota+-rating:s+order:random+type:webm&limit=50', headers=headers)
			print('got e6 link')
			print(r.status)
			if r.status == 200:
				data = await r.json(content_type=None)
				print(len(data['posts']))
				if len(data['posts']) == 0:
					return await ctx.send('No results!')
				post = random.choice(data['posts'])
				file = post['sample']['alternates']['original']['urls'][1]
				embed = discord.Embed(title=f"e621: {search}, id: {post['id']}", color = ctx.author.color)
				await ctx.send(embed=embed)
				await ctx.send(file)
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
	bot.add_cog(NSFWFurryCommandsplus(bot))
