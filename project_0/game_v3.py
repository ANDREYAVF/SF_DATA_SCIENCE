def game_core_v3(number: int = 1) -> int:
    """Сначала устанавливаем max и min, а потом постоянно сужаем границы
    вероятного нахождения числа в зависимости от того, больше оно или меньше нужного.
       Функция принимает загаданное число и возвращает число попыток

    Args:
        number (int, optional): Загаданное число. Defaults to 1.

    Returns:
        int: Число попыток
    """
    # Ваш код начинается здесь
    count = 0
    max_predict = 100
    min_predict = 1
    predict = max_predict // 2

    while number != predict:
        if max_predict - min_predict > 1: # еще одно условие выхода из цикла
            count += 1
            if number > predict:
                min_predict = predict
                predict = predict + ((max_predict - min_predict) // 2)
            elif number < predict:
                max_predict = predict
                predict = predict - ((max_predict - min_predict) // 2)
        else:
            break
    # Ваш код заканчивается здесь

    return count