import sys, platform, shutil
from tide_editor.classes.Event import Event
from tide_editor.classes.Layer import Layer

if platform.system() == 'Windows':
	import ctypes

	kernel32 = ctypes.windll.kernel32
	kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
	
	class cursor_info(ctypes.Structure):
		_fields_ = [("size", ctypes.c_int), ("visible", ctypes.c_byte)]

width, height = shutil.get_terminal_size((80, 20))

# PRIVATE VARS
__last_render = [[' ' * width] * height] # Keep track of last render to only update changes
__layers = [Layer()]
__active_layer = 0

onTerminalResize = Event()

# soft render means use __last_render otherwise ignore it
def __render__(soft=True):
	global __last_render, __layers, width, height
	width, height = shutil.get_terminal_size((80, 20))
	newRenderFrame = [' ' * width] * height
	for layer in __layers:
		# Generate new frame
		newRenderFrame = layer.render(newRenderFrame)

	if soft:
		# If soft render then only render any changed lines
		for index, line in enumerate(newRenderFrame):
			if line == __last_render:
				continue
			SetCursorPosition(1, 1 + index)
			if index == height - 1:
				Write(line[:-300:])
				pass
			else:
				Write(line)

	else:
		# If hard render then force render every new frame
		for index, line in enumerate(newRenderFrame):
			#SetCursorPosition(1, 1 + index)
			#Write(line)
			pass
	
	# Update last render to new render
	__last_render = newRenderFrame

def __update__():
	pass

def __send__(message):
	sys.stdout.write(message)
	sys.stdout.flush()

def SetCursor(state):  # FROM https://stackoverflow.com/questions/5174810/how-to-turn-off-blinking-cursor-in-command-window
	if platform.system() == 'Windows':
		ci = cursor_info()
		handle = kernel32.GetStdHandle(-11)
		kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
		ci.visible = state
		kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
	else:
		sys.stdout.write(f"\033[?25{'h' if state else 'l'}")
		sys.stdout.flush()

def SetCursorPosition(x, y):
	__send__(f'\033[{y};{x}f')

def ClearTerminal():
	__send__('\033[2J')

def ClearLine(y):
	SetCursorPosition(0, y)
	__send__('\033[K')

def Write(message, foreground='37', background='40'):
	__send__(f'\033[{foreground};{background}m{message}\033[0m')

def WriteLine(message, foreground='37', background='40'):
	__send__(f'\033[{foreground};{background}m{message}\033[0m\n')

def Centerize(x, y, width, height, *lines):
	width_left = width - max(lines)

def DeleteLayer(layer):
	if layer not in __layers or len(__layers) == 1:
		return
	del __layers[__layers.index(layer)]

def AddLayer(layer, setActive=False):
	__layers.append(layer)
	if setActive:
		__active_layer = len(__layers) - 1

def SetColor(color):
	__send__(f'\033[{color}m')
