from parser import parse_command
from commands import CommandHandler


class ShellEmulator:
    """
    Основная логика эмулятора.
    """

    def __init__(self):
        self.command_handler = CommandHandler()

    def execute(self, command_line):
        """
        Обрабатывает одну строку, введенную пользователем.

        Возвращает:
            output - текст результата
            should_exit - нужно ли закрыть приложение
        """

        command_line = command_line.strip()

        # Пустая команда ничего не делает
        if not command_line:
            return "", False

        try:
            args = parse_command(command_line)
        except ValueError as error:
            return str(error), False

        if not args:
            return "", False

        return self.command_handler.execute(args)
