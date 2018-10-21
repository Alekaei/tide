__author__ = 'Aleksei Ivanov'
__version__ = '0.0.1'

import os, time, keyboard, traceback

from tide.classes.TerminalView import TerminalView
from tide.classes.EditorView import EditorView
from tide.classes.ProjectView import ProjectView
from tide.classes.Layout import Layout

import tide.terminal as terminal

from tide.classes.TUI import TUI
from tide.classes.Localization import Localization

tui = TUI()
localization = Localization()


# TEMPORARY: this 
def layout_temporary(self):
	# LOAD FROM A LAYOUT FILE IN FUTURE --- TEMPORARY SOLUTION BELOW
	# __layers[0] is the base layer
	terminal.__layers[0].Layout.setType(Layout.HORIZONTAL)								# Set the layout to split vertically
	terminal.__layers[0].Layout.splitPoint = 30 										# Set the split point `x` in from the left
	terminal.__layers[0].Layout.setView(0, ProjectView, self.file) 						# Setting left view to a `project` however need to implement dynamic argument passing !!!!!!!!
																						# Idealy it would be ~~~.setView(0, ProjectView, path)
	terminal.__layers[0].Layout.setView(1, Layout)										# Set the right view to a `Layout`
	terminal.__layers[0].Layout.views[1].setType(Layout.VERTICAL)						# Set the layout type to a vertical split
	terminal.__layers[0].Layout.views[1].splitPoint = -20								# Set the split point to be 20 from the bottom
	terminal.__layers[0].Layout.views[1].setView(0, EditorView)							# Set the top layout view to a `Editor`
	terminal.__layers[0].Layout.views[1].setView(1, TerminalView, self.file)		    # Set the bottom layout view to a `Terminal`


class TideApp:
	def __init__(self, args):
		"""
		TIDE initializer

		__init__ is primarily dedicated to saving args, see __enter__ for arg parsing & actual app logic

		Parameters
		----------
		args : list
			Expected to follow sys.argv format (where [0] is script, [1] first arg, etc..)
			See dump_help() for the command syntax
		"""
		self.args = args

	def print_help(self):
		"""Print tide command help to stdout"""

		print(
		"""
		Usage: tide [file] [OPTIONS]

		Options:\tMeaning
		--help\tPrint help and exit
		""")

	def __enter__(self):
		"""Executed on example: with TideApp(sys.argv) as app:"""

		# Allow the editor to run if requested
		self.should_run = True

		if "--help" in self.args:
			self.print_help()
			# we dumped help, now prevent the editor from executing, causing it to exit
			self.should_run = False

		if len(self.args) > 1:
			# TODO: we need to modify the File class to test for this at the time
			self.file = self.args[1]
		else:	
			self.file = os.path.abspath(".")

		return self

	def run(self):
		terminal.ClearTerminal()

		# temporary layout
		layout_temporary(self)

		lastUpdate = time.time()
		while self.should_run:
			# Main update loop
			# Render loop every 100ms
			if time.time() - lastUpdate > 0.1:
				terminal.SetCursor(False)
				terminal.__render__()
				terminal.SetCursorPosition(1,1)
				lastUpdate = time.time()
				terminal.SetCursor(True)

			if keyboard.is_pressed('esc'):
				self.cleanup()
				break

	def cleanup(self):
		terminal.ClearTerminal();

	def __exit__(self, type, value, traceback):
		self.cleanup()
