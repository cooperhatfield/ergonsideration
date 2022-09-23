class Checker:
	def is_running(self) -> bool:
		raise NotImplementedError()

	def get_busy_status(self) -> bool:
		raise NotImplementedError()

	def timeout_time(self) -> int:
		return 100 #ms
