import multiprocessing

from checker import Checker
from calendar import Calendar
import notify

class Task:
	def __init__(self, notification_config, schedule_config, checkers):
		self.notification_config = notification_config
		self.schedule_config = schedule_config
		self.checkers = checkers
		self.calendar = Calendar()

	def run_task(self):
		user_is_busy = self.is_busy()
		if not user_is_busy:
			notify.send_notification(self.notification_config)
		# check notification button press for snooze or what not
		delay = self.schedule_config['interval']
		self.calendar.register_task(delay, self.run_task)

	def is_busy(self):
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
						print(f'A module timed out when getting busy status. ignored.')
						p.terminate()
					elif busy:
						return True
			except AssertionError:
				print(f'A module is not a proper child of Checker class, ignored.')
			except NotImplementedError:
				print(f'A module doesn\'t implement a necessary function from the Checker class, ignored.')
	return False