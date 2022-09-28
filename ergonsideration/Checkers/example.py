from ergonsideration.checker import Checker

class Example(Checker):
	def is_running(self) -> bool:
		return True

	def get_busy_status(self) -> bool:
		return False

	
