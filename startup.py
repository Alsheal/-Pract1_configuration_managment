
def run_startup_script(script_path, execute_line, write_output):
    """Выполняет команды из стартового скрипта."""

    if script_path is None:
        return False

    try:
        with open(script_path, "r", encoding="utf-8-sig") as file:
            lines = file.readlines()
    except OSError as error:
        write_output(f"Ошибка чтения стартового скрипта: {error}")
        write_output("")
        return False

    write_output(f"Запуск скрипта: {script_path}")
    write_output("")

    for raw_line in lines:
        line = raw_line.strip()

        if not line or line.startswith("#"):
            continue

        should_exit = execute_line(line)

        if should_exit:
            return True

    return False
