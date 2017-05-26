import manager_fog
class module(object):

	def __init__ (self, tmp):
		self.tmp = tmp
		self.data = []

	def controller(self):
		self.data.append(manager_fog.cartridge(self.tmp))
		print self.data
	def get_payload(self):
		return self.data

		
