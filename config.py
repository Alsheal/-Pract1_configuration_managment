
import argparse
from pathlib import Path


def parse_config():
    parser = argparse.ArgumentParser(
        description="Эмулятор командной оболочки ОС"
    )

    parser.add_argument(
        "--vfs",
        default="vfs",
        help="Путь к исходному каталогу VFS (по умолчанию: vfs)"
    )

    parser.add_argument(
        "--script",
        default="script/startap.txt",
        help="Путь к стартовому скрипту"
    )

    args = parser.parse_args()

    return {
        "vfs_path": Path(args.vfs).expanduser().resolve(),
        "script_path": (
            Path(args.script).expanduser().resolve()
            if args.script else None
        ),
    }
