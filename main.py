import tkinter as tk
from tkinter import messagebox

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Менеджер задач")
        self.root.geometry("400x500")
        self.tasks = []

        # Поле ввода
        self.entry = tk.Entry(root, width=40)
        self.entry.pack(pady=10)

        # Кнопки
        btn_frame = tk.Frame(root)
        btn_frame.pack()
        tk.Button(btn_frame, text="Добавить", command=self.add_task).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Удалить", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Выполнено", command=self.toggle_task).pack(side=tk.LEFT, padx=5)

        # Фильтры
        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=10)
        self.filter_var = tk.StringVar(value="Все")
        for f in ["Все", "Активные", "Выполненные"]:
            tk.Radiobutton(filter_frame, text=f, variable=self.filter_var, value=f, command=self.update_list).pack(side=tk.LEFT)

        # Список задач
        self.listbox = tk.Listbox(root, width=50, height=15)
        self.listbox.pack(pady=10)

    def add_task(self):
        text = self.entry.get().strip()
        if text:
            self.tasks.append({"text": text, "done": False})
            self.entry.delete(0, tk.END)
            self.update_list()
        else:
            messagebox.showwarning("Ошибка", "Введите текст задачи!")

    def delete_task(self):
        try:
            idx = self.listbox.curselection()[0]
            # Учитываем фильтр при удалении
            visible_tasks = self.get_visible_tasks()
            task_to_remove = visible_tasks[idx]
            self.tasks.remove(task_to_remove)
            self.update_list()
        except IndexError:
            messagebox.showwarning("Ошибка", "Выберите задачу для удаления!")

    def toggle_task(self):
        try:
            idx = self.listbox.curselection()[0]
            visible_tasks = self.get_visible_tasks()
            task = visible_tasks[idx]
            task["done"] = not task["done"]
            self.update_list()
        except IndexError:
            messagebox.showwarning("Ошибка", "Выберите задачу!")

    def get_visible_tasks(self):
        f = self.filter_var.get()
        if f == "Все": return self.tasks
        if f == "Активные": return [t for t in self.tasks if not t["done"]]
        if f == "Выполненные": return [t for t in self.tasks if t["done"]]

    def update_list(self):
        self.listbox.delete(0, tk.END)
        for task in self.get_visible_tasks():
            status = "[x]" if task["done"] else "[ ]"
            self.listbox.insert(tk.END, f"{status} {task['text']}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()