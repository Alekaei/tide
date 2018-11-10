__author__ = 'Aleksei Ivanov'
__version__ = '0.0.1'

import os, time, traceback, platform, curses, argparse

if platform.system() == 'Windows':
	pritn('Windows is not supported')
	quit()

from tide.classes.TerminalView import TerminalView
from tide.classes.EditorView import EditorView
from tide.classes.ProjectView import ProjectView
from tide.classes.Layout import Layout

from tide.classes.TUI import TUI
from tide.classes.Localization import Localization
from tide.classes.Logger import logger

tui = None
localization = None
directory = None

# TEMPORARY: this 
def layout_temporary(self):
	# LOAD FROM A LAYOUT FILE IN FUTURE --- TEMPORARY SOLUTION BELOW
	tui.layout.setType(Layout.HORIZONTAL)								# Set the layout to split vertically
	tui.layout.splitPoint = min([30, (curses.COLS * 0.3)]) 				# Set the split point `x` in from the left
	tui.layout.setView(0, ProjectView, self.file) 						# Setting left view to a `project` however need to implement dynamic argument passing !!!!!!!!
																		# Idealy it would be ~~~.setView(0, ProjectView, path)
	tui.layout.setView(1, Layout)										# Set the right view to a `Layout`
	tui.layout.views[1].setType(Layout.VERTICAL)						# Set the layout type to a vertical split
	tui.layout.views[1].splitPoint = min([-20, (curses.LINES * 0.75)])	# Set the split point to be 20 from the bottom
	tui.layout.views[1].setView(0, EditorView)							# Set the top layout view to a `Editor`
	tui.layout.views[1].setView(1, TerminalView, self.file)		   	 	# Set the bottom layout view to a `Terminal`


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
		logger.logInformation('Initializing TideApp...')

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
		global tui, localization
		
		#print(self.__parse_args__())

		#quit()
		# Allow the editor to run if requested
		self.should_run = True
		self.screen = curses.initscr()
		self.__color_init__()
		curses.noecho()
		curses.cbreak()
		curses.raw()
		self.screen.keypad(True)


		logger.logInformation('Initializing TUI...')
		tui = TUI()
		logger.logInformation('Done...')
		logger.logInformation('Initializing Localization...')
		localization = Localization()
		logger.logInformation('Done...')


		if "--help" in self.args:
			self.print_help()
			# we dumped help, now prevent the editor from executing, causing it to exit
			self.should_run = False

		if len(self.args) > 1:
			# TODO: we need to modify the File class to test for this at the time
			self.file = self.args[1]
		else:	
			self.file = os.path.abspath(".")
		
		logger.logInformation(f'Starting TideApp in dir \'{self.file}\'')

		return self

	def run(self):

		# temporary layout
		#layout_temporary(self)
		logger.logInformation('Generating temporary Layout')
		tui.layout.setType(Layout.HORIZONTAL)
		tui.layout.splitPoint = 30
		tui.layout.setView(0, ProjectView, self.file)
		#tui.layout.setView(1, EditorView)
		tui.layout.setView(1, Layout)
		tui.layout.views[1].setType(Layout.VERTICAL)
		tui.layout.views[1].splitPoint = -10
		tui.layout.views[1].setView(0, EditorView)
		tui.layout.views[1].setView(1, TerminalView, self.file)
		
		lastUpdate = time.time()
		tui.__render__()
		while self.should_run:
			# Main update loop
			# Render loop every 100ms
			key = self.screen.getch()

			tui.__render__()

			if key == ord('q'):
				self.cleanup()
				break
			y, x = self.screen.getmaxyx()
			if y != curses.LINES or x != curses.COLS:
				self.update_size(x, y)

	def update_size(self, width, height):
		curses.resizeterm(height, width)
		self.screen.refresh()
		logger.logInformation(f'Terminal size updated to `{[width, height]}`')
		tui.layout.cols = width
		tui.layout.lines = height
		tui.layout.__update_size__()

	def cleanup(self):
		curses.endwin()

	def __exit__(self, type, value, traceback):
		self.cleanup()

	def __parse_args__(self):
		parser = argparse.ArgumentParser(
			description='TIDE is a terminal integrated development environment capable of editing files through the terminal'
		)
		parser.add_argument(
			'location',
			dest='scope',
			metavar='PATH',
			type=str,
			help='the path to scope from, can be a file or folder'
		)
		parser.add_argument(
			'-l',
			'--loglevel',
			dest='loglevel',
			required=False,
			type=int,
			default=1,
			help='the level of logging to provide (default: 1), --levels to see a list of available'
		)
		parser.add_argument(
			'--levels',
			dest='levels',
			required=False,
			help='list of log levels'
		)

		return vars(parser.parse_args())

	def __color_init__(self):
		curses.start_color()
		curses.use_default_colors()
		for i in range(0, curses.COLORS):
			curses.init_pair(i, i, -1);