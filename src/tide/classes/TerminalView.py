import curses
from tide.classes.View import View


class TerminalView(View):
	def __init__(self, window, location):
		View.__init__(self, window)
		self.location = location
		self.buffer = [None] * 300
		self.input = ''

		self.layers = [(0, -3, '[x]')]

	def write(self, message, foreground='30', background='40'):
		if None in self.buffer:
			self.buffer[self.buffer.index(
				None)] = f'\033[{foreground};{background}m{message}\033[0m'

	def render(self):
		""" Example View
			┌─ Terminal ─────────────────────────┐
			│                                    │
			│                                    │
			│                                    │
			├────────────────────────────────────┤
			│ ~ >                                │
			└────────────────────────────────────┘
		"""
		height, width = self.window.getmaxyx()

		self.window.insstr(0, 0, f'┌─ Terminal {"─" * (width - 13)}┐')
		for line in range(1, height - 1):
			self.window.insstr(line, 0, f'│{" " * (width - 2)}│')
		self.window.insstr(height - 1, 0, f'└{"─" * (width - 2)}┘')

		#for layer in self.layers:
		#	self.window.addstr(layer[0] if layer[0] >= 0 else height + layer[0], layer[1] if layer[1] >= 0 else width + layer[1], layer[2])

		self.window.noutrefresh()