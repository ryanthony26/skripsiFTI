
from pathlib import Path

def load_md(file_path: str) -> str:
    try:
        return Path(file_path).read_text(encoding="utf-8")
    except Exception as e:
        return f"Error Cek Kembali Nama File: {file_path}\n\nError: {e}"