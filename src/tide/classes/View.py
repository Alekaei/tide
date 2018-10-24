"""

Base class for all views

"""

import tide.terminal as terminal

class View:
	def __init__(self, window):
		self.window = window
		self.inputs = []

	def render(self):
		self.window.noutrefresh()

	def __update_size__(self, x, y, cols, lines):
		self.window.mvwin(y, x)
		self.window.resize(lines, cols)