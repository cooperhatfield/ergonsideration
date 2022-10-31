class Checker:
	def set_name(self, name):
		self.name = name

	def get_name(self):
		return self.name

	def is_running(self) -> bool:
		raise NotImplementedError()

	def get_busy_status(self, busy) -> bool:
		raise NotImplementedError()

	def get_timeout_time(self) -> int:
		return 10 #s
