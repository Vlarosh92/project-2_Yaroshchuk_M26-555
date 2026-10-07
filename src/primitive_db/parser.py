import shlex

from constants import ALLOWED_CHAR, KEY_WORDS


def string_to_type(input_str: str) -> str | bool | int | None:
    """
    При парсинге мы получаем все значения с типом
    str, эта функция преобразует в другие типы
    в рамках допустимых форматов.
    Также проверяет корректность формата ввода данных
    """

    # проверяем на тип bool
    if input_str.lower() == "true" and "\"" not in input_str:
        return True
    if input_str.lower() == "false" and "\"" not in input_str:
        return False
    try:
        # проверяем на тип int
        if "\"" in input_str:
            raise ValueError
        return int(input_str)
    except ValueError:
        # проверяем на тип str
        # окаймляющие кавычки обязательны
        if input_str[0]=="\"" and input_str[-1]=="\"":
            return input_str[1:-1]
        else:
            return None


def split_by_delimiters(raw: str,
                        delimiters_start: str,
                        delimiters_end: str) -> list[str]:
    """
    Функция разделяет данные внутри блока values
    для команды insert
    """
    if not raw:
        return []
    # проверяем что есть окаймляющие скобки
    # и что скобок внутри нет
    if (raw[0] != delimiters_start
            or raw[-1] != delimiters_end
            or delimiters_start in raw[1:-1]
            or delimiters_end in raw[1:-1]):
        return []
    # убираем скобки
    # разделяем по запятой на блоки
    raw=(raw.replace(delimiters_start, "").
                   replace(delimiters_end, "").
                   split(","))
    # Убираем лишние пробелы, сохраняя структуру внутри кавычек
    clear_raw = []
    for cr in raw:
        first_s = cr.find('"')
        last_s = cr.rfind('"', first_s + 1)
        if last_s != -1 and last_s != -1:
            inside_str = cr[first_s: last_s + 1]
            outside_str_left = cr[:first_s].replace(" ", "")
            outside_str_right = cr[last_s + 1:].replace(" ", "")
            new_block = outside_str_left + inside_str + outside_str_right
        else:
            new_block = cr.replace(" ", "")
        clear_raw.append(new_block)

    return clear_raw


def separator(input_list: list[str]) -> dict | None:
    """
    Функция разбивает данные на словарь из ключа и значения.
    Также преобразовывает строки в их реальные типы
    """
    value = string_to_type(input_list[2])
    if value is not None:
        return {input_list[0]: string_to_type(input_list[2])}
    else:
        return None

def crud_parse(str_list: list[str], key_words: dict) -> list[list[str]]:
    """
    Функция получает список слов из пользовательского ввода
    разбивает их по словарю ключевых слов
    и возращает список разбитый на логические блоки
    списков
    """
    k_word_list = key_words[str_list[0]]["k_word"]
    table_name_ind = key_words[str_list[0]]["table_name_ind"]

    output_info = []
    current_block = []
    order_k_word = 0

    for num, str_info in enumerate(str_list[1:]):
        if str_info == k_word_list[order_k_word]:

            if num>=table_name_ind:
                output_info.append(current_block)
                current_block = []

            # двигаем указатель ключевых слов
            if order_k_word < len(k_word_list) - 1:
                order_k_word += 1
        else:

            current_block.append(str_info)

    # добавляем последний блок
    if current_block:
        output_info.append(current_block)

    return output_info


def parse_string_for_crud(input: str) -> list[list | dict | None]:
    """
    функция определяющая логику обработки данных
    для различных crud команд.
    """
    # Копия словаря ключевых слов для CRUD команд
    # необходима для случая select без where
    # когда задается модифицируемый словарь
    key_words = dict(KEY_WORDS)

    str_list = shlex.split(input, posix=False)

    # проверка, что команда в списке допустимых
    if str_list[0] not in key_words:
        print(f"Функции <{str_list[0]}> нет. Попробуйте снова.")
        return []

    key_words[str_list[0]] = dict(key_words[str_list[0]])
    # Добавляем вариант для select from без where
    if str_list[0] == "select" and "where" not in input:
        key_words[str_list[0]]["k_word"] = ["from"]


    # проверка, что все ключевые слова команды присутствуют
    if not all(k_word in str_list
                for k_word in key_words[str_list[0]]["k_word"]):
        print(f"Некорректный формат ввода данных"
              f": <{" ".join(str_list[1:])}>.Попробуйте снова.")
        return []

    output_info = crud_parse(str_list, key_words)

    try:
        match str_list[0]:
            case "insert":
                if (len(output_info) == 2 and
                        len(output_info[0]) == 1 and
                        len(output_info[1]) >= 1):
                    table_name = output_info[0][0]

                    if all(ch in ALLOWED_CHAR for ch in table_name):
                        blocks = split_by_delimiters(" ".join(str(column)
                                    for column in output_info[1]),
                                    key_words[str_list[0]]["delimiters_start"],
                                    key_words[str_list[0]]["delimiters_end"])
                        if not blocks:
                            print(f"Некорректное значение: "
                                  f"<{"".join(output_info[1])}>.Попробуйте снова.")
                            return []
                        output_info[0]=output_info[0][0]
                        # пересобираем с реальными типами значений
                        output_info[1] = [string_to_type(block) for block in blocks]
                        if None not in output_info[1]:
                            return output_info
                        else:
                            print(f"Некорректное значение: "
                                  f"<{" ".join(str_list[4:])}>. Попробуйте снова.")
                            return []
                    else:
                        print(f"Некорректное значение: "
                              f"<{table_name}>. Попробуйте снова.")
                        return []
                else:
                    print(f"Некорректное значение: "
                          f"<{" ".join(str_list[1:])}>. Попробуйте снова.")
                    return []
                # разбиваем поле с данными на блоки

            case "select":

                if (len(output_info) == 2 and
                        len(output_info[0]) == 1 and
                        len(output_info[1]) == 3 and
                        output_info[1][1] in key_words[str_list[0]]["separators"]):

                    output_info[0] = output_info[0][0]
                    output_info[1] = separator(output_info[1])

                    if output_info[1]:
                        return output_info
                    else:
                        print(f"Некорректное значение: "
                              f"<{" ".join(str_list[4:])}>. Попробуйте снова.")
                else:
                    if (len(output_info) == 1 and
                            len(output_info[0]) == 1):
                        output_info[0] = output_info[0][0]
                        return output_info
                    else:
                        print(f"Некорректное значение: "
                              f"<{" ".join(str_list[1:])}>. Попробуйте снова.")
                        return []
            case "update":
                if (len(output_info) == 3 and
                        len(output_info[0]) == 1 and
                        len(output_info[1]) == 3 and
                        len(output_info[2]) == 3 and
                        output_info[1][1] in key_words[str_list[0]]["separators"] and
                        output_info[2][1] in key_words[str_list[0]]["separators"]):
                    output_info[0] = output_info[0][0]
                    output_info[1] = separator(output_info[1])
                    if not output_info[1]:
                        print(f"Некорректное значение: "
                              f"<{" ".join(str_list[3:6])}>. Попробуйте снова.")
                        return []
                    output_info[2] = separator(output_info[2])
                    if output_info[2]:
                        return output_info
                    else:
                        print(f"Некорректное значение: "
                              f"<{" ".join(str_list[7:])}>. Попробуйте снова.")
                        return []
                else:
                    print(f"Некорректное значение: "
                          f"<{" ".join(str_list[1:])}>. Попробуйте снова.")
                    return []

            case "delete":
                if (len(output_info) == 2 and
                        len(output_info[0]) == 1 and
                        len(output_info[1]) == 3 and
                        output_info[1][1] in key_words[str_list[0]]["separators"]):
                    output_info[0] = output_info[0][0]
                    output_info[1] = separator(output_info[1])
                    if output_info[1]:
                        return output_info
                    else:
                        print(f"Некорректное значение: "
                              f"<{" ".join(str_list[4:])}>. Попробуйте снова.")
                else:
                    print(f"Некорректное значение: "
                          f"<{" ".join(str_list[1:])}>. Попробуйте снова.")
                    return []
            case _:
                return []
    except IndexError:
        raise IndexError("Ошибка: Запрос к несуществующему элементу.")