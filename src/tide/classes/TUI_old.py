import sys, shutil, re
from tide.classes.Layer import Layer

class TUI:
	"""
	TUI - Terminal User Interface
	
	...

	Attributes
	--------
	width : int
		The current width of the terminal
	height : int
		The current height of the temrinal
	lastFrame : list
		The last rendered frame
	nextFrame : list
		The upcoming frame for rendering
	layers : list
		A list of Layers
	activeLayer : int
		The index of the active layer
	__x : int
		The x position of the virtual cursor
	__y : int
		The y position of the virtual cursor

	Methods
	--------
	setCursorPosition(x, y, terminal=False)
		Set the virtual cursor position and optionally terminal cursor position
	clearTerminal()
		Clear all contents from terminal
	write(message)
		Write a message to the next frame
	addLayer(layer, setToActive=False)
		Add a new layer to the UI and optionally set it to the active layer
	deleteLayer(layer)
		Delete a layer from the UI
	update()
		Update the UI
	"""
	def __init__(self):
		"""
		TUI initialiser
		"""
		# SETUP
		self.__updateSize__()

		# PUBLIC VARIABLES
		self.lastFrame = [' ' * self.width] * self.height
		self.nextFrame = self.lastFrame
		self.layers = [Layer()]
		self.activeLayer = 0
		# PRIVATE VARIABLES
		self.__x = 0
		self.__y = 0
	
	def setCursorPosition(self, x, y, terminal=False):
		"""
		Set the virtual cursor position

		Parameters
		---------
		x : int
			The x coordinate of the cursor
			0 -> terminal width
		y : int
			The y coordinate of the cursor
			0 -> terminal height
		terminal : bool, optional
			Update the terminal cursor position (default is False)
		"""
		self.__x = x
		self.__y = y
		if terminal:
			self.__send__(f'\033[{y};{x}f')

	def clearTerminal(self):
		"""
		Clear the terminal
		"""
		self.__send__('\033[2J')
	
	def write(self, message):
		"""
		Write to the next render frame

		Parameters
		----------
		message : str
			A string message
		"""
		print(message)
		insertLine = self.nextFrame[self.__y]
		nf_splits = re.sub('(\\033\[(?:\d;|\d)+\w)', r',\1,', insertLine).split(',')
		m_splits = re.sub('(\\033\[(?:\d;|\d)+\w)', r',\1,', message).split(',')
		msg_len = len(' '.join([m_splits[x] for x in range(0, len(m_splits), 2)]))

		print(insertLine, nf_splits, m_splits, msg_len, sep='\n')

		lineIndex = 0
		startIndex = -1
		for i in range(0, len(nf_splits), 2):
			if lineIndex + len(nf_splits[i]) <= self.__x:
				if startIndex == -1:
					startIndex = self.__x - lineIndex

					if len(nf_splits[i][startIndex:]) > msg_len:
						if i > 0: # account for color
							nf_splits[i] = nf_splits[i][:startIndex] + message + nf_splits[i - 1] + nf_splits[i][startIndex + msg_len:]
						else:
							nf_splits[i] = nf_splits[i][:startIndex] + message + nf_splits[i][startIndex + msg_len:]
						break
					elif len(nf_splits[i][startIndex:]) == msg_len:
						nf_splits[i] = nf_splits[i][:startIndex] + message + nf_splits[i][startIndex + msg_len:]
						break
				if (lineIndex + len(nf_splits[i])) - self.__x < msg_len:
					del nf_splits[i]
					i -= 1
					if len(nf_splits) > i:
						del nf_splits[i + 1]
				else:
					endIndex = (self.__x + msg_len) - lineIndex
					nf_splits[i] = nf[i][endIndex:]

					self.nextFrame[self.__y] = ''.join(nf_splits)
					break
			lineIndex += len(nf_splits[i])

	def addLayer(self, layer, setToActive=False):
		"""
		Add a layer to the UI

		Parameters
		----------
		layer : Layer
			An instance of the Layer class.
		setToActive : bool, optional
			Set the active layer to this new layer (default is False)
		"""
		self.layers.append(layer)
		if setToActive:
			self.activeLayer = len(self.layers) - 1
	
	def deleteLayer(self, layer):
		"""
		Delete a layer from the UI

		Parameters
		----------
		layer : Layer
			An instance of the Layer class.
		"""
		# Dont try delete if not in layers
		# Also dont delete if its the last Layer
		if layer not in self.layers or len(self.layers) == 1:
			return
		index = self.layers.index(layer)
		del self.layers[index]
		# Set activeLayer to last layer if it was the deleted layer
		if self.activeLayer == index:
			self.activeLayer = len(self.layers) - 1

	def update(self):
		"""
		Trigger an update to the UI
		"""
		self.__updateSize__()
		self.__render__()
		self.__input__()

	def __increase__layer__(self):
		self.activeLayer = (self.activeLayer + 1) % len(self.layers)

	def __decrease_layer__(self):
		self.activeLayer = (self.activeLayer - 1) % len(self.layers)

	def __input__(self):
		"""
		Handle user input to navigate UI and pass down further through active layers
		"""
		pass

	def __render__(self, soft=True):
		"""
		Render the next frame to terminal comparing against last frame if soft is True

		Parameters
		---------
		soft : bool, optional
			Compare new frame against last frame and only render changes (default is True)
		"""
		for layer in self.layers:
			# Have layers write to new Frame
			layer.render()

		for y, line in enumerate(self.nextFrame):
			if soft:
				# Comparing current line against last frame
				if line != self.lastFrame[self.activeLayer][y]:
					continue
			self.setCursorPosition(0, y, True)
			line = f'{y:<3}:' + line
			self.__send__(line)

	def __send__(self, message):
		"""
		Write to stdout

		Parameters
		---------
		message : string
			The message to write
		"""
		print(message)
		sys.stdout.write(message)
		sys.stdout.flush()

	def __updateSize__(self):
		"""
		Update size values of terminal
		"""
		self.width, self.height = shutil.get_terminal_size((80, 20))
