from constants import ALLOWED_CHAR, REAL_TYPE, VALID_TYPES


def create_table(metadata: dict,
                 table_name:str,
                 columns:list[str]) -> dict | None:
    """
    Функция принимает текущие метаданные, имя таблицы и список столбцов.
    Делает проверку корректности данных и отсутствия такой таблицы,
    в случае успеха, обновляет словарь metadata и возвращает его.
    """
    try:
        if table_name in metadata:
            print(f'Ошибка: Таблица \"{table_name}\" уже существует.')
        else:
            # Проверяем что символы соответствуют допустимым
            if not all(ch in ALLOWED_CHAR for ch in table_name):
                print(f"Некорректное символы в имени таблицы: <{table_name}>.\n"
                      f"Допустимы только латинские буквы, цифры и подчеркивание.")
                return None

            if not columns:
                print("Некорректное значение: <>. Попробуйте снова.")
                return None
            # Объявляем словарь хранящий данные в формате <имя:тип>
            # и добавляем поле 'ID' с типом int
            dict_columns = {"ID": "int"}
            for column in columns:
                # Проверяем что разделение на имя:тип корректно
                if ":" not in column:
                    raise TypeError(f"Неверный формат колонки: \"{columns}\"")
                # разделяем на имя и тип
                name, dtype = column.split(":")
                # проверяем соответствие типа условию задания
                if dtype not in VALID_TYPES:
                    print(f"Некорректное значение: <{dtype.strip()}>. "
                         f"Попробуйте снова.")
                    return None
                dict_columns[name.strip()] = dtype.strip()
            # добавляем словарь в метаданные и возвращаем
            metadata[table_name] = dict_columns
            return metadata
    except AttributeError:
        print("Ошибка: Переданные метаданные не в формате словаря.")

def drop_table(metadata: dict,
               table_name: str) -> dict | None:
    """
    Функция проверяет наличие таблицы в мета_данных и в случае
    успеха удаляет её
    """
    try:
        if table_name in metadata:
            metadata.pop(table_name)
            return metadata
        else:
            print(f'Ошибка: Таблица \"{table_name}\" не существует.')
            return None
    except TypeError:
        print("Ошибка: Неверный тип данных.")

def list_tables(metadata: dict) -> list[str]:
    """
    Функция возвращающая список названий всех таблиц
    """
    return [" - " +table
            for table in metadata.keys()]