import argparse
from pathlib import Path


def parse_arguments():
    """Разбирает параметры командной строки."""

    parser = argparse.ArgumentParser(
        description="Графический эмулятор UNIX-подобной оболочки"
    )

    parser.add_argument(
        "--vfs",
        default="vfs",
        help="Путь к каталогу-источнику виртуальной файловой системы"
    )

    parser.add_argument(
        "--script",
        default=None,
        help="Путь к стартовому скрипту с командами"
    )

    args = parser.parse_args()

    # Относительные пути разрешаем от текущего каталога запуска.
    vfs_path = Path(args.vfs).expanduser().resolve()

    script_path = None
    if args.script:
        script_path = Path(args.script).expanduser().resolve()

    return {
        "vfs_path": vfs_path,
        "script_path": script_path,
    }
