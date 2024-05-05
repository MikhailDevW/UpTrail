import sys
from pathlib import Path


BACKEND_DIR = Path(__file__).parent.parent.resolve()
sys.path.append(BACKEND_DIR)
BACKEND_DIR_NAME = "src"
FILENAME = "main.py"


if not (BACKEND_DIR / BACKEND_DIR_NAME).is_dir():
    assert False, (
        f"В директории `{BACKEND_DIR}` не найдена папка c проектом "
        f"`{BACKEND_DIR_NAME}`. Убедитесь, что у вас верная структура проекта."
    )


if not (BACKEND_DIR / BACKEND_DIR_NAME / FILENAME).is_file():
    assert False, (
        f"В директории `{BACKEND_DIR}` не найден файл `{FILENAME}`. "
        f"Убедитесь, что у вас верная структура проекта."
    )
