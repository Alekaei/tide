import keyboard
import tide_editor.terminal as terminal
from tide_editor.classes.View import View
from tide_editor.classes.File import File

class EditorView(View):
	def __init__(self, x, y, width, height):
		View.__init__(self, x, y, width, height)

		self.openFiles = []
		self.file_index = 0

		self.min_x = self.x + 9
		self.max_x = self.x + self.width - 2
		self.min_y = self.y + 2
		self.max_y = self.y + self.height - 4

	def render(self, to):
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
		## NEW RENDER MODE

		## OLD RENDER MODE
		"""
		terminal.SetCursorPosition(self.x + 8, self.y)
		terminal.Write('\033[31m[ sqrt.py     ● ]\033[0m[ test.py       ]')
		terminal.SetCursorPosition(self.x, self.y + 1)
		terminal.Write('┌──────┐')

		for x in range(3, self.height - 2):
			terminal.SetCursorPosition(self.x, self.y + x - 1)
			terminal.Write(f'│{x-2:>5} │')
		
		terminal.SetCursorPosition(self.x, self.y + self.height - 3)
		terminal.Write(f'├──────┴{"─" * (self.width - 9)}┐')
		terminal.SetCursorPosition(self.x, self.y + self.height - 2)
		terminal.Write('│ utf-8  python')
		terminal.SetCursorPosition(self.x + self.width - 14, self.y + self.height - 2)
		terminal.Write('Ln 12, Col 4 │')
		terminal.SetCursorPosition(self.x, self.y + self.height - 1)
		terminal.Write(f'└{"─" * (self.width - 2)}┘')

		# TEMP RENDER FAKE FILE
		terminal.SetCursorPosition(self.x + 9, self.y + 3)
		terminal.Write('\033[34mimport\033[0m math')

		terminal.SetCursorPosition(self.x + 9, self.y + 5)
		terminal.Write('\033[34mprint\033[0m(\033[32;1m\'This program gets the sqrt of 25\'\033[0m)')
		terminal.SetCursorPosition(self.x + 1, self.y + 6)
		terminal.Write('\033[41m    5 \033[0m')
		terminal.SetCursorPosition(self.x + 9, self.y + 6)
		terminal.Write('\033[34mprint\033[0m(\033[35mf\033[32;1m\'sqrt (25) = \033[33m{\033[0mmath.sqrt(25)\033[33m}\033[32;1m\'\033[0m)')
		"""
		return to

	def RenderFile(self):
		if len(self.openFiles) == 0:
			return

		openFile = self.openFiles[self.file_index]

		line_index = 0 if openFile.far_y <= self.height - 6 else openFile.far_x - (self.height - 6)
		line_start_index = 0 if openFile.far_x <= self.width - 11 else openFile.far_y - (self.width - 11)


	def OpenFile(self, path):
		self.far_x = 0
		self.far_y = 0
		self.openFiles.append(File(path))
		self.render()

	def Update(self):
		if len(self.openFiles) == 0:
			return
		openFile = self.openFiles[self.file_index]
		terminal.SetCursorPosition(self.max_x + openFile.cursor_x, self.max_y + openFile.cursor_y)
