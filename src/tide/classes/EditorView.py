
import os, re, curses
from tide.classes.View import View
from tide.classes.File import File
from tide.classes.Logger import logger

class EditorView(View):
	def __init__(self, window):
		View.__init__(self, window)

		self.openFiles = []
		self.file_index = 0

		self.openFiles.append(File(os.path.abspath('./test.py')))
		self.openFiles.append(File(os.path.abspath('./tide/__init__.py')))

	def render(self):
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
		height, width = self.window.getmaxyx()

		logger.logInformation(f'Drawing {self} at size `{[width, height]}`')

		self.window.insnstr(1, 0, f'┌──────┐{" " * (width - 8)}', width)
		for editorline in range(2, height - 3):
			self.window.insnstr(editorline, 0, f'│      │{" " * (width - 8)}', 0)
		self.window.insnstr(height - 3, 0, f'├──────┴{"─" * (width - 9)}┐', width)
		self.window.insnstr(height - 2, 0, f'│{" " * (width - 2)}│', width)
		self.window.insnstr(height - 1, 0, f'└{"─" * (width - 2)}┘', width)
		self.window.addstr(height - 2, 2, 'utf-8 python')
		self.window.addstr(height - 2, width - 13, 'Ln 1, Col 1')

		self.__render_files()

		self.window.noutrefresh()

	def OpenFile(self, path):
		self.far_x = 0
		self.far_y = 0
		self.openFiles.append(File(path))

	def Update(self):
		if len(self.openFiles) == 0:
			return
		openFile = self.openFiles[self.file_index]

	def __no_open_files(self):
		"""
		width = self.width - 10
		height = self.height - 5
		msg_lines = [
			"┌─┬─────┬─┐",
			"│ └─────┘ │    Oh no!",
			"│▐███████▌│    You haven't opened a file yet :(",
			"││───────││",
			"││───────││",
			"└┴───────┴┘"
		]
		start_y = (height // 2) - 2
		start_x = (width // 2)
		for i in range(len(msg_lines)):
			to[start_y + i] = writeutil.write(start_x, to[start_y + i], msg_lines[i])
		return to
		"""
		height, width = self.window.getmaxyx()

		msg_lines = [
			"┌─┬─────┬─┐",
			"│ └─────┘ │    Oh no!",
			"│▐███████▌│    You haven't opened a file yet :(",
			"││───────││",
			"││───────││",
			"└┴───────┴┘"
		]

		start_y = ((height - 5) // 2) - 2
		start_x = ((width - 10) // 2)

		for i in range(len(msg_lines)):
			self.window.addstr(start_y + i, start_x, msg_lines[i])

		pass

	def __render_files(self):
		height, width = self.window.getmaxyx()
		if len(self.openFiles) == 0:
			self.__no_open_files()
			return;
		openFilesLineIndex = 9

		for i, file in enumerate(self.openFiles):
			fileLine = f'[{file.name:<12}{"●" if file.needs_saving else " "}]'
			if i == self.file_index:

				self.window.addstr(0, openFilesLineIndex, fileLine, curses.color_pair(161))
				
				for line in range(min(len(file.lines), height - 5)):
					self.window.addstr(2 + line, 1, f'{line + 1:>5}')
					self.window.addstr(2 + line, 9, file.lines[line])
			else:
				self.window.addstr(0, openFilesLineIndex, fileLine)
				pass
			openFilesLineIndex += len(fileLine) + 1
		pass