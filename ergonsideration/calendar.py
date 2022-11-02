import sched

#class Calendar:
'''This class will have tasks registered, and run those tasks at the proper intervals.
'''
_instance = None

def register_task(delay, task_action, priority=0):
	''' Given a task, register its task action (usually `run_task` function) to run after a 
	delay.
	'''
	_instance.enter(delay, priority, task_action)

def run_schedule():
	''' Start the schedule with the registered tasks. This will block execution until a task is
	run.
	'''
	_instance.run()

if _instance is None:
	_instance = sched.scheduler()