#Unifox Discord bot
#musicCommands.py

#---imports---#
#discord for basic function
#nacl and ffmpeg for audio playing
#and others for other functionality
import discord
import nacl
import ffmpeg
import time
import os
from main import Main
from cogs.botSettings import BotSettings
from discord.ext import commands

#music commands class
#houses the commands for playing and controlling audio
class MusicCommands(commands.Cog, name="Music Commands", description='Commands for controlling the bot in VC'):

	global voice

	#to get the bot to join your voice channel for playing
	@commands.command(name='join', help='connects bot to your current vc')
	async def connect(self, ctx):
		await ctx.send("connecting...")
		connected = ctx.author.voice
		if not connected:
			await ctx.send("You need to be connected in a voice channel to use this command!")
			return
		MusicCommands.voice = await connected.channel.connect(timeout=600.0, reconnect=False)
		await ctx.send(f'connected to {MusicCommands.voice.channel}')

	#to get the bot to leave the voice channel
	@commands.command(name='leave', help='disconnects bot from all vcs', pass_context=True)
	async def leave(self, ctx):
		for x in Main.bot.voice_clients:
			await x.disconnect(force=True)
		await ctx.send('left vcs')

	#a list of video urls to play, and who requested each one
	queue = list()
	queueRequests = list()
	#and command to add to them
	@commands.command(name='add', help='This command adds a song to the queue')
	async def add(self, ctx, *, url):
		urls = url.split()
		for x in urls:
			MusicCommands.queue.append(x)
			MusicCommands.queueRequests.append(ctx.author.mention)
			await ctx.send(f'`{x}` added to queue! requested by {ctx.author.mention}')

	paused = False

	#a function used to wait for the bot to no longer be playing
	#sends a message to timeout channel to keep the bot from crashing due to timeout
	async def isPlaying(ctx):
		pingchan = 0
		try:
			pingchan = BotSettings.timeoutChanindex
		except:
			await ctx.send('something wrong with ping channel')
			print('pingchan not set')
		channel = Main.bot.get_channel(pingchan)
		while True:
			if ctx.voice_client.is_playing() or MusicCommands.paused:
				await channel.send('still playing', delete_after=5)
				time.sleep(5)
				continue
			elif not ctx.voice_client.is_playing():
				print('not playing')
				return
			else:
				print('wha')

	gettingAudio = False

	#a function to wait for the bot to start playing something
	#called after the queue is empty
	async def waiting(ctx):
		messagenum = 0
		pingchan = 0
		try:
			pingchan = BotSettings.timeoutChanindex
		except:
			await ctx.send('something wrong with ping channel')
			print('pingchan not set')
		channel = Main.bot.get_channel(pingchan)
		while True:
			if not ctx.voice_client.is_playing() and not MusicCommands.gettingAudio:
				await channel.send('Waiting to start playing again', delete_after=5)
				messagenum += 1
				time.sleep(5)
				if messagenum == 12:
					messagenum = 0
					await ctx.voice_client.disconnect(force=True)
					await ctx.send("I wasn't playing anything, so i left")
					return
				continue
			elif ctx.voice_client.is_playing() or MusicCommands.gettingAudio:
				print('playing again')
				return
			else:
				print('wha')

	#used to display an error to the console upon an error playing audio
	def playError(error=None):
		if error == None:
			print('playing fine')
		else:
			print(f'AH SHIT {error}')

	#the main play command. this is used to start plaing audio on discord
	@commands.command(name='play', help='To play the queue')
	async def play(self, ctx):
		try:
			if len(MusicCommands.queue) == 0:
				await ctx.send('nothing in the queue!')
				return
			#get the voice channel the bot is in
			voice_channel = ctx.voice_client

			#go through the songs in the queue playing one at a time
			while len(MusicCommands.queue) > 0:
				await ctx.send('getting audio', delete_after=10)
				MusicCommands.gettingAudio = True
				async with ctx.typing():
					#get the audio source to start playing, and the filename to delete the file when done (to keep storag low)
					player, filename = await Main.YTDLSource.from_url(url=MusicCommands.queue[0], loop=Main.bot.loop)
					#if its playing, stop. this is used for the 'next' command to skip the current song
					if voice_channel.is_playing():
						voice_channel.stop()
					#start playing the audio
					voice_channel.play(player, after=MusicCommands.playError())
					#create a fancy message to tell that it has started playing, and send it
					embed = discord.Embed(title="Now playing", colour=discord.Colour.random(), description=f"[{player.title}]({MusicCommands.queue[0]}) \n[requested by{MusicCommands.queueRequests[0]}]")
					await ctx.send(embed=embed)
					MusicCommands.gettingAudio = False
				#use the isPlaying function to wait until playing is done
				await MusicCommands.isPlaying(ctx)
				#once playing is done, delete the file, and remove the song from queue
				os.remove(filename)
				if len(MusicCommands.queue) != 0:
					MusicCommands.queue.pop(0)
					MusicCommands.queueRequests.pop(0)
				else:
					print('empty queue')
			#once the queue is done, say that its done, clear the queue, and wait to start playing again
			await ctx.send('Finished playing queue')
			voice_channel.stop()

			await MusicCommands.waiting(ctx)
			
		#call the error function if something happens
		except Exception as e:
			await Main.on_command_error(ctx, e)

	#used to play a song right away, not from a queue
	@commands.command(name='playnow', help='to play a song from url directly')
	async def playnow(self, ctx, *, url):
		async with ctx.typing():
			player, filename = await Main.YTDLSource.from_url(url, loop=Main.bot.loop)
			if ctx.voice_client.is_playing():
				ctx.voice_client.stop()
			ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

		await ctx.send('Now playing: {}'.format(player.title))

		await MusicCommands.isPlaying(ctx)
		await ctx.send('done playing')
		os.remove(filename)

	#used to pause what is playing
	@commands.command(name='pause', help='This command pauses the song')
	async def pause(self, ctx):
		voiceToPause = ctx.guild.voice_client
		print(voiceToPause)
		if voiceToPause.is_playing():
			MusicCommands.paused = True
			voiceToPause.pause()
		else:
			await ctx.send("The bot is not playing anything at the moment.")

	#and resume playing
	@commands.command(name='resume', help='Resumes the song')
	async def resume(self, ctx):
		voiceToResume = ctx.guild.voice_client
		if voiceToResume.is_paused():
			voiceToResume.resume()
			MusicCommands.paused = False
		else:
			await ctx.send("The bot was not playing anything before this. Use play command")

	#as well as full stop playing
	@commands.command(name='stop', help='Stops the song')
	async def stop(self, ctx):
		voiceToStop = ctx.guild.voice_client
		x = 0
		while x != len(MusicCommands.queue):
			MusicCommands.queue.pop(x)
			MusicCommands.queueRequests.pop(x)
		if voiceToStop.is_playing():
			voiceToStop.stop()
			await ctx.send("music stopped and queue emptied")
		else:
			await ctx.send("The bot is not playing anything at the moment.")
	
	#used to view whats in the queue
	@commands.command(name='queue', help='shows what is in the queue of songs')
	async def inQueue(self, ctx):
		await ctx.send(MusicCommands.queue)

	#used to skip to the next song, if playing from queue
	@commands.command(name='next', help='skips to the next song')
	async def next(self, ctx):
		try:
			print(MusicCommands.voice)
			print('stopping')
			if MusicCommands.voice.is_playing():
				MusicCommands.voice.stop()
				print('stopped')
			else:
				await ctx.send('Not playing anything')
				print("wasn't playing")
		except Exception as e:
			await ctx.send(f"not connected or {e}")
		
	#used to turn the volume up for the next song
	@commands.command(name='volup', help='Adjusts music volume up (only applies to next songs, not current)')
	async def volup(self, ctx):
		if BotSettings.setVolume == 1.0:
			return await ctx.send('Already full volume')
		BotSettings.setMusicVol(BotSettings.setVolume + 0.2)
		await ctx.send('volume up')
		BotSettings.quietSave()

	#and turn it down
	@commands.command(name='voldown', help='Adjusts music volume down (only applies to next songs, not current)')
	async def voldown(self, ctx):
		if BotSettings.setVolume == 0.0:
			return await ctx.send('Already muted')
		BotSettings.setMusicVol(BotSettings.setVolume - 0.2)
		await ctx.send('volume down')
		BotSettings.quietSave()

	#set it to full
	@commands.command(name='volfull', help='Sets music to full volume (only applies to next songs, not current)')
	async def volfull(self, ctx):
		BotSettings.setMusicVol(1.0)
		await ctx.send('Volume full')
		BotSettings.quietSave()

	#and mute
	@commands.command(name='volmute', help='Mutes music (only applies to next songs, not current)')
	async def volmute(self, ctx):
		BotSettings.setMusicVol(0.0)
		await ctx.send('Muted')
		BotSettings.quietSave()

	#sets the timeout channel it will send messages to
	@commands.command(name='timeoutChannel', help='sets the channel the bot uses to prevent timouts BY ID')
	async def timeoutChannel(self, ctx, *, channelid: int):
		BotSettings.setTimeoutChan(channelid)
		BotSettings.quietSave()
		await ctx.send(f'set timeout channel to {Main.bot.get_channel(BotSettings.timeoutChanindex)}')

	#and check what channel is set
	@commands.command(name='checktimeout', help='used to check the set tieout channel')
	async def checktimeout(self, ctx):
		await ctx.send(int(BotSettings.timeoutChanindex))
		await ctx.send(Main.bot.get_channel(int(BotSettings.timeoutChanindex)))

#the setup function
def setup(bot):
	bot.add_cog(MusicCommands(bot))