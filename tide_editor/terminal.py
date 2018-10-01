import sys, ctypes, platform, shutil

width, height = shutil.get_terminal_size((80, 20))

if platform.system() == 'Windows':
	kernel32 = ctypes.windll.kernel32
	kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


def __send__(message):
	sys.stdout.write(message)
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
