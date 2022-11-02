from ergonsideration.checker import Checker

import psutil

import os

class WinTeamsStatus(Checker):
	def is_running(self) -> bool:
		return "Teams.exe" in (program.name() for program in psutil.process_iter(attrs=['name']))

	def get_busy_status(self, busy):
		''' Get busy status by checking the user's status in the logs
		'''
		log_path = os.getenv('APPDATA') + '\\Microsoft\\Teams\\logs.txt'
		status = ''
		with open(log_path, 'r') as log:
			for log_line in log:
				if 'StatusIndicatorStateService: Added' in log_line:
					status = log_line.split('StatusIndicatorStateService: Added ')[1].split(' (current state: ')[0]

		busy.value = status in ['Busy', 'DoNotDisturb']