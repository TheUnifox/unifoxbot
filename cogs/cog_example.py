#Unifox Discord bot
#cog_examples.py
#a default file thats made when creating a repl from the bot template

#import discord commands to make stuff work
import discord
from discord.ext import commands

#develpoer commands class
#houses commands to be used by me for development
class DevCommands(commands.Cog, name='Developer Commands', description='Strictly only commands for the bot developer'):
	'''These are the developer commands'''

	#an init, idk
	def __init__(self, bot):
		self.bot = bot

	#a function to check if the person using these commands is me ig
	async def cog_check(self, ctx):  
		'''
		The default check for this cog whenever a command is used. Returns True if the command is allowed.
		'''
		return ctx.author.id == self.bot.author_id

	#a reload command to reload all or a certain chunk of commands
	@commands.command(  # Decorator to declare where a command is.
		name='reload',  # Name of the command, defaults to function name.
		aliases=['rl']  # Aliases for the command.
	)  
	async def reload(self, ctx, cog):
		'''
		Reloads a cog.
		'''
		extensions = self.bot.extensions  # A list of the bot's cogs/extensions.
		if cog == 'all':  # Lets you reload all cogs at once
			for extension in extensions:
				self.bot.unload_extension(cog)
				self.bot.load_extension(cog)
			await ctx.send('Done')
		if cog in extensions:
			self.bot.unload_extension(cog)  # Unloads the cog
			self.bot.load_extension(cog)  # Loads the cog
			await ctx.send('Done')  # Sends a message where content='Done'
		else:
			await ctx.send('Unknown Cog')  # If the cog isn't found/loaded.
	
	#used to unload a chunk of commands if needed ig
	@commands.command(name="unload", aliases=['ul']) 
	async def unload(self, ctx, cog):
		'''
		Unload a cog.
		'''
		extensions = self.bot.extensions
		if cog not in extensions:
			await ctx.send("Cog is not loaded!")
			return
		self.bot.unload_extension(cog)
		await ctx.send(f"`{cog}` has successfully been unloaded.")
	
	#used to load a cog
	@commands.command(name="load")
	async def load(self, ctx, cog):
		'''
		Loads a cog.
		'''
		try:

			self.bot.load_extension(cog)
			await ctx.send(f"`{cog}` has successfully been loaded.")

		except commands.errors.ExtensionNotFound:
			await ctx.send(f"`{cog}` does not exist!")

	#to list al the cogs enabled
	@commands.command(name="listcogs", aliases=['lc'])
	async def listcogs(self, ctx):
		'''
		Returns a list of all enabled commands.
		'''
		base_string = "```css\n"  # Gives some styling to the list (on pc side)
		base_string += "\n".join([str(cog) for cog in self.bot.extensions])
		base_string += "\n```"
		await ctx.send(base_string)

	@commands.command(name='off', help='turns the bot off, bot needs to be restarted to turn on again')
	async def off(self, ctx):
		await ctx.send('BYE!')
		await self.bot.logout()

	@commands.command(name='restart', help='restarts the bot')
	async def restart(self, ctx):
		await ctx.send('restarting...')
		await self.bot.close()
		await self.bot.start()

	@commands.command(name='timeouttest', aliases=['tt'], help='testing command timeout, current = 5 seconds')
	async def timeouttest(self, ctx):
		def check(msg):
			return msg.author == ctx.author and msg.channel == ctx.channel
		isdone = False
		usermessage = None
		while not isdone:
			await ctx.send(usermessage)
			usermessage = (await Main.bot.wait_for(timeout = 5, 'message', check=check)).content

	@timeouttest.error
	async def on_error(self, ctx, error):
		if isinstance(error, commands.CommandInvokeError):
			await ctx.send('timeout!')

#the setup to add these commands to the bot
def setup(bot):
	print('loading cog example')
	bot.add_cog(DevCommands(bot))
