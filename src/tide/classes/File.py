class File:
	def __init__(self, path):
		self.needs_saving = False
		self.lines = [line.rstrip('\n') for line in open(path, 'r')]

		self.cursor_x = 0
		self.cursor_y = 0
		self.far_x = 0
		self.far_y = 0

	def Save(self):
		self.needs_saving = False

	def Up(self):
		self.cursor_y -= 1
		if len(lines[self.cursor_y]) - 1 < self.cursor_x:
			self.cursor_x = len(lines[self.cursor_y]) - 1

	def Down(self):
		self.cursor_y += 1
		if len(lines[self.cursor_y]) - 1 < self.cursor_x:
			self.cursor_x = len(lines[self.cursor_y]) - 1

	def Left(self):
		self.cursor_x -= 1

	def Right(self):
		self.cursor_x += 1

	def Delete(self):
		pass

	def Insert(self, key):
		pass
