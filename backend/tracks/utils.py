import math


def get_distance(
        latitude_end: float,
        latitude_start: float,
        longitude_end: float,
        longitude_start: float
) -> float:
    """
    Расчитать расстояние между точками на поверхности Земли.
    Params:
    аргументы передавать только в градусах.
    возвращаемое значение - киллометры!
    """
    coeff = 0.01744  # Преобразуем радианы в градусы
    RUDIUS = 6371  # Радиус земли. Усредненный
    radian = math.acos(
        math.sin(latitude_end*coeff)*math.sin(latitude_start*coeff) +
        math.cos(latitude_end*coeff)*math.cos(latitude_start*coeff) *
        math.cos((longitude_end-longitude_start)*coeff)
    )
    path_length = radian * RUDIUS
    return path_length
