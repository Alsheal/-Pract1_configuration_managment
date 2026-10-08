class CommandHandler:
    """
    Обработчик команд эмулятора.
    На этапе 1 ls и cd являются заглушками.
    """

    SUPPORTED_COMMANDS = {"ls", "cd", "exit"}

    def execute(self, args):
        """
        Выполняет команду.

        args:
            список, полученный от parser.py

        Возвращает:
            (результат, should_exit)
        """

        if not args:
            return "", False

        command = args[0]
        command_args = args[1:]

        if command == "ls":
            return self._ls(command_args), False

        if command == "cd":
            return self._cd(command_args), False

        if command == "exit":
            return "", True

        return f"Ошибка: неизвестная команда '{command}'", False

    def _ls(self, args):
        """
        Заглушка команды ls.
        """

        result = ["Команда: ls"]

        if args:
            result.append(f"Аргументы: {args}")
        else:
            result.append("Аргументы: []")

        return "\n".join(result)

    def _cd(self, args):
        """
        Заглушка команды cd.
        """

        result = ["Команда: cd"]

        if args:
            result.append(f"Аргументы: {args}")
        else:
            result.append("Аргументы: []")

        return "\n".join(result)
