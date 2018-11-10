import os
from datetime import datetime

class LogLevel:
	DEBUG = 0
	INFORMATION = 1
	WARNING = 2
	ERROR = 3
	NONE = 4

class Logger:
	def __init__(self, location='./logs/log.txt', logLevel=LogLevel.INFORMATION):
		self.file = os.path.abspath(location)
		self.dir = os.path.dirname(self.file)
		self.logLevel = logLevel

		if os.path.exists(self.file):
			os.rename(self.file, os.path.join(self.dir, f'log_{int(datetime.now().timestamp())}.txt'))
		if not os.path.exists(self.dir):
			os.makedirs(self.dir)
	
	def __write__(self, message):
		with open(self.file, 'a' if os.path.exists(self.file) else 'w') as wFile:
			wFile.write(message + '\n')

	def logError(self, message):
		if self.logLevel > LogLevel.ERROR:
			return
		self.__write__(f'[ERROR] [{datetime.now()}] {message}')

	def logWarning(self, message):
		if self.logLevel > LogLevel.WARNING:
			return
		self.__write__(f'[WARNING] [{datetime.now()}] {message}')

	def logInformation(self, message):
		if self.logLevel > LogLevel.INFORMATION:
			return
		self.__write__(f'[INFO] [{datetime.now()}] {message}')
	
	def getLevels(self):
		levels = {}
		sclass = Logger.__class__
		for var in sclass.__dict__:
			if not callable(getattr(sclass, var)):
				levels[var] = A.__dict__[var] 

logger = Logger()