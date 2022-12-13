import glob
import importlib
import json
import os

import ergonsideration.calendar as calendar
from ergonsideration.task import Task
from ergonsideration.checker import Checker

package_directory = os.path.dirname(os.path.abspath(__file__))

def dynamic_import(checker_name, py_path):
	''' from https://stackoverflow.com/questions/57878744/how-do-i-dynamically-import-all-py-files-from-a-given-directory-and-all-sub-di
	Load a python file given by filename `py_path` as a module. WARNING: this could be very 
	dangerous. Make sure you verify EVERY module is safe before using this!
	'''
	module_spec = importlib.util.spec_from_file_location(checker_name, py_path)
	module = importlib.util.module_from_spec(module_spec)
	module_spec.loader.exec_module(module)
	
	expected_attributes = ['Checker', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__']
	class_name = [attr for attr in dir(module) if attr not in expected_attributes][0]
	active_module = getattr(module, class_name)
	checker = active_module()
	checker.set_name(checker_name)
	return checker

def parse_config(config_file):
	''' Parse a config file defining an task. The structure of the file is defined elsewhere, but
	it describes the notification content, schedule settings, and relevant checker modules for the
	given task.
	'''
	filepath = config_file
	with open(filepath) as file:
		config_data = json.load(file)
	checker_config, notification_config, schedule_config = config_data['checker_config'], config_data['notification_config'], config_data['schedule_config']
	return checker_config, notification_config, schedule_config

def load_task(config_file):
	''' Load a task from its config file, create the object, and set up the relevant checkers.
	'''
	checker_config, notification_config, schedule_config = parse_config(config_file)
	checkers = []
	for checker_name in checker_config['checkers']:
		checker_file = package_directory + f'\\Checkers\\{checker_name}'
		if not os.path.isfile(checker_file):
			print(f'Checker {checker_name} not found, ignoring.')
		else:
			checkers.append(dynamic_import(checker_name, checker_file))
	task = Task(notification_config, schedule_config, checkers)
	return task

def setup_calendar():
	''' Basically the program entry point; this creates the scheduling calendar, loads tasks from
	all current configs, registers the tasks with the calendar, and runs it.
	'''
	for config_file in glob.glob(os.path.join(package_directory, 'Task Configs', '*.txt')):
		print(f'Loading file {config_file[len(package_directory) + 14:]}')
		task = load_task(config_file)
		task_action = task.run_task
		task_delay = task.schedule_config['interval']
		calendar.register_task(task_delay, task_action)
	calendar.run_schedule()




