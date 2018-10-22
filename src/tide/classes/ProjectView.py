import tide.terminal as terminal
import os
from tide.classes.View import View
import tide.writeutil as writeutil

class ProjectView(View):
	def __init__(self, window, location):
		View.__init__(self, window)
		self.location = location
		self.fileCount = 0

	def render(self, to):
		""" Example View
			┌────────────────┐
			│    Project     │
			│ folder       ▼ │
			│   file         │
			│   file.py      │
			│ folder2        │
			│   example.js   │
			│                │
			│                │
			│                │
			├────────────────┤
			│ 32 files       │
			└────────────────┘
		projectName = os.path.basename(self.location)
		to[self.y] = writeutil.write(self.x, to[self.y], f'┌{"─" * (self.width - 2)}┐')
		to[self.y + 1] = writeutil.write(self.x, to[self.y + 1], f'│\033[31m{projectName.center(self.width - 2, " ")}\033[0m│')
		for y in range(2, self.height - 3):
			to[self.y + y] = writeutil.write(self.x, to[self.y + y], f'│{" " * (self.width - 2)}│')
		to[self.y + self.height - 3] = writeutil.write(self.x, to[self.y + self.height - 3], f'├{"─" * (self.width - 2)}┤')
		to[self.y + self.height - 2] = writeutil.write(self.x, to[self.y + self.height - 2], f'│{(str(self.fileCount) + " files").center(self.width - 2, " ")}│')
		to[self.y + self.height - 1] = writeutil.write(self.x, to[self.y + self.height - 1], f'└{"─" * (self.width - 2)}┘')
		return to
		"""
		y, x = self.window.getpayyx()
		height, width = self.window.getmaxyx()

		self.window.addstr(y, x, f'┌{"─" * (width - 2)}┐')
		scopeName = os.path.basename(self.location)
		self.window.addstr(y + 1, x, f'│{scopeName.center(width - 2, " ")}│')
		for line in range(2, height - 3):
			self.window.addstr(y + line, x, f'│{" " * (width - 2)}│')
		self.window.addstr(y + height - 3, x, f'├{"─" * (width - 2)}┤')
		self.window.addstr(y + height - 2, x, f'│{(str(fileCount) + " files").center(width - 2, " ")}│')
		self.window.addstr(y + height - 1, x, f'└{"─" * (width - 2)}┘')