import os
import tide_editor.terminal as terminal

class Layer:
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

		self.clearRegion()

	def clearRegion(self):
		for vert in range(self.y, self.height):
			terminal.SetCursorPosition(self.x, vert)
			terminal.Write(' ' * self.width)

class Terminal(Layer):
	def __init__(self, x, y, width, height, location):
		Layer.__init__(self, x, y, width, height)
		self.location = location
		self.buffer = [None] * 300
		self.input = ''

	def write(self, message, foreground='30', background='40'):
		if None in self.buffer:
			self.buffer[self.buffer.index(None)] = f'\033[{foreground};{background}m{message}\033[0m'

	def render(self):
		self.clearRegion()
		""" Example View
			┌─ Terminal ─────────────────────────┐
			│                                    │
			│                                    │
			│                                    │
			├────────────────────────────────────┤
			│ ~ >                                │
			└────────────────────────────────────┘
		"""
		terminal.SetCursorPosition(self.x, self.y)
		terminal.Write(f'┌─ Terminal {"─" * (self.width - 13)}┐')
		for x in range(1, self.height - 3):
			terminal.SetCursorPosition(self.x, self.y + x)
			terminal.Write('│')
			terminal.SetCursorPosition(self.x + self.width, self.y + x)
			terminal.Write('│')
		terminal.SetCursorPosition(self.x, self.y + self.height - 3)
		terminal.Write(f'├{"─" * (self.width - 2)}┤')

		terminal.SetCursorPosition(self.x, self.y + self.height - 2)
		terminal.Write('│ ')
		terminal.Write(self.location, foreground='31')
		terminal.Write(' >')
		terminal.SetCursorPosition(self.x + self.width, self.y + self.height - 2)
		terminal.Write('│')

		terminal.SetCursorPosition(self.x, self.y + self.height)
		terminal.Write(f'└{"─" * (self.width - 2)}┘')

class Editor(Layer):
	def __init__(self, x, y, width, height):
		Layer.__init__(self, x, y, width, height)
		

	def render(self):
		self.clearRegion()
		""" Example View
					[ sqrt.py     ● ][ test.py       ]
			┌──────┐
			│    1 │ import math
			│    2 │
			│    3 │ print('This program gets the sqrt of 25')
			│    4 │ print(f'sqrt (25) = {math.sqrt(25)}')
			│    5 │
			│    6 │
			│    7 │
			│    8 │
			│    9 │
			│   10 │
			├──────┴─────────────────────────────────────────────────────────────────────────┐
			│ utf-8  python                                                     Ln 12, Col 4 │
			└────────────────────────────────────────────────────────────────────────────────┘
		"""
		terminal.SetCursorPosition(self.x + 8, self.y)
		terminal.Write('\033[31m[ sqrt.py     ● ]\033[0m[ test.py       ]')
		terminal.SetCursorPosition(self.x, self.y + 2)
		terminal.Write('┌──────┐')

		for x in range(3, self.height - 2):
			terminal.SetCursorPosition(self.x, self.y + x)
			terminal.Write(f'│{x-2:>5} │')
		
		terminal.SetCursorPosition(self.x, self.y + self.height - 2)
		terminal.Write(f'├──────┴{"─" * (self.width - 9)}┐')
		terminal.SetCursorPosition(self.x, self.y + self.height - 1)
		terminal.Write('│ utf-8  python')
		terminal.SetCursorPosition(self.x + self.width - 14, self.y + self.height - 1)
		terminal.Write('Ln 12, Col 4 │')
		terminal.SetCursorPosition(self.x, self.y + self.height)
		terminal.Write(f'└{"─" * (self.width - 2)}┘')

		# TEMP RENDER FAKE FILE
		terminal.SetCursorPosition(self.x + 9, self.y + 3)
		terminal.Write('\033[34mimport\033[0m math')

		terminal.SetCursorPosition(self.x + 9, self.y + 5)
		terminal.Write('\033[34mprint\033[0m(\033[32;1m\'This program gets the sqrt of 25\'\033[0m)')
		terminal.SetCursorPosition(self.x + 1, self.y + 6)
		terminal.Write('\033[41m    4 \033[0m')
		terminal.SetCursorPosition(self.x + 9, self.y + 6)
		terminal.Write('\033[34mprint\033[0m(\033[35mf\033[32;1m\'sqrt (25) = \033[33m{\033[0mmath.sqrt(25)\033[33m}\033[32;1m\'\033[0m)')


class Project(Layer):
	def __init__(self, x, y, width, height, location):
		Layer.__init__(self, x, y, width, height)
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

	def render(self):
		self.clearRegion()
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
		terminal.SetCursorPosition(self.x, self.y)
		terminal.Write(f'┌{"─" * (self.width - 2)}┐')
		projectName = os.path.basename(self.location)
		terminal.SetCursorPosition(self.x, self.y + 2)
		terminal.Write('│')
		terminal.Write(projectName.center(self.width - 2, ' '), foreground='31')
		terminal.Write('│')

		for x in range(3, self.height - 2):
			terminal.SetCursorPosition(self.x, self.y + x)
			terminal.Write('│')
			terminal.SetCursorPosition(self.x + self.width, self.y + x)
			terminal.Write('│')

		self.printLeaf(self.x + 3, self.y + 3, self.tree)

		terminal.SetCursorPosition(self.x, self.y + self.height - 2)
		terminal.Write(f'├{"─" * (self.width - 2)}┤')
		terminal.SetCursorPosition(self.x, self.y + self.height - 1)
		terminal.Write(f'│ { (str(self.fileCount) + " files").center(self.width - 4, " ")} │')
		terminal.SetCursorPosition(self.x, self.y + self.height)
		terminal.Write(f'└{"─" * (self.width - 2)}┘')
