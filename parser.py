import shlex


def parse_command(command_line):
    """
    Разбирает строку команды с учетом кавычек.

    Пример:
        cd "my folder"
    Результат:
        ["cd", "my folder"]
    """

    try:
        return shlex.split(command_line)
    except ValueError as error:
        raise ValueError(f"Ошибка разбора команды: {error}")
