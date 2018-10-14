class Layout:
	VERTICAL = 0
	HORIZONTAL = 1
	CENTER = 2
	TOP_LEFT = 3
	TOP_RIGHT = 4
	BOTTOM_LEFT = 5
	BOTTOM_RIGHT = 6
	SCALE = 7

	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		
		self.views = [0, 1]
		self.type = Layout.HORIZONTAL
		self.splitPoint = self.width // 2

	def setView(self, index, view):
		view_x = self.x
		view_y = self.y
		view_width = self.width
		view_height = self.height

		if self.type == Layout.VERTICAL:
			if self.splitPoint < 0:  # Negative value
				if index == 0:
					view_x = self.x
					view_y = self.y
					view_width = self.width
					view_height = self.height + self.splitPoint 
				else:
					view_x = self.x
					view_y = self.y + (self.height + self.splitPoint)
					view_width = self.width
					view_height = -self.splitPoint
			else:
				if index == 0:
					view_x = self.x
					view_y = self.y
					view_width = self.width
					view_height = self.splitPoint
				else:
					view_x = self.x
					view_y = self.y + self.splitPoint + 1
					view_width = self.width
					view_height = self.height - self.splitPoint
			pass
		elif self.type == Layout.HORIZONTAL:
			if self.splitPoint < 0: # Negative value
				if index == 0:
					view_x = self.x
					view_y = self.y
					view_width = self.width + self.splitPoint
					view_height = self.height
				else:
					view_x = self.x + (self.width + self.splitPoint)
					view_y = self.y
					view_width = -self.splitPoint
					view_height = self.height
			else:
				if index == 0:
					view_x = self.x
					view_y = self.y
					view_width = self.splitPoint
					view_height = self.height
				else:
					view_x = self.x + self.splitPoint + 1
					view_y = self.y
					view_width = self.width - self.splitPoint
					view_height = self.height
		view.x = view_x
		view.y = view_y
		view.width = view_width
		view.height = view_height
		self.views[index] = view

	def setType(self, sType):
		self.type = sType
		if self.type == Layout.VERTICAL:
			self.splitPoint = self.height // 2
		elif self.type == Layout.HORIZONTAL:
			self.splitPoint = self.width // 2

	def increase(self):
		if self.width - (self.splitPoint + 1) < 3:
			return
		self.splitPoint += 1

	def decrease(self):
		if self.splitPoint - 1 < 3:
			return
		self.splitPoint -= 1
	
	def setSize(self, width, height):
		self.width = width
		self.height = height

	def setPos(self, x, y):
		self.x = x
		self.y = y
	
	def render(self, to):
		if len(self.views) == 0:
			return to
		if self.type == Layout.HORIZONTAL or self.type == Layout.VERTICAL:
			frames = self.views[0].render(to)
			frames = self.views[1].render(frames)
			return frames
		return self.views[0].render(to)

