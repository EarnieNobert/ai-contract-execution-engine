import os


def ensure_directory(path: str):
    os.makedirs(path, exist_ok=True)


def write_text_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)