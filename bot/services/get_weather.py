import aiohttp
from typing import Dict, Any, List


async def get_weather_data(city: str) -> Dict[str, Any]:
    """
    Получает данные о погоде для рекомендаций по одежде
    с разбивкой на утро/день/вечер
    """
    url = "http://api.weatherapi.com/v1/forecast.json"
    params = {
        'key': 'b37226ed91f5447192a185002252409',
        'q': city,
        'lang': 'ru',
        'days': 1,
        'hours': 24
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    current = data['current']
                    forecast_day = data['forecast']['forecastday'][0]['day']
                    location = data['location']
                    hours = data['forecast']['forecastday'][0]['hour']

                    # Получаем данные по периодам дня
                    periods_data = _get_periods_data(hours)

                    # Анализируем опасности и рекомендации
                    weather_analysis = _analyze_weather_for_clothing(
                        current, forecast_day, hours, periods_data
                    )

                    # Формируем итоговый ответ
                    return {
                        'success': True,
                        'location': location['name'],
                        'date': data['forecast']['forecastday'][0]['date'],

                        # Основные метрики для AI
                        'current_metrics': {
                            'temp': current['temp_c'],
                            'feels_like': current['feelslike_c'],
                            'condition': current['condition']['text'],
                            'condition_code': current['condition']['code'],
                            'wind_speed': current['wind_kph'],
                            'wind_gust': current['gust_kph'],
                            'humidity': current['humidity'],
                            'visibility': current['vis_km'],
                            'uv': current.get('uv', forecast_day['uv'])
                        },

                        # Дневные экстремумы
                        'daily_extremes': {
                            'min_temp': forecast_day['mintemp_c'],
                            'max_temp': forecast_day['maxtemp_c'],
                            'avg_temp': forecast_day['avgtemp_c'],
                            'chance_of_rain': forecast_day['daily_chance_of_rain'],
                            'chance_of_snow': forecast_day['daily_chance_of_snow'],
                            'max_wind': forecast_day['maxwind_kph']
                        },

                        # Данные по периодам дня (для одежды)
                        'periods': {
                            'morning': periods_data['morning'],  # 6-10
                            'day': periods_data['day'],  # 11-16
                            'evening': periods_data['evening'],  # 17-21
                            'night': periods_data['night'],  # 22-5
                        },

                        # Анализ для рекомендаций
                        'analysis': {
                            'hazards': weather_analysis['hazards'],
                            'thermal_level': weather_analysis['thermal_level'],
                            'wind_chill_severity': weather_analysis['wind_chill_severity'],
                            'precipitation_type': weather_analysis['precipitation_type'],
                            'visibility_status': weather_analysis['visibility_status'],
                            'max_time_outdoor': weather_analysis['max_time_outdoor'],
                            'key_hours': _get_key_hours_for_clothing(hours)
                        },

                        # Для нейросети (упрощенный формат)
                        'for_ai': {
                            'temperature_profile': weather_analysis['temperature_profile'],
                            'weather_type': weather_analysis['weather_type'],
                            'comfort_score': weather_analysis['comfort_score'],
                            'conditions_summary': weather_analysis['conditions_summary'],
                            'temp_range_today': f"{forecast_day['mintemp_c']}..{forecast_day['maxtemp_c']}",
                            'feels_like_now': current['feelslike_c']
                        },

                        # Полные почасовые данные (опционально, можно убрать если много)
                        'all_hours': hours if len(hours) <= 12 else hours[::2]  # каждый 2-й час если много
                    }
                else:
                    return {
                        'success': False,
                        'error': f"Ошибка API: {response.status}"
                    }

    except Exception as e:
        return {
            'success': False,
            'error': f"Ошибка соединения: {str(e)}"
        }


def _get_periods_data(hours: List[Dict]) -> Dict[str, Dict]:
    """Получает агрегированные данные по периодам дня"""
    periods = {
        'morning': {'start': 6, 'end': 10, 'hours': []},
        'day': {'start': 11, 'end': 16, 'hours': []},
        'evening': {'start': 17, 'end': 21, 'hours': []},
        'night': {'start': 22, 'end': 5, 'hours': []}
    }

    for hour in hours:
        hour_time = int(hour['time'][11:13])

        if 6 <= hour_time <= 10:
            periods['morning']['hours'].append(hour)
        elif 11 <= hour_time <= 16:
            periods['day']['hours'].append(hour)
        elif 17 <= hour_time <= 21:
            periods['evening']['hours'].append(hour)
        elif hour_time >= 22 or hour_time <= 5:
            periods['night']['hours'].append(hour)

    # Агрегируем данные для каждого периода
    result = {}
    for period_name, period_data in periods.items():
        hours_list = period_data['hours']
        if hours_list:
            temps = [h['temp_c'] for h in hours_list]
            feels_like = [h['feelslike_c'] for h in hours_list]
            conditions = [h['condition']['text'] for h in hours_list]

            # Находим самую частую погоду в периоде
            most_common_condition = max(set(conditions), key=conditions.count)

            result[period_name] = {
                'avg_temp': sum(temps) / len(temps),
                'min_temp': min(temps),
                'max_temp': max(temps),
                'avg_feels_like': sum(feels_like) / len(feels_like),
                'min_feels_like': min(feels_like),
                'max_feels_like': max(feels_like),
                'condition': most_common_condition,
                'condition_code': hours_list[0]['condition']['code'],
                'wind_avg': sum(h['wind_kph'] for h in hours_list) / len(hours_list),
                'precipitation_chance': max(h['chance_of_rain'] for h in hours_list),
                'hours_count': len(hours_list),
                'sample_hour': hours_list[0]['time'][11:16]  # пример времени
            }
        else:
            result[period_name] = None

    return result


def _analyze_weather_for_clothing(current: Dict, forecast_day: Dict,
                                  hours: List[Dict], periods_data: Dict) -> Dict[str, Any]:
    """Анализирует погоду для рекомендаций по одежде"""

    current_temp = current['temp_c']
    feels_like = current['feelslike_c']
    wind_chill = current.get('windchill_c', feels_like)
    visibility = current['vis_km']
    condition = current['condition']['text']
    condition_code = current['condition']['code']

    # Определяем тип осадков
    precipitation_type = 'none'
    if forecast_day['daily_chance_of_rain'] > 30:
        precipitation_type = 'rain'
    elif forecast_day['daily_chance_of_snow'] > 30:
        precipitation_type = 'snow'

    # Опасности
    hazards = []
    if feels_like <= -20:
        hazards.append('extreme_cold')
    elif feels_like <= -10:
        hazards.append('severe_cold')

    if visibility < 1:
        hazards.append('low_visibility')
    elif visibility < 5:
        hazards.append('reduced_visibility')

    if wind_chill <= -15:
        hazards.append('wind_chill_danger')

    if condition_code in [1063, 1066, 1069, 1072, 1087, 1150, 1153, 1168, 1171, 1180, 1183,
                          1186, 1189, 1192, 1195, 1198, 1201, 1204, 1207, 1210, 1213, 1216,
                          1219, 1222, 1225, 1237, 1240, 1243, 1246, 1249, 1252, 1255, 1258,
                          1261, 1264, 1273, 1276, 1279, 1282]:
        hazards.append('precipitation_expected')

    # Уровень тепла (от 1 - очень холодно до 10 - жарко)
    thermal_level = 1
    if feels_like > 25:
        thermal_level = 10
    elif feels_like > 20:
        thermal_level = 9
    elif feels_like > 15:
        thermal_level = 8
    elif feels_like > 10:
        thermal_level = 7
    elif feels_like > 5:
        thermal_level = 6
    elif feels_like > 0:
        thermal_level = 5
    elif feels_like > -5:
        thermal_level = 4
    elif feels_like > -10:
        thermal_level = 3
    elif feels_like > -15:
        thermal_level = 2

    # Профиль температуры
    if feels_like <= -25:
        temperature_profile = 'arctic'
    elif feels_like <= -15:
        temperature_profile = 'subzero_severe'
    elif feels_like <= 0:
        temperature_profile = 'subzero_mild'
    elif feels_like <= 10:
        temperature_profile = 'cold'
    elif feels_like <= 20:
        temperature_profile = 'cool'
    elif feels_like <= 25:
        temperature_profile = 'warm'
    else:
        temperature_profile = 'hot'

    # Тип погоды для AI
    weather_type = 'clear'
    if 'дождь' in condition.lower() or 'rain' in condition.lower():
        weather_type = 'rainy'
    elif 'снег' in condition.lower() or 'snow' in condition.lower():
        weather_type = 'snowy'
    elif 'туман' in condition.lower() or 'fog' in condition.lower():
        weather_type = 'foggy'
    elif 'облач' in condition.lower() or 'cloud' in condition.lower():
        weather_type = 'cloudy'

    # Максимальное время на улице (в минутах)
    max_time_outdoor = 120  # по умолчанию
    if 'extreme_cold' in hazards:
        max_time_outdoor = 20
    elif 'severe_cold' in hazards:
        max_time_outdoor = 45
    elif 'wind_chill_danger' in hazards:
        max_time_outdoor = 60

    # Сводка условий
    conditions_summary = []
    if precipitation_type != 'none':
        conditions_summary.append(precipitation_type)
    if 'low_visibility' in hazards:
        conditions_summary.append('fog')
    if 'extreme_cold' in hazards or 'severe_cold' in hazards:
        conditions_summary.append('freezing')

    return {
        'hazards': hazards,
        'thermal_level': thermal_level,
        'wind_chill_severity': 'severe' if wind_chill <= -15 else 'moderate' if wind_chill <= -5 else 'mild',
        'precipitation_type': precipitation_type,
        'visibility_status': 'zero' if visibility < 1 else 'low' if visibility < 5 else 'normal',
        'max_time_outdoor': max_time_outdoor,
        'temperature_profile': temperature_profile,
        'weather_type': weather_type,
        'comfort_score': max(0, min(100, (feels_like + 30) * 2)),  # грубая оценка комфорта 0-100
        'conditions_summary': conditions_summary
    }


def _get_key_hours_for_clothing(hours: List[Dict]) -> List[Dict]:
    """Получает ключевые часы для рекомендаций по одежде"""
    key_times = [6, 8, 10, 12, 14, 16, 18, 20, 22]
    result = []

    for hour in hours:
        hour_time = int(hour['time'][11:13])
        if hour_time in key_times:
            result.append({
                'hour': hour_time,
                'temp': hour['temp_c'],
                'feels_like': hour['feelslike_c'],
                'condition': hour['condition']['text'],
                'wind': hour['wind_kph'],
                'precipitation_chance': hour['chance_of_rain']
            })

    return result
