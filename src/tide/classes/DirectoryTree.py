import os
from tide.classes.File import File
from tide.classes.Folder import Folder

class DirectoryTree(Folder):
	def __init__(self, basePath):
		self.basePath = basePath
		self.name = os.path.basename(self.basePath)
		self.folders = []
		self.files = []

	def generateTree(self):
		if os.path.isfile(basePath):
			self.files.append(basePath)
		else:
			for directory in os.listdir(self.basePath):
				if os.path.isdir(directory):
					self.folders.append(Folder(os.path.relpath(f'./{directory}')))
				else:
					self.files.append(File(os.path.join(self.basePath, directory)))

	def __getitem__(self, index):
		if index in folders:
			return folders[index]
		elif index in files:
			return os.path.join(self.basePath, index)
		return None
