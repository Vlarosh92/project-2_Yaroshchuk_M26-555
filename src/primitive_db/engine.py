import prompt


def welcome() -> None:
    """
    Функция ввода данных от пользователя
    """
    print(
        "Первая попытка запустить проект!\n"
        "***\n"
        "<command> exit - выйти из программы\n"
        "<command> help - справочная информация\n"
    )
    while True:


        user_input = prompt.string('>>> Введите команду: ')

        match user_input:
            case "exit":
                break
            case "help":
                print(
                     "Первая попытка запустить проект!\n"
                     "***\n"
                     "<command> exit - выйти из программы\n"
                     "<command> help - справочная информация\n"
                     )