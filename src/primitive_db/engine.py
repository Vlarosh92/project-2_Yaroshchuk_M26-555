import shlex

import prompt
from prettytable import PrettyTable

from constants import (
    META_DATA_FILE_PATH,
    STRING_COMMON_COMMANDS,
    STRING_DATA_COMMANDS,
    STRING_TABLE_COMMANDS,
)

from .core import (
    create_table,
    delete,
    drop_table,
    info,
    insert,
    list_tables,
    select,
    update,
)
from .parser import parse_string_for_crud
from .utils import (
    create_file_in_data,
    delete_file_from_data,
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)


def print_help() -> None:
    """Выдает информацию в консоль на вызов команды help"""
    print(STRING_TABLE_COMMANDS)
    print(STRING_DATA_COMMANDS)
    print(STRING_COMMON_COMMANDS)

def check_attr_in_meta(cond: dict, meta: dict, table_name: str) -> None:
    """
    Функция проверяет соответствие ключа из условия cond,
    списку ключей в метаданных таблицы meta
    """
    key_wc = list(cond.keys())[0]
    if key_wc not in meta:
        print(f'Ошибка: Поля <{key_wc}> '
              f'в таблице <{table_name}> не существует.')
        return False
    return True

def run() -> None:
    """
    Функция ввода данных от пользователя
    """
    print(STRING_TABLE_COMMANDS)
    print(STRING_DATA_COMMANDS)
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
                    create_file_in_data(args[1])
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
                    delete_file_from_data(args[1])
            case "insert":
                if len(args)<3:
                    print('Ошибка: не задано имя таблицы.')
                    continue
                if args[2] not in meta_data:
                    print(f'Ошибка: Таблица "{args[2]}" не существует.')
                    continue

                data_from_parse_value = parse_string_for_crud(user_input)
                if not data_from_parse_value:
                    continue

                table_name = data_from_parse_value[0]
                values_data = data_from_parse_value[1]

                table_data = insert(meta_data,
                                    load_table_data(table_name),
                                    table_name,
                                    values_data)
                if table_data:
                    print(f"Запись с ID={table_data[-1]["ID"]}"
                          f" успешно добавлена в таблицу "
                          f"\"{table_name}\".")
                    save_table_data(table_name,
                                    table_data)
            case "select":
                if len(args)<3:
                    print('Ошибка: не задано имя таблицы.')
                    continue
                if args[2] not in meta_data:
                    print(f'Ошибка: Таблица \"{args[2]}\" не существует.')
                    continue

                data_from_parse_value = parse_string_for_crud(user_input)
                if not data_from_parse_value:
                    continue

                table_name = data_from_parse_value[0]
                pretty_table = PrettyTable()

                where_clause = None
                if len(data_from_parse_value) > 1:
                    where_clause = data_from_parse_value[1]
                    if not check_attr_in_meta(where_clause,
                                              meta_data[table_name],
                                              table_name):
                        continue

                select_answer = select(load_table_data(table_name),
                                                      where_clause)

                if select_answer:
                    pretty_table.field_names = list(select_answer[0].keys())
                    for row in select_answer:
                        pretty_table.add_row(list(row.values()))
                if pretty_table.rowcount > 0:
                    print(pretty_table)

            case "update":
                if len(args)<2:
                    print('Ошибка: не задано имя таблицы.')
                    continue
                if args[1] not in meta_data:
                    print(f'Ошибка: Таблица \"{args[1]}\" не существует.')
                    continue

                data_from_parse_value = parse_string_for_crud(user_input)
                if not data_from_parse_value:
                    continue

                table_name = data_from_parse_value[0]


                set_clause = data_from_parse_value[1]
                where_clause = data_from_parse_value[2]


                old_table_data = load_table_data(table_name)

                # Проверяем что заданные поля существует в таблице
                if not check_attr_in_meta(where_clause,
                                          meta_data[table_name],
                                          table_name):
                    continue
                if not check_attr_in_meta(set_clause,
                                          meta_data[table_name],
                                          table_name):
                    continue

                table_data = update(load_table_data(table_name),
                                    set_clause,
                                    where_clause)


                if table_data:
                    # с помощью функции zip сравниваем
                    # все значения словарей для нахождения
                    # расхождений и формирования списка id
                    update_id_list = [o["ID"]
                                      for o, n in zip(old_table_data, table_data)
                                      if o != n]
                    for u_i_l in update_id_list:
                        print(f"Запись с ID={u_i_l}"
                              f" в таблице \"{table_name}\" успешно обновлена.")
                    save_table_data(table_name, table_data)
            case "delete":
                if len(args)<3:
                    print('Ошибка: не задано имя таблицы.')
                    continue
                if args[2] not in meta_data:
                    print(f'Ошибка: Таблица "{args[2]}" не существует.')
                    continue

                data_from_parse_value = parse_string_for_crud(user_input)
                if not data_from_parse_value:
                    continue

                table_name = data_from_parse_value[0]

                where_clause = data_from_parse_value[1]

                # Проверяем что заданное поле существует в таблице
                if not check_attr_in_meta(where_clause,
                                          meta_data[table_name],
                                          table_name):
                    continue

                # добавляем версию до удаления для нахождения id
                # которые были удалены
                old_table_data = load_table_data(table_name)

                table_data = delete(load_table_data(table_name),
                                    where_clause)


                if table_data is not None:
                    # находим удаленные id
                    old_table_id = {row["ID"]
                                    for row in table_data}
                    delete_id_list = [row["ID"]
                                      for row in old_table_data
                                      if row["ID"] not in old_table_id]

                    for d_i_l in delete_id_list:
                        print(f"Запись с ID={d_i_l}"
                              f" успешно удалена из таблицы"
                              f" \"{table_name}\".")
                    save_table_data(table_name, table_data)
            case "info":
                if len(args)<2:
                    print('Ошибка: не задано имя таблицы.')
                    continue
                if args[1] in meta_data:
                    result = info(meta_data,
                                  load_table_data(args[1]),
                                  args[1])
                    if result:
                        print(result)
                else:
                    print(f'Ошибка: Таблица "{args[1]}" не существует.')

            case _:
                print(f"Функции <{args[0]}> нет. Попробуйте снова.")