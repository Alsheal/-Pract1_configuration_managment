import os
import socket
import sys
import tkinter as tk
from tkinter import scrolledtext

from config import parse_arguments
from emulator import ShellEmulator
from startup import run_startup_script as execute_startup_script


class ShellGUI:
    def __init__(self, root, config):
        self.root = root
        self.config = config
        self.emulator = ShellEmulator(config["vfs_path"])
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

        script_path = self.config.get("script_path")
        if script_path:
            self.write_output(f"Стартовый скрипт: {script_path}\n")

        self.write_output(
            "Доступные команды: ls, ls -l, pwd, cd, vfs-save, exit.\n"
        )
        self.write_prompt()

        if script_path:
            self.root.after(100, self.execute_startup_script)

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

        self.command_entry.bind("<Return>", self.execute_command)
        self.command_entry.focus_set()

    def write_output(self, text):
        if self.closed:
            return

        self.output.config(state=tk.NORMAL)
        self.output.insert(tk.END, str(text))
        self.output.config(state=tk.DISABLED)
        self.output.see(tk.END)

    def write_prompt(self):
        if not self.closed:
            self.write_output("$ ")

    def show_command_result(self, command, output):
        self.write_output(command + "\n")

        if output:
            self.write_output(str(output) + "\n")

        self.write_prompt()

    def execute_startup_script(self):
        """Выполняет команды из стартового скрипта."""

        script_path = self.config.get("script_path")
        if not script_path or self.closed:
            return

        def execute_line(command):
            if self.closed:
                return True

            output, should_exit = self.emulator.execute(command)
            self.show_command_result(command, output)
            return should_exit

        def write_script_output(message):
            self.write_output(str(message) + "\n")

        try:
            should_exit = execute_startup_script(
                script_path,
                execute_line,
                write_script_output
            )
        except (OSError, UnicodeError) as error:
            self.write_output(
                f"\nОшибка чтения стартового скрипта: {error}\n"
            )
            return
        except Exception as error:
            self.write_output(
                f"\nОшибка выполнения стартового скрипта: {error}\n"
            )
            return

        if should_exit:
            self.close()

    def execute_command(self, event=None):
        if self.closed:
            return "break"

        command = self.command_entry.get()
        self.command_entry.delete(0, tk.END)

        if not command.strip():
            self.write_prompt()
            return "break"

        output, should_exit = self.emulator.execute(command)
        self.show_command_result(command, output)

        if should_exit:
            self.close()

        return "break"

    def close(self):
        if not self.closed:
            self.closed = True
            self.root.destroy()


def main():
    config = parse_arguments()

    print("=== Параметры запуска эмулятора ===")
    print(f"VFS path: {config['vfs_path']}")
    print(f"Startup script: {config['script_path']}")
    print(f"Python executable: {sys.executable}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Username: {ShellGUI.get_username()}")
    print(f"Hostname: {socket.gethostname()}")

    root = tk.Tk()
    ShellGUI(root, config)
    root.mainloop()


if __name__ == "__main__":
    main()