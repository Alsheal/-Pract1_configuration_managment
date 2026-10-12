import os
import socket
import sys
import tkinter as tk
from tkinter import scrolledtext

from config import parse_arguments
from emulator import ShellEmulator
from startup import execute_startup_script


class ShellGUI:
    def __init__(self, root, config):
        self.root = root
        self.config = config
        self.emulator = ShellEmulator()
        self.closed = False

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
            f"Путь VFS: {self.config['vfs_path']}\n"
        )

        if self.config["script_path"]:
            self.write_output(
                f"Стартовый скрипт: "
                f"{self.config['script_path']}\n"
            )

        self.write_output(
            "Доступные команды: ls, cd, exit.\n\n"
        )
        self.write_prompt()

        # Запускаем скрипт после создания окна.
        if self.config["script_path"]:
            self.root.after(100, self.run_startup_script)

    @staticmethod
    def get_username():
        try:
            return os.getlogin()
        except OSError:
            return (
                os.environ.get("USERNAME")
                or os.environ.get("USER")
                or "unknown"
            )

    def create_widgets(self):
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

        input_frame = tk.Frame(self.root)
        input_frame.pack(
            fill=tk.X,
            padx=10,
            pady=(5, 10)
        )

        self.command_entry = tk.Entry(
            input_frame,
            font=("Consolas", 11)
        )
        self.command_entry.pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=True
        )

        self.execute_button = tk.Button(
            input_frame,
            text="Enter",
            command=self.execute_command
        )
        self.execute_button.pack(
            side=tk.RIGHT,
            padx=(5, 0)
        )

        self.command_entry.bind(
            "<Return>",
            self.execute_command
        )
        self.command_entry.focus_set()

    def write_output(self, text):
        self.output.config(state=tk.NORMAL)
        self.output.insert(tk.END, text)
        self.output.config(state=tk.DISABLED)
        self.output.see(tk.END)

    def write_prompt(self):
        self.write_output("$ ")

    def show_dialog(self, command, output):
        """Показывает команду и результат в окне."""

        self.write_output(command + "\n")

        if output:
            self.write_output(output + "\n")

        self.write_prompt()

    def run_startup_script(self):
        script_path = self.config["script_path"]

        try:
            should_exit = execute_startup_script(
                script_path,
                self.emulator,
                self.show_dialog
            )
        except (OSError, UnicodeError) as error:
            self.write_output(
                f"\nОшибка стартового скрипта: {error}\n"
            )
            return

        if should_exit:
            self.close()

    def execute_command(self, event=None):
        command_line = self.command_entry.get()
        self.command_entry.delete(0, tk.END)

        if not command_line.strip():
            self.write_output("\n$ ")
            return "break"

        output, should_exit = self.emulator.execute(command_line)
        self.show_dialog(command_line, output)

        if should_exit:
            self.close()

        return "break"

    def close(self):
        if not self.closed:
            self.closed = True
            self.root.destroy()


def main():
    config = parse_arguments()

    # Диагностика параметров выводится в консоль.
    print("=== Параметры запуска эмулятора ===")
    print(f"VFS path: {config['vfs_path']}")
    print(f"Startup script: {config['script_path']}")
    print(f"Python executable: {sys.executable}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Username: {ShellGUI.get_username()}")
    print(f"Hostname: {socket.gethostname()}")
    print("===================================")

    root = tk.Tk()
    ShellGUI(root, config)
    root.mainloop()


if __name__ == "__main__":
    main()