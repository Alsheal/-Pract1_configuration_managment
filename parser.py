
import shlex


def parse_command(line):
    """Разбирает строку на команду и список аргументов."""
    try:
        parts = shlex.split(line, comments=False, posix=True)
    except ValueError as error:
        raise ValueError(
            f"Ошибка разбора команды: {error}"
        ) from error

    if not parts:
        return None, []

    return parts[0], parts[1:]


# Совместимость с кодом, который использует старое имя.
parse_command_line = parse_command
