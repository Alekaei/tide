"""


REQUIRES MORE WORK


"""

import yaml, os

class Localization:
	def __init__(self, defaultLocale='en'):
		self.locales = {}
		self.locale = defaultLocale

	def loadLocale(self, path):
		"""
		Load a locale from a path

		Parameters
		--------
		path : str
			Path to a .yml locale file
		"""
		lang = os.path.basename(path).split('.')[0]
		with open(path, 'r') as stream:
			if lang in self.locales:
				self.locales[lang] += yaml.safe_load(stream)
			else:
				self.locales[lang] = yaml.safe_load(stream)
	
	def hasLocale(self, lang):
		"""
		Checks if a locale exists

		Parameters
		--------
		lang : str
			A locale to check for i.e. `en`
		
		Returns
		--------
		bool
			A True or False indicating whether the locale exists or not
		"""
		return lang in locales

	def setLocale(self, lang):
		"""
		Set the current locale

		Parameters
		--------
		lang : str
			A locale to check for i.e. `en`
		"""
		if not self.hasLocale(lang):
			return
		self.locale = lang

	def translate(self, key):
		"""
		Translates a key to a localized string

		Parameters
		--------
		key : str
			The key to search for
		
		Returns
		--------
		str
			A localized string if successful
		None
			If it fails to find a localized string for that key
		"""
		if key not in self.locales[self.locale]:
			return None
		return self.locales[self.locale][key]
