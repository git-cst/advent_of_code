from pathlib import Path

def get_data(file_path: Path):
    with open(str(file_path.absolute()), mode='r', encoding='utf-8') as file:
        data: str = file.read()
    return data