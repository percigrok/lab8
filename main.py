import tkinter as tk
from tkinter import messagebox


class TaskError(Exception):
    """Базовое исключение для задач."""
    pass

class EmptyTaskError(TaskError):
    """Исключение для пустой задачи."""
    def __init__(self):
        super().__init__("Задача не может быть пустой.")

# class задачи 
class Task:
    def __init__(self, title):
        if not title.strip():
            raise EmptyTaskError()
        self.title = title
        self.status = "To Do"

    def change_status(self, new_status):
        self.status = new_status

# gui
class KanbanApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Канбан-доска")

        self.tasks = []

        self.entry = tk.Entry(master, width=40)
        self.entry.pack(pady=5)

        self.add_button = tk.Button(master, text="Добавить задачу", command=self.add_task)
        self.add_button.pack()

        self.columns = {
            "To Do": tk.Listbox(master, width=30, height=10),
            "In Progress": tk.Listbox(master, width=30, height=10),
            "Done": tk.Listbox(master, width=30, height=10),
        }

        self.column_frames = {}

      # колонки
        frame = tk.Frame(master)
        frame.pack(pady=10)

        for i, (status, listbox) in enumerate(self.columns.items()):
            col_frame = tk.Frame(frame)
            col_frame.grid(row=0, column=i, padx=10)
            self.column_frames[status] = col_frame

            tk.Label(col_frame, text=status).pack()
            listbox.pack()
            tk.Button(col_frame, text="Изменить статус", command=lambda s=status: self.change_task_status(s)).pack(pady=5)

    def add_task(self):
        try:
            title = self.entry.get()
            task = Task(title)
            self.tasks.append(task)
            self.columns["To Do"].insert(tk.END, task.title)
            self.entry.delete(0, tk.END)
        except EmptyTaskError as e:
            messagebox.showerror("Ошибка", str(e))

    def change_task_status(self, current_status):
        listbox = self.columns[current_status]
        selection = listbox.curselection()

        if not selection:
            return

        index = selection[0]
        task_title = listbox.get(index)
        listbox.delete(index)

        # поиск задачи 
        task = next((t for t in self.tasks if t.title == task_title and t.status == current_status), None)

        if task:
            if current_status == "To Do":
                new_status = "In Progress"
            elif current_status == "In Progress":
                new_status = "Done"
            else:
                new_status = "To Do"

            task.change_status(new_status)
            self.columns[new_status].insert(tk.END, task.title)

if __name__ == "__main__":
    root = tk.Tk()
    app = KanbanApp(root)
    root.mainloop()
