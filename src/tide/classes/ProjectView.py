import os
from tide.classes.View import View

class ProjectView(View):
	def __init__(self, window, location):
		View.__init__(self, window)
		self.location = location
		self.fileCount = 0

	def render(self):
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

		#self.window.border()
		#self.window.noutrefresh()
		#return
		height, width = self.window.getmaxyx()

		self.window.insnstr(0, 0, f'┌{"─" * (width - 2)}┐', width)
		scopeName = os.path.basename(self.location)
		self.window.insnstr(1, 0, f'│{scopeName.center(width - 2, " ")}│', width)
		for line in range(2, height - 3):
			self.window.insnstr(line, 0, f'│{" " * (width - 2)}│', width)
		self.window.insnstr(height - 3, 0, f'├{"─" * (width - 2)}┤', width)
		self.window.insnstr(height - 2, 0, f'│{(str("10") + " files").center(width - 2, " ")}│', width)
		self.window.insnstr(height - 1, 0, f'└{"─" * (width - 2)}┘', width)
		self.window.noutrefresh()