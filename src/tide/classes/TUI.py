import curses

class TUI:
	def __init__(self):
		self.layouts = []
		self.activeWindow = None

	def __render__(self):
		for layout in self.layouts:
			layout.render()
		
		curses.doupdate()