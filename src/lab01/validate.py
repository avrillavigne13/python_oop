def validate_string(value: str, field_name: str, min_length: int = 1, max_length: int = 50) -> None:
    """
    Проверка строковых полей.
    
    Аргументы:
        value: проверяемое значение
        field_name: имя поля для сообщения об ошибке
        min_length: минимальная длина строки
        max_length: максимальная длина строки
    
    Исключения:
        TypeError: если значение не строка
        ValueError: если строка пустая или слишком длинная
    """
    if not isinstance(value, str):
        raise TypeError(f"{field_name} должен быть строкой (str), получен {type(value).__name__}")
    
    if len(value.strip()) < min_length:
        raise ValueError(f"{field_name} не может быть пустым или короче {min_length} символа(ов)")
    
    if len(value) > max_length:
        raise ValueError(f"{field_name} не может быть длиннее {max_length} символов")


def validate_int(value: int, field_name: str, min_val: int, max_val: int) -> None:
    """
    Проверка целочисленных полей.
    
    Аргументы:
        value: проверяемое значение
        field_name: имя поля для сообщения об ошибке
        min_val: минимальное допустимое значение
        max_val: максимальное допустимое значение
    """
    if not isinstance(value, int):
        raise TypeError(f"{field_name} должен быть целым числом (int), получен {type(value).__name__}")
    
    if value < min_val:
        raise ValueError(f"{field_name} не может быть меньше {min_val}")
    
    if value > max_val:
        raise ValueError(f"{field_name} не может быть больше {max_val}")


def validate_float(value: float, field_name: str, min_val: float, max_val: float) -> None:
    """
    Проверка чисел с плавающей точкой.
    """
    if not isinstance(value, (int, float)):
        raise TypeError(f"{field_name} должен быть числом (int/float), получен {type(value).__name__}")
    
    # Приводим int к float для единообразия проверки
    value = float(value)
    
    if value < min_val:
        raise ValueError(f"{field_name} не может быть меньше {min_val}")
    
    if value > max_val:
        raise ValueError(f"{field_name} не может быть больше {max_val}")


def validate_experience(value: int, current_level: int) -> None:
    """
    Специализированная проверка для опыта.
    Опыт не должен превышать необходимый для следующего уровня.
    
    Формула: для перехода с уровня N на N+1 нужно N * 1000 опыта
    """
    max_exp_for_current_level = current_level * 1000
    
    if value > max_exp_for_current_level:
        raise ValueError(
            f"Опыт ({value}) превышает максимальный для уровня {current_level} "
            f"(максимум: {max_exp_for_current_level})"
        )