from constants import ALLOWED_CHAR, REAL_TYPE, VALID_TYPES
from decorators import confirm_action_decorator, handle_db_errors, log_time


@handle_db_errors
def create_table(metadata: dict,
                 table_name:str,
                 columns:list[str]) -> dict | None:
    """
    Функция принимает текущие метаданные, имя таблицы и список столбцов.
    Делает проверку корректности данных и отсутствия такой таблицы,
    в случае успеха, обновляет словарь metadata и возвращает его.
    """
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

@confirm_action_decorator("удаление таблицы")
@handle_db_errors
def drop_table(metadata: dict,
               table_name: str) -> dict | None:
    """
    Функция проверяет наличие таблицы в мета_данных и в случае
    успеха удаляет её
    """
    if table_name in metadata:
        metadata.pop(table_name)
        return metadata
    else:
        print(f'Ошибка: Таблица \"{table_name}\" не существует.')
        return None

def list_tables(metadata: dict) -> list[str]:
    """
    Функция возвращающая список названий всех таблиц
    """
    return [" - " +table
            for table in metadata.keys()]

@log_time
@handle_db_errors
def insert(metadata: dict,
           table_data: list[dict],
           table_name: str,
           values: list[int | bool | str]) -> list[dict] | None:
    """
    Функция создание записи в таблице.
    Типы и количество данных должны соответствовать метаданным
    """
    if table_name in metadata:

        m_data = metadata[table_name]
        m_data.pop("ID", None)
        # Переводим строку с типом данных, в реальный тип
        metadata_type = [REAL_TYPE[m_type]
                         for key, m_type in m_data.items()
                         if m_type in REAL_TYPE]
        # Создаем список имен для словаря
        metadata_name = [key
                         for key, m_type in m_data.items()
                         if m_type in REAL_TYPE]
        # Создаем список типов входящих значений
        values_type = [type(val)
                       for val in values]

        if len(values_type) != len(metadata_type):
            print(f"В таблице {table_name} "
                  f"количество столбцов ввода {len(values_type)}\n"
                  f"не соответствуют количеству столбцов "
                  f"в метаданных таблицы(без ID) {len(metadata_type)}")
            return None
        else:

            # добавляем новый id с проверкой для первой записи
            new_id = max((row["ID"]
                          for row in table_data), default=0) + 1
            # создаем новую запись. Сшиваем данные
            # -> переводим в словарь
            # -> добавляем id
            voc = {
                "ID": new_id,
                **{name: val for name, val in zip(metadata_name, values)}
            }
            # Проверяем что все типы соответствуют метаданным,
            # сшиваем типы (zip)
            # -> сравнием
            # -> проверяем чтобы все соответствовали (all)
            if all(v_type == m_type
                   for v_type, m_type in zip(values_type, metadata_type)):
                table_data.append(voc)
                return table_data
            else:
                print(f"В таблице {table_name} "
                      f"тип вводимых данных {values_type} "
                      f"не соответствуют "
                      f"типу данных {metadata_type} "
                      f"по схеме метаданных")
                return None
    else:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None

@log_time
@handle_db_errors
def select(table_data: list[dict],
           where_clause: dict[str, int | bool | str]=None) -> list[dict] | None:
    """
    Функция выдачи данных из таблицы по условию where_clause
    """
    if where_clause is None:
        return table_data
    else:
        # Разбиваем условие на ключ и значение
        if not where_clause:
            print("Ошибка: Словарь условий не имеет значений.")
            return None

        key, value = next(iter(where_clause.items()))
        if any(key not in t_data for t_data in table_data):
            print(f"Некорректное значение: <{where_clause}>. Попробуйте снова.")
            return None
        else:
            # Проверяем на соответствие типу данных атрибута
            if type(value) is type(table_data[0][key]):
                return [data
                        for data in table_data
                        if data[key] == value]
            else:
                print(f"Некорректный тип данных where: "
                      f"<{type(table_data[0][key])} = {type(value)}>. "
                      f"Попробуйте снова.")
                return None

@handle_db_errors
def update(table_data: list[dict],
           set_clause:  dict[str, int | bool | str],
           where_clause:  dict[str, int | bool | str]) -> list[dict | None]:
    """
    Функция обновления данных в таблице
    по условию where_clause
    """
    if not where_clause:
        print("Ошибка: Не указаны условия.")
        return []
    else:
        if not set_clause:
            print("Ошибка: Не указаны изменения.")
            return []

        # Получаем ключ и значение условия
        key_wc, value_wc = next(iter(where_clause.items()))
        # Получаем ключ и значение обновления
        key_sc, value_sc = next(iter(set_clause.items()))
        if key_sc == "ID":
            print("Запрет на смену ID.")
            return []
        new_table_data = []
        if type(value_wc) is not type(table_data[0][key_wc]):
            print(f"Неверный тип данных where "
                  f"{type(value_wc)} "
                  f"для выбранного значения "
                  f"{type(table_data[0][key_wc])}")
            return []
        for dict_field in table_data:
            if (dict_field[key_wc] == value_wc
                    and key_wc in dict_field
                    and key_sc in dict_field):
                if type(value_sc) is type(dict_field[key_sc]):
                    dict_field[key_sc] = value_sc
                else:
                    print(f"Неверный тип данных set "
                          f"{type(value_sc)} "
                          f"для выбранного значения "
                          f"{type(dict_field[key_sc])}")
                    return []

            new_table_data.append(dict_field)
        return new_table_data

@confirm_action_decorator("удаление записи")
@handle_db_errors
def delete(table_data: list[dict],
           where_clause: dict[str, int | bool | str]) -> list[dict] | None:
    """
    Функция удаление записей из таблицы
    по условию where_clause
    """
    # Получаем ключ и значение
    key_wc, value_wc = next(iter(where_clause.items()))
    # Проверяем наличия условий и наличия такого столбца
    if any(key_wc not in t_data for t_data in table_data):
        print("Условие отсутствует в таблице")
        return None
    else:

        if type(value_wc) is type(table_data[0][key_wc]):
            return [dict_field
                    for dict_field in table_data
                    if not dict_field[key_wc] == value_wc]
        else:
            print(f"Некорректный тип данных: "
                  f"<{type(value_wc)} = {type(table_data[0][key_wc])}>. "
                  f"Попробуйте снова.")
            return None

@handle_db_errors
def info(metadata: dict,
         table_data: list[dict],
         table_name: str) -> str:
    """
    Функция выдачи информации о таблице
    """
    # создаем список строк формата: имя:тип
    data = [key + ":" + val
            for key, val in metadata[table_name].items()]
    # создаем строку с информацией о таблице
    info_str = f"Таблица: {table_name}\n"
    info_str += "Столбцы: " + ", ".join(str(column)
                                        for column in data)
    info_str += f"\nКоличество записей: {len(table_data)}"
    return info_str

