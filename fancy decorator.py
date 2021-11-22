from pathlib import Path
from typing import Optional


def add_file_prefix(path: str, file_name: Optional[str] = '') -> Path:
    return Path('OK/' + path + file_name)

print(add_file_prefix('LOVE', file_name='HI'))
