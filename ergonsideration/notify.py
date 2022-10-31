# from https://stackoverflow.com/questions/64230231/how-can-i-can-send-windows-10-notifications-with-python-that-has-a-button-on-the
import winsdk.windows.ui.notifications as notifications
import winsdk.windows.data.xml.dom as dom

default_Accept_Snooze = f'<actions>\
						       <action\
						           content="Accept"\
						           imageUri="Assets/Icons/accept.png"\
						           arguments="accept"\
						           activationType="background"/>\
						       <action\
						           content="Snooze"\
						           imageUri="Assets/Icons/snooze.png"\
						           arguments="snooze"\
						           activationType="background"/>\
						   </actions>'

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
	'''Choose the right kind of notification to send. Currently only supports 
	Windows "Toast" notifications.
	'''
	send_win_toast_notification(notification_config)

def send_win_toast_notification(notification_config):
	#create notifier
	nManager = notifications.ToastNotificationManager
	notifier = nManager.create_toast_notifier();

	match notification_config:
		case {'visual_config': {'task_name': task_name, 'title': task_title, 'content': task_content, 'template': task_template},
			  'button_config': {'button_group': task_buttons}}:
			pass

	#define your notification as string
	visuals = f'\
	    <visual>\
	        <binding template=\'{task_template}\'>\
	            <text>{task_title}</text>\
	            <text>{task_content}</text>\
	        </binding>\
	    </visual>'
	
	buttons = task_buttons

	task_string = '<toast>' + visuals + buttons + '</toast>'

	#convert notification to an XmlDocument
	xml_doc = dom.XmlDocument()
	xml_doc.load_xml(task_string)

	#display notification
	notifier.show(notifications.ToastNotification(xml_doc))