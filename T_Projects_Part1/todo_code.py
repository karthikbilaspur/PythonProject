import tkinter as tk
from tkinter import messagebox

class ToDoList:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("To-Do List App")
        self.tasks: list[dict[str, object]] = []

        # Create task entry field
        self.task_entry = tk.Entry(root, width=40)
        self.task_entry.pack(padx=10, pady=10)

        # Create buttons
        button_frame = tk.Frame(root)
        button_frame.pack(padx=10, pady=10)
        tk.Button(button_frame, text="Add Task", command=self.add_task).pack(side=tk.LEFT)
        tk.Button(button_frame, text="Delete Task", command=self.delete_task).pack(side=tk.LEFT)
        tk.Button(button_frame, text="Mark as Done", command=self.mark_as_done).pack(side=tk.LEFT)
        tk.Button(button_frame, text="Clear All", command=self.clear_tasks).pack(side=tk.LEFT)

        # Create task list
        self.task_list = tk.Listbox(root, width=40)
        self.task_list.pack(padx=10, pady=10)

    def add_task(self) -> None:
        task = self.task_entry.get()
        if task:
            self.tasks.append({"task": task, "done": False})
            self.task_list.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def delete_task(self):
        try:
            task_index = self.task_list.curselection()[0]
            self.task_list.delete(task_index)
            self.tasks.pop(task_index)
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to delete.")

    def mark_as_done(self):
        try:
            task_index = self.task_list.curselection()[0]
            task = self.tasks[task_index]
            task["done"] = not task["done"]
            if task["done"]:
                self.task_list.itemconfig(task_index, fg="green")
            else:
                self.task_list.itemconfig(task_index, fg="black")
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to mark as done.")

    def clear_tasks(self):
        self.task_list.delete(0, tk.END)
        self.tasks.clear()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoList(root)
    root.mainloop()