import curses
import tide.terminal as terminal
from tide.classes.View import View
import tide.writeutil as writeutil


class TerminalView(View):
	def __init__(self, window, location):
		View.__init__(self, window)
		self.location = location
		self.buffer = [None] * 300
		self.input = ''

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

		to[self.y] = writeutil.write(self.x, to[self.y], f'┌─ Terminal {"─" * (self.width - 13)}┐')
		for y in range(1, self.height - 3):
			to[self.y + y] = writeutil.write(self.x, to[self.y + y], f'│{" " * (self.width - 2)}│')
		to[self.y + self.height - 3] = writeutil.write(self.x, to[self.y + self.height - 3], f'├{"─" * (self.width - 2)}┤')
		to[self.y + self.height - 2] = writeutil.write(self.x, to[self.y + self.height - 2], f'│ \033[31m{self.location}\033[0m >{" " * (self.width - 5 - len(self.location))}│')
		to[self.y + self.height - 1] = writeutil.write(self.x, to[self.y + self.height - 1], f'└{"─" * (self.width - 2)}┘')

		return to
		"""
		y, x = self.window.getpayyx()
		height, width = self.window.getmaxyx()

		self.window.addstr(y, x, f'┌─ Terminal {"─" * (width - 13)}┐')
		for line in range(1, height - 1):
			self.window.addstr(y + line, x, f'│{" " * (width - 2)}│')
		self.window.addstr(y + height - 1, x, f'└{"─" * (width - 2)}┘')
