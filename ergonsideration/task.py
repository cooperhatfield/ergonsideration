import multiprocessing

from ergonsideration.checker import Checker
import ergonsideration.calendar as calendar
import ergonsideration.notify as notify

class Task:
	''' A task is an object representing a specific action (theoretically an ergonomic reminder),
	such as 'get up to stretch every hour'. A task object will contain the relevant checkers, the
	configuration for when to run the task, and the configuration for the task's notification.
	'''
	def __init__(self, notification_config, schedule_config, checkers, name):
		self.notification_config = notification_config
		self.schedule_config = schedule_config
		self.checkers = checkers
		self.name = name

	def run_task(self):
		''' Check if the user is busy. If not, then send a notification.
		TODO:
		- add logic for buttons on the notification
		- support for snoozing
		'''
		user_is_busy = self.is_busy()
		if not user_is_busy:
			notify.send_notification(self.notification_config)
			task_length = self.schedule_config.get('length', 0)
			# set up a notification to end the task, if configured
			if task_length > 0:
				calendar.register_task(task_length, self.schedule_end_notification)
		# check notification button press for snooze or what not
		delay = self.schedule_config['interval']
		calendar.register_task(delay, self.run_task)

	def schedule_end_notification(self):
		''' If configured, send a notification signaling the end of the task. This assumes the user
			isn't busy (if they were, the initial notification would have not been sent). Right now
			this simple appends some text onto the already set message, in the future maybe 
			specific ending messages can be configured.
			
			TODO:
			- configure ending messages
			'''
		end_config = {"visual_config":
						{
						"task_name": self.notification_config['visual_config']['task_name'],
						"title": self.notification_config['visual_config']['task_name'],
						"content": "Done!",
						"template": self.notification_config['visual_config']['task_name']
						},
					  "button_config":
						{"button_group": "default_Accept"}
					}

		notify.send_notification(end_config)

	def is_busy(self):
		''' Check with each registered checker to see if the user is busy. If a checker times out,
		isn't a proper instance of the `Checker` class, or doesn't implement all relevant 
		functions, then it is ignored.
		TODO:
		- optional behavior for ignoring, quitting, or assuming the user is busy when a checker
			times out
		'''
		busy = multiprocessing.Value('i', False)
		for checker in self.checkers:
			try:
				assert issubclass(type(checker), Checker)
				if not checker.is_running():
					pass
				else:
					#p = multiprocessing.Process(target=checker.get_busy_status, args=(busy,))
					#p.start()
					#p.join(checker.get_timeout_time())
					#if p.is_alive():
					checker.get_busy_status(busy)
					if False:
						print(f'Checker {checker.get_name()} timed out when getting busy status. ignored.')
						p.terminate()
					return bool(busy.value)
			except AssertionError:
				print(f'Module {checker.get_name()} is not a proper child of Checker class, ignored.')
			except NotImplementedError:
				print(f'Module {checker.get_name()} doesn\'t implement a necessary function from the Checker class, ignored.')
		return False