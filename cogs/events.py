#Unifox Discord Bot
#Events.py

#---Imports Section---
from pydoc import describe
import discord
from discord.ext import commands
from cogs.botSettings import BotSettings
from main import Main
import json
import aiohttp
import asyncio

#---Events Class---
class Events(commands.Cog, name="Events Commands", description="Commands for The Energetic Convention events!"):

    @commands.command(name="events", help="See a list of events to sign up for!")
    async def events(self, ctx):
        cs = aiohttp.ClientSession()
        r = await cs.get("https://tec-site.herokuapp.com/events/api")
        if r.status == 200:
            data = await r.json(content_type='text/plain')
            embed = discord.Embed(title="Events:", color=ctx.author.color)
            eventnum = 0
            for event in data:
                eventnum += 1
                embed.add_field(name=f"event #{eventnum}", value=event)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Problem status: {r.status}')
        await cs.close()

    @commands.command(name="addevent", help="register to be pinged for an event. ex. tec addevent opening")
    async def addevent(self, ctx, *, eventname, extra):
        try:
            BotSettings.eventpings[eventname] += f", @{ctx.author.name}"
            BotSettings.botSettingsToSave['eventpings'][eventname] = BotSettings.eventpings[eventname]
            BotSettings.quietSave()
        except:
            BotSettings.eventpings[eventname] = f"@{ctx.author.name}"
            BotSettings.botSettingsToSave['eventpings'][eventname] = BotSettings.eventpings[eventname]
            BotSettings.quietSave()
        await ctx.send(f"{eventname} has been added to your list @{ctx.author.name}!")

    @commands.command(name="removeEvent", help="remove an event from your list. ex. tec removeevent puttputt")
    async def removeEvent(self, ctx, *, eventname, extra):
        templist = BotSettings.eventpings[eventname]
        templist = templist.replace(f", @{ctx.author.name}", "")
        BotSettings.eventpings[eventname] = templist
        BotSettings.botSettingsToSave['eventpings'][eventname] = BotSettings.eventpings[eventname]
        BotSettings.quietSave()
        await ctx.send(f"{eventname} has been removed from your list @{ctx.author.name}!")

    @commands.command(name="pingfor", help="Used by staff to ping for an event!")
    @commands.has_any_role('admin', 'owner', 'Staff')
    async def pingfor(self, ctx, event, extra):
        chanfound = False
        for server in Main.bot.guilds:
            print(f"searching server {server.name}")
            for channel in server.channels:
                if chanfound:
                    return
                elif not chanfound:
                    print(f"serching channel {channel.name}")
                    if channel.name == 'event-announcements-📣':
                        chanfound = True
                        print("found channel")
                        embed=discord.Embed(title="Time for the next event!", color=discord.Colour.random())
                        embed.add_field(name=f"The next event is {event}!", value=extra)
                        await asyncio.sleep(0.2)
                        await channel.send( BotSettings.eventpings[event], embed=embed)
                        print("message sent")


def setup(bot):
    bot.add_cog(Events(bot))