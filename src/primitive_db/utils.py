import json
import os


def load_metadata(filepath: str) -> dict:
    """
    Функция загружает метаданные из файла filepath
    если прочесть не получается возращает пустой словарь
    """
    try:
        with open(filepath, encoding="utf-8") as json_file:
            return json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError, PermissionError):
        return {}

def save_metadata(filepath: str,
                  data: dict) -> None:
    """
    Сохраняет переданные метаданные в файл filepath
    """

    try:
        with open(filepath, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=2)
    except PermissionError:
        print(f"Ошибка: нет прав на запись в {filepath}")
    except FileNotFoundError:
        print(f"Ошибка: директория не существует: {filepath}")
    except TypeError as e:
        print(f"Ошибка: данные нельзя сохранить в JSON: {e}")