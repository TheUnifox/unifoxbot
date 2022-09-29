#Unifox Discord bot
#botSettings.py

#import pickle to save and load bot settings
import pickle
import os
import requests
import json
import ast

#---the bot settings---#
#houses all the variables used throughout the bot
#and some functions for saving variables to file
class BotSettings():
	
	#try to open the settings file to load from
	try:
		data = {}
		response = requests.get(url='https://api.heroku.com/apps/unifoxbot/config-vars', json=data, headers={'Accept':'application/vnd.heroku+json; version=3', 'Authorization': f'Bearer {os.environ.get("HEROKU_API_KEY")}'})
		botSettings = json.loads(response.content.decode('utf-8')) 
	except Exception as e:
		#there must not be a settings file ig
		print(f'no settings set, or {e}')
	
	#the bot prefix, the bot looks for this to see if it should do something
	prefix = 'tec'
	try:
		prefix = botSettings['prefix']
		print(prefix)
	except:
		print('default prefix')
	
	#the dictionary of people and how many warns they have
	warnlist = dict()
	try:
		warnlist = botSettings['warnlist']
		warnlist1 = list()
		for char in warnlist:
			if char == '=':
				warnlist1.append(':')
			elif char == '>':
				warnlist1.append(' ')
			else:
				warnlist1.append(char)
		warnlist = ''.join(warnlist1)
		warnlistfinal = ast.literal_eval(warnlist)
		warnlist = warnlistfinal
		print(warnlist)
	except:
		print('empty warnlist')
	
	#the volume that is set for playing music
	setVolume = 0.5
	try:
		setVolume = float(botSettings['musicVol'])
		print(setVolume)
	except:
		print('default vol set')
	
	#the channels that should be ignored by the bot
	ignoreChannels = ['spam', 'Spam', 'announcements', 'Announcements']
	try:
		ignoreChannelstodo = botSettings['ignoreChannels']
		ignoreChannelsl = ignoreChannelstodo.split(', ')
		ignoreChannelsfinal = list()
		for chan in ignoreChannelsl:
			chan = chan.strip('[]""')
			ignoreChannelsfinal.append(chan)
		ignoreChannels = ignoreChannelsfinal
		print(ignoreChannels)
	except:
		print('empty ignore list')
	
	#the blacklist of words that the bot looks for to check if it should delete a message
	badwords = [] #empty by default (may or may not be empty to show in class lol)
	try:
		badwordstodo = botSettings['badwords']
		badwordsl = badwordstodo.split(', ')
		badwordsfinal = list()
		for word in badwordsl:
			word = word.strip('[]""')
			badwordsfinal.append(word)
		badwords = badwordsfinal
		print(badwords)
	except:
		print('no bad words')
	
	#the limit number of warnings someone can get before action is taken automatically
	warnlimit = 5
	try:
		warnlimit = int(botSettings['warnlimit'])
		print(warnlimit)
	except:
		print('default warnlimit')
	
	#the index of the timeout channel used to keep the bot from crashing while playing audio
	timeoutChanindex = 0
	try:
		timeoutChanindex = int(botSettings['timeoutChanindex'])
		print(timeoutChanindex)
	except:
		print('default timeout channel index')
	
	#the channels that get pinged upon an announcement
	announceChannels = ['announcements', 'Announcements', 'test']
	try:
		announceChannelstodo = botSettings['announceChannels']
		announceChannelsl = announceChannelstodo.split(', ')
		announceChannelsfinal = list()
		for chan in announceChannelsl:
			chan = chan.strip('[]""')
			announceChannelsfinal.append(chan)
		announceChannels = announceChannelsfinal
		print(announceChannels)
	except:
		print('default announcement channels')

	clearIgnore = list()
	try:
		clearIgnoretodo = botSettings['clearIgnore']
		clearIgnorel = clearIgnoretodo.split(', ')
		clearIgnorefinal = list()
		for ci in clearIgnorel:
			ci = ci.strip('[]""')
			clearIgnorefinal.append(ci)
		clearIgnore = clearIgnorefinal
		print(clearIgnore)
	except:
		print('no clear ignores')

	#a list of tuples to store the settings
	botSettingsToSave = {'prefix' : prefix, 'warnlist' : warnlist, 'musicVol' : str(setVolume), 'warnlimit' : str(warnlimit), 'ignoreChannels' : ignoreChannels, 'badwords' : badwords, 'timeoutChanindex' : str(timeoutChanindex), 'announceChannels' : announceChannels, 'clearIgnore' : clearIgnore}
	
	#---settings saving functions---#
	#to set the prefix
	def setPrefix(newpre):
		BotSettings.prefix = newpre
		BotSettings.botSettingsToSave['prefix'] = BotSettings.prefix
		BotSettings.quietSave()
	#to set the volume
	def setMusicVol(newvol):
		BotSettings.setVolume = newvol
		BotSettings.botSettingsToSave['musicVol'] = BotSettings.setVolume
		BotSettings.quietSave()
	#to set the warn limit
	def setWarnLimit(newlimit):
		BotSettings.warnlimit = newlimit
		BotSettings.botSettingsToSave['warnlimit'] = BotSettings.warnlimit
		BotSettings.quietSave()
	#to set the timeout channel
	def setTimeoutChan(newindex):
		BotSettings.timeoutChanindex = newindex
		BotSettings.botSettingsToSave['timeoutChanindex'] = BotSettings.timeoutChanindex
		BotSettings.quietSave()

	def addtoignore(new):
		BotSettings.ignoreChannels.append(new)
		BotSettings.botSettingsToSave['ignoreChannels'] = BotSettings.ignoreChannels
		BotSettings.quietSave()

	def delfromignore(index):
		BotSettings.ignoreChannels.pop(index)
		BotSettings.botSettingsToSave['ignoreChannels'] = BotSettings.ignoreChannels
		BotSettings.quietSave()

	def addtobadwords(new):
		print(f'adding {new}')
		BotSettings.badwords.append(new)
		print('added new, setting save')
		BotSettings.botSettingsToSave['badwords'] = BotSettings.badwords
		print('save set, saving to file')
		BotSettings.quietSave()
		print('saved')

	def delfrombadwords(index):
		BotSettings.badwords.pop(index)
		BotSettings.botSettingsToSave['badwords'] = BotSettings.badwords
		BotSettings.quietSave()

	def addtoannounce(new):
		BotSettings.announceChannels.append(new)
		BotSettings.botSettingsToSave['announceChannels'] = BotSettings.announceChannels
		BotSettings.quietSave()

	def delfromannounce(index):
		BotSettings.announceChannels.pop(index)
		BotSettings.botSettingsToSave['announceChannels'] = BotSettings.announceChannels
		BotSettings.quietSave()

	def addtoclearignore(new):
		BotSettings.clearIgnore.append(new)
		BotSettings.botSettingsToSave['clearIgnore'] = BotSettings.clearIgnore
		BotSettings.quietSave()

	def delfromclearignore(index):
		BotSettings.clearIgnore.pop(index)
		BotSettings.botSettingsToSave['clearIgnore'] = BotSettings.clearIgnore
		BotSettings.quietSave()

	#used to save the vaiables to file
	def quietSave():
		response = requests.patch(url='https://api.heroku.com/apps/unifoxbot/config-vars', json=BotSettings.botSettingsToSave, headers={'Accept':'application/vnd.heroku+json; version=3', 'Authorization': f'Bearer {os.environ["HEROKU_API_KEY"]}'})
		botSettings = json.loads(response.content.decode('utf-8')) 
		print(response)
		print(botSettings)
