import sys
import os

default_Accept_Snooze_Toast = '''<actions>
							        <action
							            content="Start"
							            arguments="accept"
							            activationType="background"/>
							        <action
							            content="Snooze"
							            arguments="snooze"
							            activationType="background"/>
							    </actions>'''
default_Accept_Toast = '''<actions>
					         <action
					             content="Accept"
					             arguments="accept"
					             activationType="background"/>
					     </actions>'''


notification_config_v1 = {'visual_config': {
							'task_name': 'example',
							'title': 'example Title',
							'content': 'example content',
							'template': 'toastGeneric'
							},
						  'button_config': {
						  	'button_group': default_Accept_Snooze_Toast
						  }
						}

def send_notification(notification_config):
	''' Choose the right kind of notification to send. Currently only supports Windows "Toast" 
		notifications.

	TODO:
	- send other types of notifications
	'''
	if sys.platform.startswith('win'):
		send_win_toast_notification(notification_config)
	elif sys.platform.startswith('darwin'):
		send_osx_notification(notification_config)
	elif sys.platform.startswith('linux'):
		raise RuntimeError(f"Notifications not supported on {sys.platform}.")
	else:
		raise RuntimeError(f"Notifications not supported on {sys.platform}.")

def send_osx_notification(notification_config, *, clear_previous=True):
	''' from https://stackoverflow.com/questions/17651017/python-post-osx-notification
		Create an OSX notification.

		TODO:
		- support button effects
		- support custom picture
		- support sound(?)
	'''
	text = notification_config['visual_config']['content']
	title = notification_config['visual_config']['title']
	timeout_time = notification_config['visual_config'].get('timeout_time', 5)
	if notification_config['button_config']['button_group'] == 'default_Accept_Snooze':
		buttons_text = '{"Snooze", "Accept"}'
	elif notification_config['button_config']['button_group'] == 'default_Accept':
		buttons_text = '{"Accept"}' 

	os.system(f'osascript -e \'display alert "{title}" message "{text}" buttons {buttons_text} giving up after {timeout_time}\'')


	''' from https://stackoverflow.com/questions/64230231/how-can-i-can-send-windows-10-notifications-with-python-that-has-a-button-on-the
def send_win_toast_notification(notification_config, *, clear_previous=True):
	Create a windows 'Toast' notification with content from the `notification_config` dict, and display it.
	TODO:
	- add support for button results
	'''
	import win10toast as wt
	toaster =  wt.ToastNotifier()

	match notification_config:
		case {'visual_config': {'task_name': task_name, 'title': task_title, 'content': task_content, 'template': task_template},
			  'button_config': buttons}:
			pass

	toaster.show_toast(task_title, task_content, duration=5, threaded=True)

	