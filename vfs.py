
from pathlib import Path
import shutil


class VirtualFileSystem:
    """Виртуальная файловая система с хранением данных в памяти."""

    def __init__(self, root_path):
        self.root = Path(root_path).expanduser().resolve()

        if not self.root.exists():
            raise FileNotFoundError(
                f"Каталог VFS не существует: {self.root}"
            )

        if not self.root.is_dir():
            raise NotADirectoryError(
                f"Путь VFS не является каталогом: {self.root}"
            )

        self.directories = {"/"}
        self.files = {}
        self.current_path = "/"

        self._load_directory(self.root, "/")

    def _load_directory(self, disk_path, virtual_path):
        """Загружает каталоги и файлы в память."""

        for item in sorted(
            disk_path.iterdir(),
            key=lambda p: p.name.lower()
        ):
            if item.is_symlink():
                continue

            virtual_item = (
                virtual_path.rstrip("/") + "/" + item.name
            )

            if item.is_dir():
                self.directories.add(virtual_item)
                self._load_directory(item, virtual_item)

            elif item.is_file():
                self.files[virtual_item] = item.read_bytes()

    def _resolve_path(self, path="."):
        """Возвращает нормализованный виртуальный абсолютный путь."""

        path = str(path)

        if path.startswith("/"):
            parts = []
        else:
            parts = [
                part
                for part in self.current_path.split("/")
                if part
            ]

        for part in path.split("/"):
            if part in ("", "."):
                continue

            if part == "..":
                if not parts:
                    raise PermissionError(
                        "Доступ за пределами VFS запрещён"
                    )
                parts.pop()
            else:
                parts.append(part)

        return "/" + "/".join(parts) if parts else "/"

    def get_virtual_path(self):
        """Возвращает текущий виртуальный путь."""
        return self.current_path

    def get_current_path(self):
        """Возвращает текущий виртуальный путь."""
        return self.current_path

    def change_dir(self, path=None):
        """Изменяет текущий виртуальный каталог."""

        if path is None:
            self.current_path = "/"
            return self.current_path

        target = self._resolve_path(path)

        if target not in self.directories:
            if target in self.files:
                raise NotADirectoryError(
                    f"Это не каталог: {path}"
                )

            raise FileNotFoundError(
                f"Каталог не найден: {path}"
            )

        self.current_path = target
        return self.current_path

    def list_dir(self, long_format=False):
        """Показывает содержимое текущего виртуального каталога."""

        prefix = (
            "/"
            if self.current_path == "/"
            else self.current_path + "/"
        )

        entries = {}

        for directory in self.directories:
            if directory == self.current_path:
                continue

            if not directory.startswith(prefix):
                continue

            name = directory[len(prefix):]

            if "/" not in name:
                entries[name] = ("d", directory)

        for file_path in self.files:
            if not file_path.startswith(prefix):
                continue

            name = file_path[len(prefix):]

            if "/" not in name:
                entries[name] = ("f", file_path)

        if not entries:
            return "Каталог пуст"

        result = []

        for name in sorted(entries, key=str.lower):
            kind, path = entries[name]

            if long_format:
                size = (
                    0
                    if kind == "d"
                    else len(self.files[path])
                )

                marker = "d" if kind == "d" else "-"
                result.append(
                    f"{marker} {size:>8}  {name}"
                )
            else:
                result.append(name)

        return "\n".join(result)

    def save(self, destination):
        """Сохраняет снимок VFS из памяти в новый каталог."""

        destination = Path(destination).expanduser()

        if not destination.is_absolute():
            destination = Path.cwd() / destination

        destination = destination.resolve()

        # Запрещаем сохранять VFS поверх исходных данных
        # или внутрь исходного каталога.
        if (
            destination == self.root
            or self.root in destination.parents
        ):
            raise ValueError(
                "Нельзя сохранять VFS внутрь исходного каталога"
            )

        # Не перезаписываем существующий каталог.
        if destination.exists():
            raise FileExistsError(
                f"Каталог назначения уже существует: {destination}"
            )

        if not destination.parent.is_dir():
            raise FileNotFoundError(
                "Родительский каталог не существует: "
                f"{destination.parent}"
            )

        try:
            destination.mkdir()

            # Создаём каталоги из виртуальной файловой системы.
            for directory in sorted(
                self.directories,
                key=lambda item: item.count("/")
            ):
                if directory == "/":
                    continue

                target = destination / directory.lstrip("/")
                target.mkdir(parents=True, exist_ok=True)

            # Записываем содержимое файлов из памяти.
            for virtual_path, content in self.files.items():
                target = destination / virtual_path.lstrip("/")
                target.parent.mkdir(
                    parents=True,
                    exist_ok=True
                )
                target.write_bytes(content)

        except Exception:
            # Удаляем неполную копию при ошибке сохранения.
            if destination.exists():
                shutil.rmtree(destination)
            raise

        return str(destination)
