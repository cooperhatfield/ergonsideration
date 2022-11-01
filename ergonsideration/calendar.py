import sched

from task import Task

class Calendar:
	'''This class will have tasks registered, and run those tasks at the proper intervals.
	'''
	self.instance = None

	def __init__(self):
		''' Create a singleton instance of the calendar class.
		'''
		if self.instance is not None:
			return self.instance
		self.scheduler = sched.scheduler()
		self.instance = self

	def register_task(self, delay, task_action):
		''' Given a task, register its task action (usually `run_task` function) to run after a 
		delay.
		'''
		self.scheduler.enter(delay, task_action)

	def run_schedule(self):
		''' Start the schedule with the registered tasks. This will block execution until a task is
		run.
		'''
		self.scheduler.run()
