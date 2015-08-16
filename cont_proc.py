# -*- coding: utf-8 -*-

def clear_string(str, to_int = None):
    '''
    Чистим рядок від "мусора" - нечислових символів.
    '''
    new_str = ''
    for s in str:
        # спочатку шукаємо крапку (якщо ж число с плаваючою крапкою)
        # при цьому в новому рядку не повинно бути більше однієї крапки
        # і в умові to_int не визначений
        if s == '.' and '.' not in new_str and not to_int:
            new_str += s
        else:
            try:
                i = int(s)
                new_str += s
            except:
                pass
    return new_str

def str_to_int(str):
    '''
    Перетворення рядка в ціле число
    '''
    # попробуємо скористатись самим простим способом
    try:
        return int(str)
    except:
        # якщо не вийшло, то перевіряємо чому? допускаємо, що було передано не ціле число в рядку
        if '.' in str:
            str = str[0:str.find('.')]
            return str_to_int(str)
        else:
            # якщо ж зовсім справи погані, то вертаємо 0 або пустий рядок
            return ''

def check_int(str):
    try:
        int(str)
        return True
    except:
        return False

def str_to_float(str):
    '''
    Перетворення рядка в число с плаваючою крапкою
    '''
    # попробуємо скористатись самим простим способом
    try:
        return float(str)
    except:
        # інших варіантів не залишилось, скоріш за все функція прийняла на вході мусор
        return 0

def check_float(str):
    try:
        float(str)
        return True
    except:
        return False

