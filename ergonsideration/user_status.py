import glob
import importlib
from checker import Checker

def dynamic_import(module_name, py_path):
	''' from https://stackoverflow.com/questions/57878744/how-do-i-dynamically-import-all-py-files-from-a-given-directory-and-all-sub-di
	'''
    module_spec = importlib.util.spec_from_file_location(module_name, py_path)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module

def get_registered_classes():
	files = glob.glob('/Checkers/*.py')
	names = [file[10:-3] for file in files]
	checker_modules = dynamic_import(names, files)
	return checker_modules, names

def is_busy(checker_modules, names):
	for checker_module, name in (checker_modules, names):
		try:
			checker = checker_module()
			assert issubclass(checker, Checker)
			if not checker.is_running():
				pass
			elif checker.get_busy_status():
				return True

		except AssertionError:
			print(f'Module "{name}" is not a proper child of Checker class, ignored.')
		except NotImplementedError:
			print(f'Module "{name}" doesn\'t implement a necessary function from the Checker class, ignored.')

	return False
