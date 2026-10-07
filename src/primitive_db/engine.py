import shlex

import prompt

from constants import (
    META_DATA_FILE_PATH,
    STRING_COMMON_COMMANDS,
    STRING_TABLE_COMMANDS,
)

from .core import (
    create_table,
    drop_table,
    list_tables,
)
from .utils import (
    load_metadata,
    save_metadata,
)


def print_help() -> None:
    """Выдает информацию в консоль на вызов команды help"""
    print(STRING_TABLE_COMMANDS)
    print(STRING_COMMON_COMMANDS)
def run() -> None:
    """
    Функция ввода данных от пользователя
    """
    print(STRING_TABLE_COMMANDS)
    print(STRING_COMMON_COMMANDS)
    while True:
        meta_data = load_metadata(META_DATA_FILE_PATH)
        user_input = prompt.string('>>> Введите команду: ')
        try:
            args = shlex.split(user_input)
        except (ValueError):
            print('Ошибка ввода.')
        match args[0]:
            case "exit":
                break
            case "help":
                print_help()
            case "create_table":
                if len(args)<2:
                    print('Ошибка: не задано имя таблицы.')
                    continue
                result = create_table(meta_data,
                                      args[1],
                                      [col for col in args[2:]])
                if result is not None:
                    print(f"Таблица \"{args[1]}\" успешно создана "
                          f"со столбцами: "
                          f"{', '.join(f"{k}:{v}" 
                                       for k, v in 
                                       result[args[1]].items())}")
                    save_metadata(META_DATA_FILE_PATH, result)
            case "list_tables":
                list_tables_name=list_tables(meta_data)
                for table in list_tables_name:
                    print(table)
            case "drop_table":
                if len(args)<2:
                    print('Ошибка: не задано имя таблицы.')
                    continue
                result = drop_table(meta_data, args[1])
                if result is not None:
                    print(f"Таблица \"{args[1]}\" успешно удалена.")
                    save_metadata(META_DATA_FILE_PATH, result)
            case _:
                print(f"Функции <{args[0]}> нет. Попробуйте снова.")