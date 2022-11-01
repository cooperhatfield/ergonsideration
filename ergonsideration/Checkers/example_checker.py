from ergonsideration.checker import Checker

class ExampleChecker(Checker):
	def is_running(self) -> bool:
		return True

	def get_busy_status(self, busy):
		busy = True

	
