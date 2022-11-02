import multiprocessing

from ergonsideration.checker import Checker
import ergonsideration.calendar as calendar
import ergonsideration.notify as notify

class Task:
	''' A task is an object representing a specific action (theoretically an ergonomic reminder),
	such as 'get up to stretch every hour'. A task object will contain the relevant checkers, the
	configuration for when to run the task, and the configuration for the task's notification.
	'''
	def __init__(self, notification_config, schedule_config, checkers):
		self.notification_config = notification_config
		self.schedule_config = schedule_config
		self.checkers = checkers

	def run_task(self):
		''' Check if the user is busy. If not, then send a notification.
		TODO:
		- add logic for buttons on the notification
		- support for snoozing
		- support for task ending notifications
		'''
		user_is_busy = self.is_busy()
		if not user_is_busy:
			notify.send_notification(self.notification_config)
		# check notification button press for snooze or what not
		delay = self.schedule_config['interval']
		calendar.register_task(delay, self.run_task)

	def is_busy(self):
		''' Check with each registered checker to see if the user is busy. If a checker times out,
		isn't a proper instance of the `Checker` class, or doesn't implement all relevant 
		functions, then it is ignored.
		TODO:
		- optional behavior for ignoring, quitting, or assuming the user is busy when a checker
			times out
		'''
		busy = multiprocessing.Value(bool, False)
		for checker in self.checkers:
			try:
				assert issubclass(checker, Checker)
				if not checker.is_running():
					pass
				else:
					p = multiprocessing.Process(target=checker.get_busy_status, args=busy)
					p.start()
					p.join(checker.get_timeout_time())
					if p.is_alive():
						print(f'Checker {checker.get_name()} timed out when getting busy status. ignored.')
						p.terminate()
					elif busy:
						return True
			except AssertionError:
				print(f'Module {checker.get_name()} is not a proper child of Checker class, ignored.')
			except NotImplementedError:
				print(f'Module {checker.get_name()} doesn\'t implement a necessary function from the Checker class, ignored.')
		return False