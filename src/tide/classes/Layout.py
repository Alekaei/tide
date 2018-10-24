import curses
from tide.classes.View import View

class Layout:
	VERTICAL = 0
	HORIZONTAL = 1

	def __init__(self, x=0, y=0, cols=None, lines=None, type=1, split=0.5):	
		self.views = []
		self.type = type
		self.splitPoint = split
		
		self.x = x
		self.y = y
		self.cols = curses.COLS - 1 if not cols else cols
		self.lines = curses.LINES if not lines else lines

	def setView(self, index, view, *params):
		if issubclass(view, View):
			x, y, cols, lines = self.getSize(index)
			win = curses.newwin(lines, cols, y, x)
			if len(self.views) - 1 < index:
				self.views.append(view(win, *params))
			else:
				self.views[index] = view(win, *params)
		else:
			if len(self.views) - 1 < index:
				self.views.append(view(*params))
			else:
				self.views[index] = view(*params)

	def setType(self, sType):
		self.type = sType

	def getSize(self, n):
		x,y,cols,lines = self.x, self.y, self.cols, self.lines
		if self.type == Layout.HORIZONTAL:
			"""
				view[0] | view[1]
			"""
			if self.splitPoint > 0 and self.splitPoint < 1:
				# Split is a percentage between 0 and 1
				cols = int(cols * self.splitPoint)
				if n == 1: # Move x coord for right side
					x += cols
			else:
				# Split is a fixed value
				if self.splitPoint < 0:
					# Split is working from the right
					if n == 0:
						cols += self.splitPoint + 1
					elif n == 1:
						cols = -self.splitPoint
						x += cols + self.splitPoint
				else:
					# Split is working from the left
					if n == 0:
						cols = self.splitPoint - 1
					elif n == 1:
						cols = cols - self.splitPoint
						x += self.splitPoint
		elif self.type == Layout.VERTICAL:
			"""
				view[0]
				───────
				view[1]
			"""
			if self.splitPoint > 0 and self.splitPoint < 1:
				lines = int(lines * self.splitPoint)
				if n == 1:
					y += lines
			else:
				if n == 0:
					lines += self.splitPoint
				elif n == 1:
					lines = lines - self.splitPoint
					y += self.splitPoint

		return  int(x), int(y), int(cols), int(lines)
	
	def __update_size__(self, *args):
		for i in range(len(self.views)):
			if len(args) == 0:
				x, y, cols, lines = self.getSize(i)
			else:
				x, y, cols, lines = args
			self.views[i].__update_size__(x, y, cols, lines)

	def render(self):
		for view in self.views:
			view.render()
