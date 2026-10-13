
from vfs import VirtualFileSystem


class CommandHandler:
    """Обработчик команд виртуальной оболочки."""

    def __init__(self, vfs: VirtualFileSystem):
        self.vfs = vfs

    def execute(self, command, args):
        """Выполняет команду и возвращает (результат, завершить)."""

        try:
            if command == "ls":
                if len(args) > 1 or (args and args[0] != "-l"):
                    return "Ошибка: использование ls [-l]", False

                return self.vfs.list_dir(
                    long_format=bool(args)
                ), False

            if command == "pwd":
                if args:
                    return "Ошибка: pwd не принимает аргументы", False

                return self.vfs.get_current_path(), False

            if command == "cd":
                if len(args) > 1:
                    return "Ошибка: использование cd [каталог]", False

                path = args[0] if args else None
                result = self.vfs.change_dir(path)
                return f"Текущий каталог: {result}", False

            if command == "vfs-save":
                if len(args) != 1:
                    return "Ошибка: использование vfs-save <путь>", False

                try:
                    saved_path = self.vfs.save(args[0])
                    return f"VFS успешно сохранена: {saved_path}", False
                except (OSError, ValueError) as error:
                    return f"Ошибка сохранения VFS: {error}", False
                
            if command == "exit":
                if args:
                    return "Ошибка: exit не принимает аргументы", False

                return "Эмулятор завершён", True

            return f"Ошибка: неизвестная команда '{command}'", False

        except (OSError, ValueError) as error:
            return f"Ошибка: {error}", False
