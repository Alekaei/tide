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