from tide_editor.classes.TerminalView import TerminalView
from tide_editor.classes.EditorView import EditorView
from tide_editor.classes.ProjectView import ProjectView
from tide_editor.classes.Layout import Layout

import tide_editor.terminal as terminal

import os, time, keyboard, traceback

def main(path):
	alive = True
	terminal.ClearTerminal()
	"""
	proj = ProjectView(0, 0, 20, terminal.height - 1, path)
	term = TerminalView(20, terminal.height - 10, terminal.width - 20, 10, path)
	edit = EditorView(20, 0, terminal.width - 20, terminal.height - 10)
	
	# Initial terminal render
	proj.render()
	edit.render()
	term.render()
	"""

	# LOAD FROM A LAYOUT FILE IN FUTURE --- TEMPORARY SOLUTION BELOW
	# __layers[0] is the base layer
	terminal.__layers[0].Layout.setType(Layout.HORIZONTAL)								# Set the layout to split vertically
	terminal.__layers[0].Layout.splitPoint = 30 										# Set the split point `x` in from the left
	terminal.__layers[0].Layout.setView(0, ProjectView(0, 0, 0, 0, path)) 				# Setting left view to a `project` however need to implement dynamic argument passing !!!!!!!!
																						# Idealy it would be ~~~.setView(0, ProjectView, path)
	terminal.__layers[0].Layout.setView(1, Layout(0, 0, 0, 0))							# Set the right view to a `Layout`
	terminal.__layers[0].Layout.views[1].setType(Layout.VERTICAL)						# Set the layout type to a vertical split
	terminal.__layers[0].Layout.views[1].splitPoint = -20								# Set the split point to be 20 from the bottom
	terminal.__layers[0].Layout.views[1].setView(0, EditorView(0, 0, 0, 0))				# Set the top layout view to a `Editor`
	terminal.__layers[0].Layout.views[1].setView(1, TerminalView(0, 0, 0, 0, path))		# Set the bottom layout view to a `Terminal`

	lastUpdate = time.time()
	while alive:
		# Main update loop
		# Render loop every 100ms
		if time.time() - lastUpdate > 0.1:
			terminal.SetCursor(False)
			terminal.__render__()
			terminal.SetCursorPosition(1,1)
			lastUpdate = time.time()
			terminal.SetCursor(True)

		if keyboard.is_pressed('esc'):
			break
		
	# Check if files need saving
		# Do some stuff with `edit`
	# Clear Screen
	terminal.ClearTerminal()
	# Quit
	quit()