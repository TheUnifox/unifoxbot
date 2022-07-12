#Unifox Discord bot
#botSettings.py

#import pickle to save and load bot settings
import pickle

#---the bot settings---#
#houses all the variables used throughout the bot
#and some functions for saving variables to file
class BotSettings():
	
	#try to open the settings file to load from
	try:
		file = open('bot.sett', 'rb')
		botSettings = pickle.load(file)      
		file.close()
	except Exception as e:
		#there must not be a settings file ig
		print(f'no settings file, or {e}')
	
	#the bot prefix, the bot looks for this to see if it should do something
	prefix = 'h!'
	try:
		prefix = botSettings['prefix']
		print(prefix)
	except:
		print('default prefix')
	
	#the dictionary of people and how many warns they have
	warnlist = dict()
	try:
		warnlist = botSettings['warnlist']
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
	ignoreChannels = ['spam', 'Spam']
	try:
		ignoreChannels = botSettings['ignoreChannels']
		print(ignoreChannels)
	except:
		print('empty ignore list')
	
	#the blacklist of words that the bot looks for to check if it should delete a message
	badwords = [] #empty by default (may or may not be empty to show in class lol)
	try:
		badwords = botSettings['badwords']
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
		announceChannels = botSettings['announceChannels']
		print(announceChannels)
	except:
		print('default announcement channels')

	clearIgnore = list()
	try:
		clearIgnore = botSettings['clearIgnore']
		print(clearIgnore)
	except:
		print('no clear ignores')

	#a list of tuples to store the settings
	botSettingsToSave = {'prefix' : prefix, 'warnlist' : warnlist, 'musicVol' : str(setVolume), 'warnlimit' : str(warnlimit), 'ignoreChannels' : ignoreChannels, 'badwords' : badwords, 'timeoutChanindex' : str(timeoutChanindex), 'announceChannels' : announceChannels, 'clearIgnore' : clearIgnore}
	
	#---settings saving functions---#
	#to set the prefix
	def setPrefix(newpre):
		BotSettings.prefix = newpre
		BotSettings.botSettingsToSave['prefix'] = newpre
	#to set the volume
	def setMusicVol(newvol):
		BotSettings.setVolume = newvol
		BotSettings.botSettingsToSave['musicVol'] = newvol
	#to set the warn limit
	def setWarnLimit(newlimit):
		BotSettings.warnlimit = newlimit
		BotSettings.botSettingsToSave['warnlimit'] = newlimit
	#to set the timeout channel
	def setTimeoutChan(newindex):
		BotSettings.timeoutChanindex = newindex
		BotSettings.botSettingsToSave['timeoutChanindex'] = newindex

	def addtoignore(new):
		BotSettings.ignoreChannels.append(new)
		BotSettings.botSettingsToSave['ignoreChannels'].append(new)

	def delfromignore(index):
		BotSettings.ignoreChannels.pop(index)
		BotSettings.botSettingsToSave['ignoreChannels'].pop(index)

	def addtobadwords(new):
		BotSettings.badwords.append(new)
		BotSettings.botSettingsToSave['badwords'] = BotSettings.badwords
		BotSettings.quietsave()

	def delfrombadwords(index):
		BotSettings.badwords.pop(index)
		BotSettings.botSettingsToSave['badwords'].pop(index)

	def addtoannounce(new):
		BotSettings.announceChannels.append(new)
		BotSettings.botSettingsToSave['announceChannels'].append(new)

	def delfromannounce(index):
		BotSettings.announceChannels.pop(index)
		BotSettings.botSettingsToSave['announceChannels'].pop(index)

	def addtoclearignore(new):
		BotSettings.clearIgnore.append(new)
		BotSettings.botSettingsToSave['clearIgnore'].append(new)

	def delfromclearignore(index):
		BotSettings.clearIgnore.pop(index)
		BotSettings.botSettingsToSave['clearIgnore'].pop(index)

	#used to save the vaiables to file
	def quietSave():
		settfile = open('bot.sett', 'wb')
		pickle.dump(BotSettings.botSettingsToSave, settfile)
		settfile.close()
