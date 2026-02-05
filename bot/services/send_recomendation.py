import json

import aiohttp

from bot.services import get_weather_data
from config import Config, load_config


async def get_recommendation_message(city: str,
                                     gender: str | None = None,
                                     style: str | None = None) -> str:
    config: Config = load_config()
    weather_data = await get_weather_data(city)

    if weather_data['success']:
        # Для нейросети
        ai_data = weather_data['for_ai']

        # temperature_profile, weather_type, comfort_score, etc.
        # Для рекомендаций по периодам
        morning = weather_data['periods']['morning']
        day = weather_data['periods']['day']
        evening = weather_data['periods']['evening']

        # Опасности
        hazards = weather_data['analysis']['hazards']
        # ['extreme_cold', 'low_visibility']

        # Текущая погода
        current = weather_data['current_metrics']

        json_data = {
            **ai_data,
            "periods": {"утро": morning, "день": day, "вечер": evening},
            "hazards": hazards,
            "current_metrics": current
        }
        message = ({"message": f"пол: {gender}"
                               f"стиль: {style}"
                               f"данные о погоде ниже:"
                               f"{json.dumps(json_data, ensure_ascii=False)}"})
        headers = {
            "content-type": "application/json",
            "authorization": f"Bearer {config.deepseek.token}"
        }
        timeout = aiohttp.ClientTimeout(total=30)
        api_url = f"{config.deepseek.api_url}/{config.deepseek.agent_id}/call"

        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(api_url,
                                    headers=headers,
                                    json=message) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get("message")
                else:
                    return "Ошибка получения данных о погоде"

    else:
        return "Ошибка получения данных о погоде"
