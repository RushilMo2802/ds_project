import sqlite3
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from datetime import datetime
from kivy.utils import platform

# Set window size for desktop testing
Window.size = (600, 720)

class Database:
    """Handles database operations for the ToDo app."""
    def __init__(self, db_name="todo.db"):
        self.connection = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        """Creates the tasks table if it doesn't exist."""
        with self.connection:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    due_date TEXT,
                    completed INTEGER DEFAULT 0  -- default value for completed
                )
            ''')

    def create_task(self, task, due_date):
        """Adds a new task to the database, setting completed to 0 by default."""
        with self.connection:
            cursor = self.connection.execute(
                "INSERT INTO tasks (task, due_date, completed) VALUES (?, ?, ?)", 
                (task, due_date, 0)  # Set completed to 0 by default
            )
            return cursor.lastrowid  # Return the ID of the newly created task

    def get_tasks(self):
        """Retrieves all tasks from the database."""
        with self.connection:
            cursor = self.connection.execute("SELECT * FROM tasks WHERE completed = 0")
            uncompleted_tasks = cursor.fetchall()
            cursor = self.connection.execute("SELECT * FROM tasks WHERE completed = 1")
            completed_tasks = cursor.fetchall()
            return completed_tasks, uncompleted_tasks

    def mark_task_as_complete(self, task_id):
        """Marks a task as completed."""
        with self.connection:
            self.connection.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
            return task_id

    def mark_task_as_incomplete(self, task_id):
        """Marks a task as incomplete."""
        with self.connection:
            self.connection.execute("UPDATE tasks SET completed = 0 WHERE id = ?", (task_id,))
            return task_id

    def delete_task(self, task_id):
        """Deletes a task from the database."""
        with self.connection:
            self.connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

class DialogContent(MDBoxLayout):
    """Opens a dialog box that gets the task from the user."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.date_text.text = str(datetime.now().strftime('%A %d %B %Y'))

    def show_date_picker(self):
        """Opens the date picker."""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        """Gets the date from the date picker."""
        date = value.strftime('%A %d %B %Y')
        self.ids.date_text.text = str(date)

class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    """Custom list item with a checkbox."""
    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        self.pk = pk

    def mark(self, check, the_list_item):
        """Mark the task as complete or incomplete."""
        if check.active:
            the_list_item.text = '[s]' + the_list_item.text + '[/s]'
            db.mark_task_as_complete(the_list_item.pk)
        else:
            the_list_item.text = str(db.mark_task_as_incomplete(the_list_item.pk))

    def delete_item(self, the_list_item):
        """Delete the task."""
        self.parent.remove_widget(the_list_item)
        db.delete_task(the_list_item.pk)

class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    """Custom left container for checkbox."""

class MainApp(MDApp):
    task_list_dialog = None

    def build(self):
        """Set the theme for the app."""
        self.theme_cls.primary_palette = "DeepPurple"

    def show_task_dialog(self):
        """Show the task creation dialog."""
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(
                title="Create Task",
                type="custom",
                content_cls=DialogContent(),
            )
        self.task_list_dialog.open()

    def on_start(self):
        """Load saved tasks into the UI when the app starts."""
        try:
            completed_tasks, uncompleted_tasks = db.get_tasks()
            for task in uncompleted_tasks:
                self.add_task_to_ui(task)

            for task in completed_tasks:
                task[1] = '[s]' + task[1] + '[/s]'
                self.add_task_to_ui(task, completed=True)
        except Exception as e:
            print(e)

    def add_task_to_ui(self, task, completed=False):
        """Add a task to the UI."""
        add_task = ListItemWithCheckbox(pk=task[0], text=task[1], secondary_text=task[2])
        if completed:
            add_task.ids.check.active = True
        self.root.ids.container.add_widget(add_task)

    def close_dialog(self, *args):
        """Close the task dialog."""
        self.task_list_dialog.dismiss()

    def add_task(self, task, task_date):
        """Add a task to the list of tasks."""
        created_task = db.create_task(task.text, task_date)
        self.add_task_to_ui((created_task, task.text, task_date))
        task.text = ''

if __name__ == '__main__':
    db = Database()  # Initialize the Database instance before the app
    app = MainApp()
    app.run()
