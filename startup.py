from pathlib import Path


def read_startup_script(script_path):
    """Читает команды из стартового скрипта."""

    path = Path(script_path)

    if not path.is_file():
        raise FileNotFoundError(
            f"Стартовый скрипт не найден: {path}"
        )

    # utf-8-sig позволяет прочитать и файлы с BOM.
    with path.open("r", encoding="utf-8-sig") as file:
        return file.readlines()


def execute_startup_script(script_path, emulator, show_dialog):
    """
    Выполняет команды из скрипта последовательно.

    show_dialog(command, output) отвечает за отображение
    команды и её результата в GUI.
    """

    lines = read_startup_script(script_path)

    for line_number, line in enumerate(lines, start=1):
        command = line.strip()

        # Пустые строки и комментарии пропускаем.
        if not command or command.startswith("#"):
            continue

        output, should_exit = emulator.execute(command)

        show_dialog(command, output)

        if should_exit:
            return True

    return False