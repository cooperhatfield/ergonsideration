import glob
import importlib
import json

from ergonsideration.calendar import Calendar
from ergonsideration.task import Task
from ergonsideration.checker import Checker

def dynamic_import(py_path):
	''' from https://stackoverflow.com/questions/57878744/how-do-i-dynamically-import-all-py-files-from-a-given-directory-and-all-sub-di
	Load a python file given by filename `py_path` as a module. WARNING: this could be very 
	dangerous. Make sure you verify EVERY module is safe before using this!
	'''
	module_spec = importlib.util.spec_from_file_location(module_name, py_path)
	module = importlib.util.module_from_spec(module_spec)
	module_spec.loader.exec_module(module)
	
	activated_module = module()
	activated_module.set_name(py_path)
	return activated_module

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
	for checker in checker_config:
		checker_file = glob.glob(f'/Checkers/{checker}')
		checkers.append(dynamic_import(checker_file))
	task = Task(notification_config, schedule_config, checkers)
	return task

def setup_calendar():
	''' Basically the program entry point; this creates the scheduling calendar, loads tasks from
	all current configs, registers the tasks with the calendar, and runs it.
	'''
	calendar = Calendar()
	for config_file in glob.glob(f'/Task Config/*.txt'):
		print(f'loading file {config_file}')
		task = load_task(config_file)
		calendar.register_task(task)
	print(calendar.queue())
	calendar.run_schedule()




