import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from datetime import datetime

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.data = []

        # Создание формы
        self.create_form()

        # Создание таблицы
        self.create_table()

        # Построение фильтров
        self.create_filters()

        # Создание кнопок
        self.create_buttons()

    def create_form(self):
        frame = ttk.Frame(self.root)
        frame.pack(pady=10)

        ttk.Label(frame, text="Дата (YYYY-MM-DD):").grid(row=0, column=0)
        self.date_entry = ttk.Entry(frame)
        self.date_entry.grid(row=0, column=1)

        ttk.Label(frame, text="Тип тренировки:").grid(row=0, column=2)
        self.type_entry = ttk.Entry(frame)
        self.type_entry.grid(row=0, column=3)

        ttk.Label(frame, text="Длительность (мин):").grid(row=0, column=4)
        self.duration_entry = ttk.Entry(frame)
        self.duration_entry.grid(row=0, column=5)

    def create_table(self):
        columns = ("date", "type", "duration")
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        self.tree.heading("date", text="Дата")
        self.tree.heading("type", text="Тип тренировки")
        self.tree.heading("duration", text="Длительность")
        self.tree.pack(pady=10)

    def create_filters(self):
        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(pady=5)

        ttk.Label(filter_frame, text="Фильтр по типу:").grid(row=0, column=0)
        self.filter_type = ttk.Combobox(filter_frame, values=["Все"])
        self.filter_type.current(0)
        self.filter_type.grid(row=0, column=1)

        ttk.Label(filter_frame, text="Фильтр по дате (YYYY-MM-DD):").grid(row=0, column=2)
        self.filter_date_entry = ttk.Entry(filter_frame)
        self.filter_date_entry.grid(row=0, column=3)

        ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter).grid(row=0, column=4)
        ttk.Button(filter_frame, text="Сбросить фильтр", command=self.reset_filter).grid(row=0, column=5)

    def create_buttons(self):
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Добавить тренировку", command=self.add_training).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Сохранить в JSON", command=self.save_json).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Загрузить из JSON", command=self.load_json).pack(side=tk.LEFT, padx=5)

    def validate_input(self):
        date_str = self.date_entry.get()
        t_type = self.type_entry.get()
        duration_str = self.duration_entry.get()

        # Проверка даты
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный формат даты.")
            return False

        # Проверка типа тренировки
        if not t_type:
            messagebox.showerror("Ошибка", "Введите тип тренировки.")
            return False

        # Проверка длительности
        if not duration_str.isdigit():
            messagebox.showerror("Ошибка", "Длительность должна быть числом.")
            return False

        return True

    def add_training(self):
        if not self.validate_input():
            return

        entry = {
            "date": self.date_entry.get(),
            "type": self.type_entry.get(),
            "duration": int(self.duration_entry.get())
        }
        self.data.append(entry)
        self.update_table()
        # Очистить поля
        self.date_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)

    def update_table(self, filtered_data=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        data_to_show = filtered_data if filtered_data is not None else self.data
        for item in data_to_show:
            self.tree.insert('', tk.END, values=(item["date"], item["type"], item["duration"]))

    def apply_filter(self):
        filter_type = self.filter_type.get()
        filter_date = self.filter_date_entry.get()

        filtered = self.data
        if filter_type != "Все":
            filtered = [d for d in filtered if d["type"] == filter_type]
        if filter_date:
            try:
                datetime.strptime(filter_date, "%Y-%m-%d")
                filtered = [d for d in filtered if d["date"] == filter_date]
            except ValueError:
                messagebox.showerror("Ошибка", "Некорректный формат даты фильтра.")
                return
        self.update_table(filtered)

    def reset_filter(self):
        self.filter_type.set("Все")
        self.filter_date_entry.delete(0, tk.END)
        self.update_table()

    def save_json(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json")
        if filename:
            with open(filename, 'w') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Успех", "Данные сохранены.")

    def load_json(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, 'r') as f:
                self.data = json.load(f)
            self.update_table()

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
