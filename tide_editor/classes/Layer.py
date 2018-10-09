from tide_editor.classes.Layout import Layout

import tide_editor.terminal as terminal

class Layer:
	def __init__(self):
		self.Layout = Layout(0,0, terminal.width, terminal.height)

	def delete(self):
		pass

	def render(self, to):
		return self.Layout.render(to)