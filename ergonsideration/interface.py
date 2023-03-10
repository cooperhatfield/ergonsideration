import tkinter as tk
import threading

import ergonsideration.main as main

class Threader(threading.Thread):
    def __init__(self, tasks, *args, **kwargs):
        self.tasks = tasks
        threading.Thread.__init__(self, *args, **kwargs)
        self.daemon = True
        self.start()

    def run(self):
        main.setup_calendar_from_interface(self.tasks)

class TaskListEntry(tk.Frame):
    def __init__(self, master=None, content=None):
        tk.Frame.__init__(self, master, width=200, height=50)
        self.grid_propagate(0)
        self.grid(sticky=tk.W, rowspan=3, pady=1)

        self.enabled = tk.IntVar()
        self.createWidgets(content)

    def createWidgets(self, content):
        if content is None:
            content = {'text': 'defaultbutton', 'default_state': 0, 'task': None}

        # checkbox
        self.checkbox = tk.Checkbutton(self, borderwidth=10, variable=self.enabled)
        self.checkbox.grid(column=0, padx=10, pady=1)

        # text
        self.label = tk.Label(self, text=content['text'], anchor=tk.W, font=("TkDefaultFont", 10))
        self.label.grid(column=1, row=self.checkbox.grid_info()['row'], pady=1, padx=8)

        # set the entry's task object, to access later if it's enabled
        self.task = content['task']

        # set the checkbox's initial status
        if content['default_state'] == 1:
            self.checkbox.select()

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        # label
        self.task_label = tk.Label(self, text='Tasks', justify=tk.LEFT, anchor=tk.S, font=("TkDefaultFont", 15))
        self.task_label.grid(padx=10, pady=10, sticky=tk.S)

        # task frame
        self.checker_frame = tk.Frame(self, relief=tk.SUNKEN, height=400, width=200, borderwidth=1, bg='#cccccc')
        self.checker_frame.grid(padx=10, pady=20)
        self.checker_frame.grid_propagate(0)

        # read each config and make a list entry
        self.task_entries = []
        for task in main.get_tasks_from_configs():
            task_name = task.name
            content = {'text': task_name, 'default_state': 0, 'task': task}
            self.task_entries.append(TaskListEntry(self.checker_frame, content))

        
        # status label
        self.status_label = tk.Label(self, text='Waiting for configuration...', font=("TkDefaultFont", 10))
        self.status_label.grid(padx=20)

        # start button
        self.start_button = tk.Button(self, text='Start', command=self.start_schedule)
        self.start_button.grid(ipadx=20, padx=10, pady=10, column=0)

        # quit button
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(ipadx=10, pady=10, row=100)


    def start_schedule(self):
        tasks = [entry.task for entry in self.task_entries if entry.enabled.get() == 1]
        #main.setup_calendar_from_interface(tasks)

        # start new daemon thread with schedule
        self.schedule_thread = Threader(tasks, name='Ergonsideration-Schedule')

        # update status label
        self.status_label.configure(text='Running!')

app = Application()
app.master.title('Ergonsideration Configuration')
app.master.geometry('500x620')
app.mainloop()
