import curses
from tide.classes.Input import Input

class Button(Input):
	def __init__(self, label, cb):
		self.label = label
		self.cb = cb

	def onClick(self, key):
		if key == 0:
			cb()
	
	def onInput(self, key):
		if key == curses.KEY_ENTER:
			cb()
	