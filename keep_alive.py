#Unifox Disocrd bot
#keep_alive.py
#this file is used to keep the bot up when the repl is running
#even if no device is currently accessing the repl

#imports to create and run a websocket
from flask import Flask
from threading import Thread
import random
import os

#get a flask to run
app = Flask('Unifox Discord Bot')

class PingCount():
	pingcount = 0
#get a home an print a startup script to it ig
@app.route('/')
def home():
	PingCount.pingcount += 1
	print(f'Pinged, Ping Count: {PingCount.pingcount}')
	return f'Websocket started... \nPing count is: {PingCount.pingcount}'

#actually run the websocket
def run():
  app.run(
		host='0.0.0.0',
		port=os.environ.get('PORT')
	)

#used to get things setup and running to be pinged from a web service to keep it running
def keep_alive():
	'''
	Creates and starts new thread that runs the function run.
	'''
	t = Thread(target=run)
	t.start()
