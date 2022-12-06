# ergonsideration (Ergonomics + Consideration)
Schedule and status based ergonomics reminder. Designed to support python scripts to check if a program is running, and to check if the user is "busy" in that program and should not be disturbed.

Included is a simple "Checker" to see if the user's status is "Busy" or "Do Not Disturb" on Microsoft Teams. I'll publish other checkers I make in [checkerLibrary](https://github.com/cooperhatfield/checkerLibrary).

Due to the requirement of running arbitrary code in checkers, the library is designed to have a simple interface in task creation and checker objects, so that users can verify the legitimacy of shared tasks and checkers.

TODO:
- Create executable release to package modules and python 
- Flesh out notifications
  - Support for other OS's
  - Support for button responses
  - More program-specific customization to notifications
- Thread checker code with a timeout
- Tests

## Usage

The program can be run by calling the `ergonsideration.main.setup_calendar()` function. Doing so will load all config files in the "ergonsideration/ergonsideration/Task Configs/" folder as tasks. In the future I would like to migrate this to an executable, but for now, clone the repo and run it from the terminal.

Users can create custom "Tasks", which are configured to create a notification at a certain interval if the user is not busy. The user is considered "busy" or "available" based on scripts (called "Checkers") that check other programs for a status. For example, a user may configure a task which reminds them to look away from the screen every 20 minutes. For this task, they might add the "win_teams_status" checker, in which case the notification will not pop up if the user's is busy on Teams.

## Implementing New Tasks

Users wishing to create their own task should make a new text file in the "ergonsideration/ergonsideration/Task Configs/" folder. The file should contain JSON in the following format:

```json
{"name": "Example",
"schedule_config":
    {
    "interval": 1200,
    "length": 20
    },
"notification_config":
    {
    "visual_config":
        {
        "task_name": "Example Task",
        "title": "Title of Notification",
	"content": "Notification body text.",
        "template": "toastGeneric"
	"timeout_time": 5
        },
    "button_config":
        {"button_group": "default_Accept_Snooze"}
    },
"checker_config":
    {
    "checkers": ["win_teams_status.py"]
    }
}
```

- `name`: String, currently unused
- `schedule_config`: Dict containing properties relating to the schedule of the Task,
  - `interval`: Integer, the number of seconds between runs of the task. A value of 600 means the task will run every 10 minutes.
  - `length`: Integer, if this is greater than 0, a notification will be send after `length` seconds to mark the end of the task.
- `notification_config`: Dict containing properties of the task's notification,
  - `visual_config`: Dict containing properties of the notification's layout and text,
    - `task_name`: String, currently unused.
    - `title`: String, title to be displayed on the notification.
    - `content`: String, text content to display in the body of the notification.
    - `template`: String, only used on Windows, should be a string defined as a template [by Microsoft](https://learn.microsoft.com/en-us/previous-versions/windows/apps/hh779727(v=win.10)). Warning! Changing this is untested, doing so may not work...
    - `timeout_time`: Integer, only used on OSX, the number of seconds to display the alert before automatically closing.
  - `button_config`: Dict containing properties of the notifications buttons,
    - `button_group`: String, this should be either "default_Accept_Snooze" for the default "Accept" and "Snooze" buttons built in to ergonsideration, or "default_Accept" for just "Accept". On windows, you can supply [valid XML content](https://learn.microsoft.com/en-us/uwp/schemas/tiles/toastschema/element-action) describing the button actions, and on OSX you can supply a formatted list of buttons as described [here](https://developer.apple.com/library/archive/documentation/AppleScript/Conceptual/AppleScriptLangGuide/reference/ASLR_cmds.html#//apple_ref/doc/uid/TP40000983-CH216-SW11). Currently there is no way to actually link any functionality to buttons, though.
- `checker_config`: Dict containing properties of the checkers which this task will use,
  - `checkers`: List of names of checkers to use for this task.
  
## Implementing New Checkers

Users wishing to create their own checkers should make a new python module in the "ergonsideration/ergonsideration/Checkers/" folder. Inside this file you should define a new class which extends and implements the base `ergonsideration.Checker` class. The `Checker` class is as follows:

```python
class Checker:
	def set_name(self, name):
		self.name = name

	def get_name(self):
		return self.name

	def is_running(self) -> bool:
		raise NotImplementedError()

	def get_busy_status(self, busy):
		raise NotImplementedError()

	def get_timeout_time(self) -> int:
		return 10 #s
```

A specific checker class should implement the following:
- `is_running` should check if the relevant program is running on the user's computer. For example, a checker for Discord calls would return `False` if the Discord program is not running, and `True` otherwise.
- `get_busy_status` should check if the user is busy in the specific program. For the purpose of multiprocessing, this is achieved by passing a `multiprocessing.Value` variable called `busy`. The implementation should determine if the user is busy in the specific program, and assign `busy.value = True` or `busy.value = False` accordingly. For example, a checker for Discord calls would set `busy.value` to `True` if the user is currently in a call, and set it to `False` otherwise.
- `get_timeout_time` is optional to implement. This defines the amount of time to allow `is_busy` to run before cancelling it. Currently, this is not implemented.

An example implementation of a `Checker`, in this case to determine the user's status on Microsoft Teams:

```python
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
```
