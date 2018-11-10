"""

Base class for all views

"""
import curses
from tide.classes.Logger import logger

class View:
	def __init__(self, window):
		self.window = window
		self.inputs = []
		self.layers = []

	def render(self):
		self.window.noutrefresh()

	def __update_size__(self, x, y, cols, lines):
		cY, cX = self.window.getbegyx()
		if cY != y or cX != x:
			logger.logInformation(f'Moving {self} from `{[cX, cY]}` to `{[x, y]}`')
			try:
				self.window.mvwin(y, x)
			except:
				pass
		self.window.resize(lines, cols)