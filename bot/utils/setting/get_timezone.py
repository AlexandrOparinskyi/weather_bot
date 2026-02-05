def get_timezone_by_coords(lon: float) -> str:
    """
    Более точный расчет с учетом реальных границ часовых поясов
    :param lon: float
    :return: timezone
    """
    russian_timezones = [
        {"min_lon": 19.0, "max_lon": 39.0, "offset": 3},
        {"min_lon": 39.0, "max_lon": 60.0, "offset": 4},
        {"min_lon": 60.0, "max_lon": 90.0, "offset": 5},
        {"min_lon": 90.0, "max_lon": 105.0, "offset": 6,},
        {"min_lon": 105.0, "max_lon": 120.0, "offset": 7},
        {"min_lon": 120.0, "max_lon": 135.0, "offset": 8},
        {"min_lon": 135.0, "max_lon": 150.0, "offset": 9},
        {"min_lon": 150.0, "max_lon": 165.0, "offset": 10},
        {"min_lon": 165.0, "max_lon": 180.0, "offset": 11}
    ]

    for tz in russian_timezones:
        if tz["min_lon"] <= lon < tz["max_lon"]:
            return f"UTC+{tz['offset']}"
