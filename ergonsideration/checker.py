class Checker:
	def is_running(self) -> bool:
		raise NotImplementedError()

	def get_busy_status(self, busy) -> bool:
		raise NotImplementedError()

	def get_timeout_time(self) -> int:
		return 10 #s
