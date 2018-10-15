import tide.terminal as terminal
import os
from tide.classes.View import View
import tide.writeutil as writeutil

class ProjectView(View):
	def __init__(self, x, y, width, height, location):
		View.__init__(self, x, y, width, height)
		self.location = location
		self.fileCount = 0
		
		self.tree = self.getTree(self.location)

	def getTree(self, path):
		t = {'folders':{},'files': []}
		for p in os.listdir(path):
			if p == '.git':
				continue
			if os.path.isdir(p):
				t['folders'][p] = self.getTree (p)
			else:
				self.fileCount += 1
				t['files'].append(p)
		return t

	def printLeaf(self, x, y, leaf, prefix=''):
		index = 0
		for folder in leaf['folders']:
			terminal.SetCursorPosition(x, y + index)
			terminal.Write(folder)
			terminal.SetCursorPosition(self.width - 2, y + index)
			terminal.Write('▼', foreground='31')
			index += self.printLeaf(x + 2, y + index + 1, leaf['folders'][folder], prefix=prefix+'-') + 1
		for file in leaf['files']:
			terminal.SetCursorPosition(x, y + index)
			terminal.Write(prefix + ' ' + file)
			index += 1
		return index

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
		"""
		"""
		terminal.SetCursorPosition(self.x, self.y)
		terminal.Write(f'┌{"─" * (self.width - 2)}┐')
		projectName = os.path.basename(self.location)
		terminal.SetCursorPosition(self.x, self.y + 1)
		terminal.Write('│')
		terminal.Write(projectName.center(self.width - 2, ' '), foreground='31')
		terminal.Write('│')

		for x in range(2, self.height - 2):
			terminal.SetCursorPosition(self.x, self.y + x)
			terminal.Write('│')
			terminal.SetCursorPosition(self.x + self.width - 1, self.y + x)
			terminal.Write('│')

		self.printLeaf(self.x + 3, self.y + 3, self.tree)

		terminal.SetCursorPosition(self.x, self.y + self.height - 2)
		terminal.Write(f'├{"─" * (self.width - 2)}┤')
		terminal.SetCursorPosition(self.x, self.y + self.height - 1)
		terminal.Write(f'│ { (str(self.fileCount) + " files").center(self.width - 4, " ")} │')
		terminal.SetCursorPosition(self.x, self.y + self.height)
		terminal.Write(f'└{"─" * (self.width - 2)}┘')
		"""
		projectName = os.path.basename(self.location)
		to[self.y] = writeutil.write(self.x, to[self.y], f'┌{"─" * (self.width - 2)}┐')
		to[self.y + 1] = writeutil.write(self.x, to[self.y + 1], f'│\033[31m{projectName.center(self.width - 2, " ")}\033[0m│')
		for y in range(2, self.height - 3):
			to[self.y + y] = writeutil.write(self.x, to[self.y + y], f'│{" " * (self.width - 2)}│')
		to[self.y + self.height - 3] = writeutil.write(self.x, to[self.y + self.height - 3], f'├{"─" * (self.width - 2)}┤')
		to[self.y + self.height - 2] = writeutil.write(self.x, to[self.y + self.height - 2], f'│{(str(self.fileCount) + " files").center(self.width - 2, " ")}│')
		to[self.y + self.height - 1] = writeutil.write(self.x, to[self.y + self.height - 1], f'└{"─" * (self.width - 2)}┘')
		return to