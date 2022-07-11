#Unifox Discord bot
#generalCommands.py

#---imports---#
#import discord stuff, the main file, and bot settings
import discord
import discord.ext
from main import Main
from cogs.botSettings import BotSettings
from discord.ext import commands

#general commands class
#houses the commands that can be used by anyone allowed to message
class GeneralCommands(commands.Cog, name='General Commands', description='Commands for anyone to use any time'):

	#to check the server details
	#creates a fancy message showing said details
	@commands.command(name='whereami', help='tells where the bot is')
	async def whereami(self, ctx):
		owner = str(ctx.guild.owner)
		guildID = str(ctx.guild.id)
		memberCount = str(ctx.guild.member_count)
		icon = str(ctx.guild.icon_url)

		embed = discord.Embed(
			title = ctx.guild.name + " Server Info",
			color = discord.Color.blue()
		)

		embed.set_thumbnail(url=icon)
		embed.add_field(name="Owner", value=owner, inline=True)
		embed.add_field(name="Server ID", value=guildID, inline=True)
		embed.add_field(name="Member Count", value=memberCount, inline=True)

		await ctx.send(embed=embed)
		
	#used to delete your last message
	@commands.command(name='del', help='deletes the command message and the last message before that from the person who sent the command')
	async def delete(self, ctx):
		messageFound = False
		async for message in ctx.channel.history(limit=1):
			await message.delete()
		async for message in ctx.channel.history(limit=25):
			if not messageFound:
				if message.author == ctx.author:
					await message.delete()
					messageFound = True

	#show how many warnings someone has
	@commands.command(name='showWarns', help='shows the number of warnings for a given user')
	async def showWarns(self, ctx, *, member: discord.Member):
		try:
			await ctx.send(BotSettings.warnlist[member])
		except:
			await ctx.send('member has no warnings')

	#show the details of the person who sent the command (also checks if i sent it)
	@commands.command(name='whoami', help='tells who you are ig. may also be given another user')
	async def whoami(self, ctx, *, member: discord.Member = None):
		if member != None:
			user = member
		elif member == None:
			user = ctx.author
		embed = discord.Embed(title=f"{user} Member Info", color=user.color)
		embed.set_thumbnail(url=user.avatar)
		if int(user.id) == Main.bot.author_id:
			await ctx.send("Why hello my creator!")
		await ctx.send(user)

#the setup function
def setup(bot):
	bot.add_cog(GeneralCommands(bot))
