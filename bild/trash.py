"""Хранит то, что совсем не нужно, но удалять жалко"""


# Генерирует "случайный" сид, исходя из координат
def seed_from_cord(x: int, y: int) -> int:
    tmp = x << abs(y)
    if tmp.bit_length() < 16:
        return tmp
    else:
        while tmp.bit_length() > 16:
            tmp = round(tmp / 1000)
        return tmp
