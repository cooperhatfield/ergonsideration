import glob
import importlib
import json

import calendar
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

def register_new_task(config_file):
	checker_config, notification_config, schedule_config = parse_config(config_file)
	checkers = []
	for checker in checker_config:
		checker_file = glob.glob(f'/Checkers/{checker}')
		checkers.append(dynamic_import(checker_file))

	task = Task(notification_config, schedule_config, checkers)

	# now register the task with the calendar


