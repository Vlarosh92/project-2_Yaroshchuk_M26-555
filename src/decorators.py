import time

import prompt


def handle_db_errors(func):
    """
    Декоратор для ловли исключений
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("Ошибка: Файл данных не найден. "
                  "Возможно, база данных не инициализирована.")
        except TypeError:
            print("Ошибка: Неверный тип данных.")
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец {e} не найден.")
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
        except AttributeError:
            print("Ошибка: Объект не имеет такого свойства или метода.")
        except IndexError:
            print("Ошибка: Запрос к несуществующему элементу.")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper

def confirm_action_decorator(description: str):
    """
    Декоратор для уточнения операций с подтверждением
    """
    def confirm_action(func): # объявляем декоратор
        def wrapper(*args, **kwargs):
            user_input = prompt.string(f'Вы уверены, что хотите'
                                       f' выполнить "{description}"? [y/n]:')
            if user_input.strip() == 'y':
                return func(*args, **kwargs)
            else:
                return None
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper
    return confirm_action # возвращаем декоратор

def log_time(func):
    """
    Декоратор для измерения времени выполнения
    """
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        d_time = end_time - start_time
        print(f"Функция <{func.__name__}>: выполнилась за {d_time:.3f} секунд.")
        return result
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper

def create_cacher():
    """
    Функцию с замыканием для кэширования
    результатов запросов
    """
    cache = dict()
    def cache_result(key: str, value_func: callable):
        nonlocal cache
        if key not in cache:
            cache[key] = value_func()
        return cache[key]
    return cache_result

