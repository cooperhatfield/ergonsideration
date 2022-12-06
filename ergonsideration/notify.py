# from https://stackoverflow.com/questions/64230231/how-can-i-can-send-windows-10-notifications-with-python-that-has-a-button-on-the
import winsdk.windows.ui.notifications as notifications
import winsdk.windows.data.xml.dom as dom

default_Accept_Snooze = '''<actions>
						       <action
						           content="Start"
						           arguments="accept"
						           activationType="background"/>
						       <action
						           content="Snooze"
						           arguments="snooze"
						           activationType="background"/>
						   </actions>'''
default_Accept = '''<actions>
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
						  	'button_group': default_Accept_Snooze
						  }
						}

def send_notification(notification_config):
	''' Choose the right kind of notification to send. Currently only supports 
	Windows "Toast" notifications.
	TODO:
	- check OS and send other types of notifications
	'''
	send_win_toast_notification(notification_config)

def send_win_toast_notification(notification_config, *, clear_previous=True):
	''' from https://stackoverflow.com/questions/64230231/how-can-i-can-send-windows-10-notifications-with-python-that-has-a-button-on-the
	Create a windows 'Toast' notification with content from the `notification_config` dict, and display it.
	TODO:
	- add support for button results
	'''
	import sys

	nManager = notifications.ToastNotificationManager
	notifier = nManager.create_toast_notifier(sys.executable)

	match notification_config:
		case {'visual_config': {'task_name': task_name, 'title': task_title, 'content': task_content, 'template': task_template},
			  'button_config': {'button_group': task_buttons}}:
			pass
	match notification_config['button_config']['button_group']:
		case 'default_Accept_Snooze':
			task_buttons = default_Accept_Snooze
		case 'default_Accept':
			task_buttons = default_Accept
		case _:
			pass

	task_string = '''
	<toast duration="short">

        <visual>
            <binding template='ToastGeneric'>
                <text>{title}</text>
                <text>{content}</text>
            </binding>
        </visual>

        {buttons}

    </toast>'''.format(title=task_title, content=task_content, buttons=task_buttons)

	#convert notification to an XmlDocument
	xml_doc = dom.XmlDocument()
	xml_doc.load_xml(task_string)

	if clear_previous:
		#clear previous toasts
		history = nManager.get_history()
		history.clear(sys.executable)

	#display notification
	notifier.show(notifications.ToastNotification(xml_doc))