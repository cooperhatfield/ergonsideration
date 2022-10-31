# from https://stackoverflow.com/questions/64230231/how-can-i-can-send-windows-10-notifications-with-python-that-has-a-button-on-the
import winsdk.windows.ui.notifications as notifications
import winsdk.windows.data.xml.dom as dom

def send_win_notification():
	#create notifier
	nManager = notifications.ToastNotificationManager
	notifier = nManager.create_toast_notifier();

	#define your notification as string
	tString = """
	<toast>
	    <visual>
	        <binding template='ToastGeneric'>
	            <text>Sample toast</text>
	            <text>Sample content</text>
	        </binding>
	    </visual>
	</toast>
	"""

	#convert notification to an XmlDocument
	xDoc = dom.XmlDocument()
	xDoc.load_xml(tString)

	#display notification
	notifier.show(notifications.ToastNotification(xDoc))