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