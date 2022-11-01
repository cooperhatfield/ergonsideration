class Checker:
	''' Abstract class defining how a `Checker` should be implemented. A checker is a python module
	which is responsible for checking if a user is "busy" with a certain program. 

	A specific checker class should implement the following:
	- `is_running` should check if the relevant program is running on the user's computer. For 
		example, a checker for Discord calls would return `False` if the Discord program is not
		running, and `True` otherwise.
	- `get_busy_status` should check if the user is busy in the specific program. For example, a 
		checker for Discord calls would set `busy` to `True` if the user is currently in a call, 
		and set it to `False` otherwise.
	- `get_timeout_time` is optional to implement. This defines the amount of time to allow 
	    `is_busy` to run before cancelling it. Currently, timing out is equivalent to 'not busy'.
	'''
	def set_name(self, name):
		self.name = name

	def get_name(self):
		return self.name

	def is_running(self) -> bool:
		raise NotImplementedError()

	def get_busy_status(self, busy):
		raise NotImplementedError()

	def get_timeout_time(self) -> int:
		return 10 #s
