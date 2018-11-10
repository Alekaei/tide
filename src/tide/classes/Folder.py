class Folder:
	def __init__(self, basePath):
		self.basePath = basePath
		self.name = os.path.basename(self.basePath)
		self.folders = []
		self.files = []

	def generateTree(self):
		for directory in os.listdir(self.basePath):
			if os.path.isdir(directory):
				self.folders.append(DirectoryTree(os.path.relpath(f'./{directory}')))
			else:
				self.files.append(File(os.path.join(self.basePath, directory)))

	def __getitem__(self, index):
		if index in folders:
			return folders[index]
		elif index in files:
			return os.path.join(self.basePath, index)
		return None