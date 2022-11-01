import glob
import importlib
import json

from calendar import Calendar
from task import Task
from checker import Checker

def dynamic_import(py_path):
	''' from https://stackoverflow.com/questions/57878744/how-do-i-dynamically-import-all-py-files-from-a-given-directory-and-all-sub-di
	'''
    module_spec = importlib.util.spec_from_file_location(module_name, py_path)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    
    activated_module = module()
    activated_module.set_name(py_path)
    return activated_module

def parse_config(config_file):
	filepath = glob.glob(f'/Task Config/{config_file}')
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
		task = load_task(config_file)
		calendar.register_task(task)
	calendar.run_schedule()


	# now register the task with the calendar


