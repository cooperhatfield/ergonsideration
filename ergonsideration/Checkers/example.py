from ergonsideration.checker import Checker

class Example(Checker):
	def is_running() -> bool:
		return True

	def get_busy_status() -> bool:
		return False

	
