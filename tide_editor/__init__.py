from tide_editor.classes import *
import tide_editor.terminal as terminal

import os

def main(path):
	alive = True
	terminal.ClearTerminal()
	proj = Project(0, 0, 20, terminal.height, path)
	term = Terminal(21, terminal.height - 9, terminal.width - 20, 10, path)
	edit = Editor(21, 0, terminal.width - 20, terminal.height - 10)
	proj.render()
	term.render()
	edit.render()
	while alive:
		# Main update loop
		pass
	# Check if files need saving
		# Do some stuff with `edit`
	# Clear Screen
	terminal.ClearTerminal()
	# Quit
	quit()
