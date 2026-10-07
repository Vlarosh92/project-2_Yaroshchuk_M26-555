# путь к метаданным таблиц
META_DATA_FILE_PATH = "db_meta.json"
# перевод строковых представлений к реальным типам
REAL_TYPE = {"int": int, "str": str, "bool": bool}
# допустимые типы данных
VALID_TYPES = {"int", "str", "bool"}
# допустимые символы в имени таблицы
ALLOWED_CHAR = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                   "abcdefghijklmnopqrstuvwxyz"
                   "0123456789"
                   "_")
# словарь ключевых слов для CRUD команд
KEY_WORDS = {
        "insert": {
            "k_word": ["into", "values"],
            "table_name_ind": 1,
            "delimiters_start": "(",
            "delimiters_end": ")",
        },
        "select": {
            "k_word": ["from", "where"],
            "table_name_ind": 1,
            "separators": {"="}
        },
        "update": {
            "k_word": ["set", "where"],
            "table_name_ind": 0,
            "separators": {"="}
        },
        "delete": {
            "k_word": ["from", "where"],
            "table_name_ind": 1,
            "separators": {"="},
        },
    }
# текстовый формат работы с консолью
STRING_TABLE_COMMANDS = (
"\n"
"***Процесс работы с таблицей***\n"
"\n"
"Функции:\n"

"<command> create_table <имя_таблицы>"
" <столбец1:тип>"
" <столбец2:тип>"
" .. - создать таблицу\n"

"<command> list_tables"
" - показать список всех таблиц\n"
"<command> drop_table <имя_таблицы>"
" - удалить таблицу\n"
)

STRING_COMMON_COMMANDS = (
"***Общие команды***:\n"
"\n"
"<command> exit - выход из программы\n"
"<command> help - справочная информация\n"
)

STRING_DATA_COMMANDS = (
"***Операции с данными***\n"
"\n"
"Функции:\n"

"<command> insert into <имя_таблицы>"
" values (<значение1>, <значение2>, ...)"
" - создать запись.\n"

"<command> select from <имя_таблицы>"
" where <столбец> = <значение>"
" - прочитать записи по условию.\n"

"<command> select from <имя_таблицы>"
" - прочитать все записи.\n"

"<command> update <имя_таблицы>"
" set <столбец1> = <новое_значение1>"
" where <столбец_условия> = <значение_условия>"
" - обновить запись.\n"

"<command> delete from <имя_таблицы>"
" where <столбец> = <значение>"
" - удалить запись.\n"

"<command> info <имя_таблицы>"
" - вывести информацию о таблице.\n"
)