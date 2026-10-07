import json
import os


def get_path_fun(table_name: str) -> str:
    """
    Функция возвращает путь к файлу в
    директории data с именем table_name
    """
    try:
        current = os.getcwd()
        while True:
            if os.path.isdir(os.path.join(current, "data")):
                project_root = current
                break
            parent = os.path.dirname(current)
            if parent == current:
                project_root = current
                break
            current = parent
        return os.path.join(project_root, "data", table_name)
    except TypeError:
        print("Ошибка: Неверный тип данных.")

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

def load_table_data(table_name: str) -> dict:
    """
    Загрузка данных из таблицы table_name
    """
    try:
        with open(get_path_fun(table_name+".json"), encoding="utf-8") as json_file:
            return json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError, PermissionError):
        return []

def save_table_data(table_name: str,
                    data: list[dict]) -> None:
    """
    Сохранения данных data в таблицу table_name
    """
    try:
        with open(get_path_fun(table_name+".json"), "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=2)
    except PermissionError:
        print("Ошибка: запрет на запись")
    except FileNotFoundError:
        print("Ошибка: файл не найден")
    except TypeError as e:
        print(f"Ошибка: данные нельзя сохранить в JSON: {e}")
def delete_file_from_data(table_name: str) -> None:
    """
    Удаление файла таблицы из директории data
    """
    try:
        os.remove(get_path_fun(table_name+".json"))
    except PermissionError:
        print(f"Ошибка: нет прав на удаление файла {table_name}")
    except FileNotFoundError:
        pass
def create_file_in_data(table_name: str) -> None:
    """
    Создание пустого файла таблицы в
    директории data при создании
    """
    try:
        # Проверяем наличие директории, если нет создаем
        os.makedirs(os.path.dirname(get_path_fun(table_name)), exist_ok=True)
        # создаем пустой файл таблицы в директории
        with open(get_path_fun(table_name+".json"), "x", encoding="utf-8"):
            pass
    except FileExistsError:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
    except PermissionError:
        print(f"Ошибка: нет прав на создание файла {table_name}")
    except FileNotFoundError:
        print(f"Ошибка: не удалось создать файл {table_name}")