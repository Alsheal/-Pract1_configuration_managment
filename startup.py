def run_startup_script(script_path, execute_line, write_output):
    """Выполняет команды из стартового скрипта."""

    if not script_path:
        return False

    try:
        with open(script_path, "r", encoding="utf-8-sig") as file:
            lines = file.readlines()
    except (OSError, UnicodeError) as error:
        write_output(f"Ошибка чтения стартового скрипта: {error}")
        return False

    write_output(f"Запуск скрипта: {script_path}")
    write_output("")

    for raw_line in lines:
        line = raw_line.strip()

        if not line or line.startswith("#"):
            continue

        if execute_line(line):
            return True

    return False