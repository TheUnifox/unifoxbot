 #Unifox Discord Bot
#main.py

#---imports---#
#this is the imports section, even if it says something is unused, it is used while running.
#os is for environment variables like the bot token. nacl and ffmpeg are for playing audio, and youtube-dl is for getting the audio
#time is used once to wait a sec to not cause issues. all discord is for the bot to have basic function. botSettings holds... the bot settings
import os
import asyncio
import nacl
import ffmpeg
import time
import youtube_dl
import aiohttp
import discord
import discord.ext
from cogs.botSettings import BotSettings
from keep_alive import keep_alive
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure, check

#---main class---#
#this houses most of this files stuff
class Main():

	#this is to get the discord bot, and set some stuff for it
	bot = commands.Bot(
    command_prefix = BotSettings.prefix,  # Change to desired prefix
    case_insensitive=True,  # Commands aren't case-sensitive
		strip_after_prefix=True
	)

	bot.ses = aiohttp.ClientSession()#get a client session for sumn idk

	#this is to tell discord who made it
	bot.author_id = 448846699692032006  # Change to your discord id!!!

	#this is used for loading all the functions later
	extensions = [
		'cogs.cog_example',
		'cogs.admin',
		'cogs.music',
		'cogs.general',
		'cogs.search',
		'cogs.furry'
	]

	#---events---#
	#these get triggered by discord for different things
	#on ready is when the bot starts and is ready
	@bot.event
	async def on_ready():  # When the bot is ready
		print("I'm in")
		print(Main.bot.user)  # Prints the bot's username and identifier
		for guild in Main.bot.guilds: #goes through all the servers the bot is in
			for channel in guild.text_channels: #goes through all the channels in each server
				if str(channel) == "bot-setup-for-the-mods" or str(channel) == "bot-setup" or str(channel) == "testagain": #checks if the channel is one of these
					await channel.send("I'M AWAKE") #and sends a message saying the bot is up
			print(f'active in {guild.name}\n member count: {guild.member_count}') #and finally says its active in a server, and how many people are in it

	#this is when someone joins a server
	#it creates a chat with person to welcome them
	@bot.event
	async def on_member_join(member):
		await member.create_dm()
		await member.dm_channel.send(f"Why hello there {member.name}! Welcome!")

	#this is when something bad happens in a command
	#it lets me know what went wrong, and possibly keeps the bot from crashing
	@bot.event
	async def on_command_error(ctx, error):
		print(error)
		if isinstance(error, commands.CommandNotFound):
			return
		elif isinstance(error, commands.MissingAnyRole):
			embed = discord.Embed(title="Error", colour=discord.Colour.red(), description="No permission to use that...")
		else:
			embed = discord.Embed(title="Error", colour=discord.Colour.red(), description=f"oops! {error}")
		
		await ctx.send(embed=embed, delete_after=5)
		await ctx.message.delete(delay=5)

	#this is when someone becomes online or offline, not sure it works
	@bot.event
	async def on_user_update(ctx, user, status, activities):
	    await ctx.send(f"{user} is now {status}")
	    if activities != None:
	        await ctx.send(f"and activity is now {activities}")


	#---youtube-dl---#
	#this section is for youtube-dl, that gets audio or video for playing
	youtube_dl.utils.bug_reports_message = lambda: ''

	#these are the required options for youtube-dl formatting
	ytdl_format_options = {
	    'format': 'bestaudio/best',
	    'restrictfilenames': True,
	    'noplaylist': True,
	    'nocheckcertificate': True,
	    'ignoreerrors': False,
	    'logtostderr': True,
	    'quiet': False,
	    'no_warnings': False,
	    'default_search': 'auto',
	    'source_address':
	    '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
	}

	#these are the options for ffmpeg, that allows us to play the audio
	ffmpeg_options = {'options': '-vn'}
	ffmpeg_beforeOptions = {"before_options": "-timelimit 9999 "}

	#we set the youtube-dl class to a variable for easier access ig
	ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

	#the youtube-dl source class
	#this is used to actually use youtube-dl to get and process the audio
	class YTDLSource(discord.PCMVolumeTransformer):
		def __init__(self, source, *, data, volume=0.5):
			super().__init__(source, volume)
			self.data = data
			self.title = data.get('title')
			self.url = ""

		#this gets the video from a youtube (or other) link
		@classmethod
		async def from_url(cls, url, *, loop=None, stream=False):
			loop = loop or asyncio.get_event_loop()
			data = await loop.run_in_executor(
				None, lambda: Main.ytdl.extract_info(url, download=not stream))
			if 'entries' in data:
				# take first item from a playlist
				data = data['entries'][0]
			filename = Main.ytdl.prepare_filename(data)
			return cls(discord.FFmpegPCMAudio(source=filename, pipe=False, before_options=Main.ffmpeg_beforeOptions, options=Main.ffmpeg_options), data=data, volume=BotSettings.setVolume), filename

	#---final main section---#
	#this command should always work if the bot is up
	@bot.command(name="ping2", help='generic ping command, should always work')
	async def ping2(ctx):
		print('pong2')
		await ctx.send("pong2")

	#this event is triggered every time a message is sent
	#it checks to see if the channel should be ignored
	#then if the message was sent by this bot
	#then if any word in the message is in a blacklist of bad words
	#now check if its a help command and deal with it here
	@bot.event
	async def on_message(message):
		if message.channel.name.lower() in BotSettings.ignoreChannels:
			return
		if message.author == Main.bot.user:
			return
		for word in message.content.split():
			if word in BotSettings.badwords:
				time.sleep(0.5)
				await message.delete() #if so, delete the message
		if message.content.startswith(f'{BotSettings.prefix}help'):
			destination = message.channel
			category = message.content
			commno = 0
			if category == f'{BotSettings.prefix}help':
				embed = discord.Embed(title='Help!', description='These are the categories.', colour=discord.Colour.red())
				print(Main.bot.cogs)
				for cog in Main.bot.cogs:
					print(cog)
					embed.add_field(name=cog, value=Main.bot.cogs[cog].description)
				embed.set_footer(text='type (prefix)help (category) for info on a category \neg. h!help Furry Commands')
			else:
				if len(Main.bot.cogs[category[5+len(BotSettings.prefix):]].get_commands()) > 25:
					commno = 0
					embed = discord.Embed(title='Help!', description=f'Commands in {category}', colour=discord.Colour.red())
					embed2 = discord.Embed(title='Help! (cont.)', description=f'Commands in {category}', colour=discord.Colour.red())
					for command in Main.bot.cogs[category[5+len(BotSettings.prefix):]].get_commands():
						print(command)
						commno += 1
						if commno > 25:
							embed2.add_field(name=command, value=command.help)
						else:
							embed.add_field(name=command, value=command.help)
				else:
					embed = discord.Embed(title='Help!', description=f'Commands in {category}', colour=discord.Colour.red())
					for command in Main.bot.cogs[category[5+len(BotSettings.prefix):]].get_commands():
						print(command)
						embed.add_field(name=command, value=command.help)
			print(embed)
			if commno > 25:
				await destination.send(embed=embed)
				return await destination.send(embed=embed2)
			else:
				return await destination.send(embed=embed)
		await Main.bot.process_commands(message)

	#this is used to load all the command modules from before
	def loadCogs():
		print('loading cogs')
		for extension in Main.extensions:
			print(extension)
			Main.bot.load_extension(extension)  # Loades every extension.

#----the startup section----#
#first start a websocket to be pinged to keep the bot up
#get the bot token to log in with
#use the command loading function to load commands
#and finally start the bot!
token = os.environ.get("DISCORD_BOT_SECRET")
Main.loadCogs()
Main.bot.run(token)  # Starts the bot
