
import keyboard, os, re
import tide_editor.terminal as terminal
from tide_editor.classes.View import View
from tide_editor.classes.File import File
import tide_editor.writeutil as writeutil

class EditorView(View):
	def __init__(self, x, y, width, height):
		View.__init__(self, x, y, width, height)

		self.openFiles = []
		self.file_index = 0

		self.openFiles.append(File(os.path.abspath('./test.py')))

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
		to[self.y + 1] = writeutil.write(self.x, to[self.y + 1], '┌──────┐')
		for y in range(2, self.height - 2):
			to[self.y + y] = writeutil.write(self.x, to[self.y + y], f'│      │')
		to[self.y + self.height - 3] = writeutil.write(self.x, to[self.y + self.height - 3], f'├──────┴{"─" * (self.width - 9)}┐')
		to[self.y + self.height - 2] = writeutil.write(self.x, to[self.y + self.height - 2], f'│{" " * (self.width - 2)}│')
		to[self.y + self.height - 1] = writeutil.write(self.x, to[self.y + self.height - 1], f'└{"─" * (self.width - 2)}┘')
		to = self.__render_files(to)
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

	def Update(self):
		if len(self.openFiles) == 0:
			return
		openFile = self.openFiles[self.file_index]
		terminal.SetCursorPosition(self.max_x + openFile.cursor_x, self.max_y + openFile.cursor_y)

	def __no_open_files(self, to):
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

	def __render_files(self, to):
		if len(self.openFiles) == 0:  # No Files Open
			return self.__no_open_files(to)
		openFilesLine = ""
		for i, file in enumerate(self.openFiles):
			if i == self.file_index:  # CURRENT OPEN FILE
				openFilesLine += f' \033[31m[{file.name:<12}{"●" if file.needs_saving else " "}]\033[0m'

				# Render currently opened file to terminal
				file_no_start = file.getLowerLimit()
				for line in range(0, min(len(file.lines), self.height - 5)):
					to[self.y + 2 + line] = writeutil.write(self.x + 1, to[self.y + 2 + line], f'{file_no_start + line:>5} ')
					to[self.y + 2 + line] = writeutil.write(self.x + 9, to[self.y + 2 + line], re.sub(r'\t', '    ', file.lines[line]))
				to[self.y + self.height - 2] = writeutil.write(self.x + 1, to[self.y + self.height - 2], f'{file.encoding}  {file.fileType}')
				cursor_pos = f'Ln {file.cursor_y}, Col {file.cursor_x}'
				to[self.y + self.height - 2] = writeutil.write(self.x + self.width - len(cursor_pos) - 2, to[self.y + self.height - 2], cursor_pos)
			else:
				openFilesLine += f' [{file.name:<12}{"●" if file.needs_saving else " "}]'
			openFilesLine = openFilesLine.strip()
		to[self.y] = writeutil.write(self.x + 8, to[self.y], openFilesLine)
		return to
