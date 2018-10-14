"""

Base class for all views

"""

import tide.terminal as terminal

class View:
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

		self.ClearRegion()

	def ClearRegion(self):
		for vert in range(self.y, self.height):
			terminal.SetCursorPosition(self.x, vert)
			terminal.Write(' ' * self.width)

	def RenderBorder(self, message):
		self.ClearRegion()
		terminal.SetCursorPosition(self.x, self.y)
		terminal.Write(f'┌{"─" * self.width - 2}┐')
		for x in range(1, self.height - 2):
			terminal.SetCursorPosition(self.x, self.y + x)
			terminal.Write(f'│{" " * self.width - 2}│')
		terminal.SetCursorPosition(self.x, self.y + self.height - 1)
		terminal.Write(f'└{"─" * self.width - 2}┘')
