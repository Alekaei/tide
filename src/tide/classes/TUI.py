import curses
from tide.classes.Layout import Layout

class TUI:
	def __init__(self):
		self.layout = Layout()
		self.activeWindow = None

	def __render__(self):
		self.layout.render()
		curses.doupdate()