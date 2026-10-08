import os
import socket
import tkinter as tk
from tkinter import scrolledtext

from emulator import ShellEmulator


class ShellGUI:
    def __init__(self, root):
        self.root = root
        self.emulator = ShellEmulator()

        self.username = self.get_username()
        self.hostname = socket.gethostname()

        self.root.title(
            f"Эмулятор - [{self.username}@{self.hostname}]"
        )

        self.root.geometry("800x500")
        self.root.minsize(600, 400)

        self.create_widgets()

        self.write_output(
            f"Эмулятор запущен: {self.username}@{self.hostname}\n"
        )
        self.write_output(
            "Введите команду. Доступные команды: ls, cd, exit.\n\n"
        )

        self.write_prompt()

    @staticmethod
    def get_username():
        """
        Получает имя текущего пользователя ОС.
        """

        try:
            return os.getlogin()
        except OSError:
            # Запасной вариант для некоторых сред Windows/Linux
            return (
                os.environ.get("USERNAME")
                or os.environ.get("USER")
                or "unknown"
            )

    def create_widgets(self):
        """
        Создает элементы графического интерфейса.
        """

        # Область вывода
        self.output = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=("Consolas", 11)
        )

        self.output.pack(
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=(10, 5)
        )

        # Нижняя панель
        input_frame = tk.Frame(self.root)
        input_frame.pack(
            fill=tk.X,
            padx=10,
            pady=(5, 10)
        )

        # Строка ввода
        self.command_entry = tk.Entry(
            input_frame,
            font=("Consolas", 11)
        )

        self.command_entry.pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=True
        )

        # Кнопка выполнения
        self.execute_button = tk.Button(
            input_frame,
            text="Enter",
            command=self.execute_command
        )

        self.execute_button.pack(
            side=tk.RIGHT,
            padx=(5, 0)
        )

        # Enter на клавиатуре
        self.command_entry.bind(
            "<Return>",
            self.execute_command
        )

        # Устанавливаем курсор в поле ввода
        self.command_entry.focus_set()

    def write_output(self, text):
        """
        Выводит текст в область терминала.
        """

        self.output.config(state=tk.NORMAL)
        self.output.insert(tk.END, text)
        self.output.config(state=tk.DISABLED)

        self.output.see(tk.END)

    def write_prompt(self):
        """
        Показывает приглашение командной строки.
        """

        self.write_output("$ ")

    def execute_command(self, event=None):
        """
        Выполняет введенную пользователем команду.
        """

        command_line = self.command_entry.get()

        # Очищаем поле ввода
        self.command_entry.delete(0, tk.END)

        # Если введена пустая строка
        if not command_line.strip():
            self.write_output("\n$ ")
            return "break"

        # Показываем введенную команду
        self.write_output(command_line + "\n")

        # Выполняем команду
        output, should_exit = self.emulator.execute(command_line)

        # Показываем результат
        if output:
            self.write_output(output + "\n")

        # Если команда exit
        if should_exit:
            self.root.destroy()
            return "break"

        # Новое приглашение
        self.write_prompt()

        return "break"


def main():
    root = tk.Tk()

    ShellGUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()
