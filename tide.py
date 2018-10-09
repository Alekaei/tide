__author__='Aleksei Ivanov'

import sys, os
from tide_editor import main

def print_help():
	print('tide <file>')

def parse_args(*args):
	pass

main(os.path.abspath('.'))