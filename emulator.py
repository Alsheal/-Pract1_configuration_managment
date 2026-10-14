from parser import parse_command_line
from commands import CommandHandler
from vfs import VirtualFileSystem


class ShellEmulator:
    """Выполняет команды виртуальной оболочки без создания GUI."""

    def __init__(self, vfs_path="vfs"):
        self.vfs = VirtualFileSystem(vfs_path)
        self.command_handler = CommandHandler(self.vfs)
        print("Класс VFS:", type(self.vfs))
        print("Метод save существует:", hasattr(self.vfs, "save"))
        print("Файл класса VFS:", __import__("inspect").getfile(type(self.vfs)))

    def execute(self, command_line):
        """Возвращает (результат, нужно_завершить_эмулятор)."""

        command_line = command_line.strip()

        if not command_line:
            return "", False

        try:
            command, args = parse_command_line(command_line)
        except ValueError as error:
            return str(error), False

        if command is None:
            return "", False

        return self.command_handler.execute(command, args)
