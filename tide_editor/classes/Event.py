"""

Event class
Usage:
myEvent = Event()				| Instantiate a Event class 
myEvent += function				| Subscribe a function to the event
myEvent.Emit()					| Emit the event

"""

class Event:
	def __init__(self):
		self.__subscribed = []

	def Emit(self, *args):
		for sub in self.__subscribed:
			sub(*args)

	def __add__(self, cb):
		if callable(cb):
			self.__subscribed.append(cb)
		return self

	def __sub__(self, cb):
		if cb in self.__subscribed:
			self.__subscribed.remove(cb)
		return self

	def __len__(self):
		return len(self.__subscribed)

	def __contains__(self, value):
		return value in self.__subscribed
